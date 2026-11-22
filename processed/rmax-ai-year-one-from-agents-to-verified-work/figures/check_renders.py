#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""Offline publication gates and host-only, tiled Chromium capture."""
from __future__ import annotations

import argparse
import base64
from contextlib import ExitStack, contextmanager
from datetime import date
from html import unescape
from html.parser import HTMLParser
import json
import math
import os
from pathlib import Path
import re
import select
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
import time
from urllib.parse import unquote, urljoin, urlsplit
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
SLUG = HERE.parent.name
ROOT = HERE.parents[2]
NOTE = ROOT / "notes" / SLUG
LIMIT = 8192
WORDS = re.compile(r"\b\w+(?:[’'.,-]\w+)*")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def prose_count(text):
    main = text.partition("\n---\n")[2].partition("## Positioning note")[0]
    main = re.sub(r"^(?:<img .*|\*Figure .*|\|[-|: ]+\|)$", "", main, flags=re.M)
    main = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", main)
    return len(WORDS.findall(plain_html(main)))


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.elements = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))

    def attrs(self, tag, key):
        return [attrs[key] for kind, attrs in self.elements if kind == tag and key in attrs]


def normalized(text):
    return " ".join(unescape(text).replace("’", "'").split())


def plain_html(text):
    # Separate adjacent block elements while preserving punctuation after inline links.
    text = re.sub(r"</(?:th|td|li|p|h[123]|figcaption)>", " ", text)
    return normalized(re.sub(r"<[^>]+>", "", text))


def plain_md(text):
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"^(?:<img .*|\|[-|: ]+\|)$", "", text, flags=re.M)
    text = re.sub(r"^(?:#+ |- |\d+\. )", "", text, flags=re.M)
    return plain_html(text.replace("|", " ").replace("*", "").replace("`", ""))


def frontmatter(md):
    # Parse the repository's flat mapping, ISO dates and indented scalar lists.
    schema = (ROOT / "notes/schema.yaml").read_text()
    types = dict(re.findall(r"^(\w+):\n  type: (string|date|list)$", schema, re.M))
    require(len(types) == len(re.findall(r"^\w+:$", schema, re.M)), "unsupported schema field")
    header, body = md.removeprefix("---\n").split("\n---\n", 1)
    require(md.startswith("---\n"), "frontmatter opening delimiter")
    fields = {}
    for line in header.splitlines():
        if line.startswith("  - "):
            require(isinstance(fields[key], list) and line[4:].strip(), "invalid list entry")
            fields[key].append(line[4:])
            continue
        key, sep, value = line.partition(":")
        require(sep and key in types and key not in fields, f"invalid field {key}")
        value = value.strip()
        if types[key] == "list":
            require(not value, f"expected block list for {key}")
            value = []
        elif types[key] == "date":
            require(date.fromisoformat(value).isoformat() == value, f"invalid date {key}")
        elif value.startswith('"'):
            value = json.loads(value)
        else:
            require(re.fullmatch(r"[\w][^#\n]*", value) and ": " not in value, f"invalid scalar {key}")
            require(value.lower() not in {"true", "false", "null", "yes", "no", "on", "off"}
                    and not re.fullmatch(r"[-+]?\d+(?:\.\d+)?|\d{4}-\d{2}-\d{2}", value),
                    f"expected string for {key}")
        fields[key] = value
    require(set(fields) == set(types) and all(fields.values()), "missing or empty frontmatter")
    require(fields["slug"] == SLUG and fields["canonical_url"] == f"https://rmax.ai/notes/{SLUG}/", "route")
    return fields, body


def local_link(page, link):
    url = urlsplit(urljoin("https://rmax.ai/" + page.relative_to(ROOT).as_posix(), link))
    if url.hostname == "rmax.ai":
        target = ROOT / unquote(url.path).lstrip("/")
        if target.is_dir():
            target /= "index.html"
        require(target.is_file(), f"{page.name}: missing {link}")


def check_footer(page, text):
    require('/styles/footer.css' in page.attrs('link', 'href'), "footer stylesheet")
    require(('footer', {'class': 'rmax-footer'}) in page.elements, "footer element")
    for element in ('agent-thought', 'agent-name', 'year'):
        require(element in page.attrs('span', 'id'), element)
    block = re.search(r'window\.footerThoughts\s*=\s*\[(.*?)\];\s*</script>\s*<script src="/scripts/footer.js">', text, re.S)
    require(block, "footer initialization order")
    pattern = r'\{\s*text:\s*"([^"]+)",\s*agent:\s*"([^"]+)"\s*\}'
    thoughts = re.findall(pattern, block[1])
    require(len(thoughts) == 3 and not re.sub(pattern, '', block[1]).strip(' ,\n\t'), "three attributed thoughts")
    require(all('I ' in t and len(t) < 140 and a.strip() for t, a in thoughts), "footer thought or attribution")


def static():
    md = (NOTE / "index.md").read_text()
    fields, body = frontmatter(md)
    count = prose_count(md)
    require(2500 <= count <= 2800, f"prose count {count}")
    estimate = f"{math.ceil(count/225)}-{math.ceil(count/200)} min"
    require(fields["reading_time"] == estimate, "reading_time estimate")
    pages = [NOTE / "index.html", NOTE / "evidence-notes/index.html"]
    for path in pages:
        text = path.read_text()
        page = Page(text)
        check_footer(page, text)
        ids = [attrs["id"] for _, attrs in page.elements if "id" in attrs]
        require(len(ids) == len(set(ids)), f"{path.name}: duplicate HTML id")
        for href in page.attrs("a", "href"):
            if href.startswith("#"):
                require(href[1:] in ids, f"{path.name}: missing chapter target {href}")
        for _, attrs in page.elements:
            for key in ("href", "src", "srcset"):
                if key in attrs:
                    local_link(path, attrs[key])
    text = pages[0].read_text()
    require(estimate.replace("-", "–") + " read" in text, "HTML reading time")
    content = text.split('<div class="post-content">', 1)[1].split('</article>', 1)[0]
    title = re.search(r"<h1>(.*?)</h1>", text)[1]
    opening = [re.search(fr'<p class="{kind}">(.*?)</p>', text)[1] for kind in ("standfirst", "coverage")]
    require(plain_md(body) == plain_html(" ".join([title, *opening, content])), "Markdown/HTML body parity")
    captions = re.findall(r"^\*(Figure .*?)\*$", body, re.M)
    rendered = re.findall(r"<figcaption>(.*?)</figcaption>", content, re.S)
    require(list(map(plain_md, captions)) == list(map(plain_html, rendered)), "caption parity")
    figures = Page(content)
    md_images = Page("\n".join(re.findall(r"^<img .*", body, re.M)))
    for attr in ("src", "alt"):
        require(md_images.attrs("img", attr) == figures.attrs("img", attr), f"{attr} parity")
    require(figures.attrs("ol", "class").count("timeline") == 1 and
            all(tag != "table" for tag, _ in figures.elements), "one primary HTML timeline and no article tables")
    require('<h2 id="chronology">Detailed chronology</h2>\n<table>' in pages[1].read_text(), "appendix chronology")
    # A heading literal proves nothing: deleting every data row still leaves it intact.
    # Compare the rendered rows against the source chronology cell by cell.
    source = (HERE.parent / "evidence-notes.md").read_text()
    chron = source.split("## Detailed chronology", 1)[-1]
    src_rows = []
    for line in chron.splitlines():
        if not line.startswith("|"):
            if src_rows:
                break
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells or cells[0] in ("Period", "") or set(cells[0]) <= {"-", ":", " "}:
            continue
        src_rows.append([plain_md(c) for c in cells])
    rendered_rows = []
    appendix = pages[1].read_text()
    table = re.search(r'<h2 id="chronology">.*?(<table>.*?</table>)', appendix, re.S)[1]
    for tr in re.findall(r"<tr>(.*?)</tr>", re.search(r"<tbody>(.*?)</tbody>", table, re.S)[1], re.S):
        cells = [plain_html(c) for c in re.findall(r"<td>(.*?)</td>", tr, re.S)]
        if cells:
            rendered_rows.append(cells)
    require(len(src_rows) == 11, f"source chronology has {len(src_rows)} rows, expected 11")
    require(rendered_rows == src_rows, "appendix chronology rows match the source")
    wide = ["figures/fig-2-control-loop.svg", "figures/fig-3-outcomes.svg"]
    mobile = [f.replace(".svg", "-mobile.svg") for f in wide]
    require(figures.attrs("img","src") == wide and figures.attrs("source","srcset") == mobile, "figure inventory")
    require(len(captions) == 2 and all(figures.attrs("img","alt")), "figure descriptions")
    linked_body = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', body)
    links = Page(linked_body).attrs("a", "href")
    require(links == figures.attrs("a","href"), "source link parity")
    fig3 = [captions[-1], figures.attrs("img","alt")[-1]]
    for filename in [wide[-1], mobile[-1]]:
        fig3.append((NOTE/filename).read_text())
    require(not re.search(r"(?<!\d)(?:810|518|1,?375)(?!\d)", " ".join(fig3)), "Figure 3 attempt token")
    dates = {u.findtext("{*}loc"):u.findtext("{*}lastmod") for u in ET.parse(ROOT/"sitemap.xml").getroot()}
    for url in (fields["canonical_url"], fields["canonical_url"]+"evidence-notes/"):
        require(dates.get(url) == "2026-11-19T23:25:57Z", f"sitemap date {url}")
    # Every local Markdown link that names this slug must resolve on disk.
    for doc in (ROOT/"CHANGELOG.md", NOTE/"index.md"):
        for link in re.findall(r"\[[^\]]+\]\(([^)#]+)\)", doc.read_text()):
            if link.startswith(("http://","https://","mailto:","#")) or SLUG not in link:
                continue
            target = (ROOT/link.lstrip("/")) if link.startswith("/") else (doc.parent/link).resolve()
            if target.is_dir():
                target /= "index.html"
            if not target.exists():
                raise ValueError(f"{doc.name}: missing local link {link}")
    print(f"PASS static: parity, {count} prose words, {estimate}, figures, frontmatter, sitemap, links, footers")


def guard():
    source = HERE.parent / "metrics.json"
    with tempfile.TemporaryDirectory(dir=HERE.parent) as tmp:
        scratch = Path(tmp) / source.name
        shutil.copyfile(source, scratch)
        fixture = json.loads(scratch.read_text())
        # Explicitly synthetic reconciled states; never infer a partition from the audit.
        fixture["attempts"].update(total=3, states={"example A": 1, "example B": 2})
        for allowed in (False, True):
            fixture["attempts"]["complete_composition_chart_allowed"] = allowed
            scratch.write_text(json.dumps(fixture))
            for unit in ("task", "attempt"):
                run = subprocess.run([sys.executable, str(HERE/"render_figures.py"), "--probe-metrics",
                                      str(scratch), "--unit", unit], capture_output=True, text=True)
                refusal = unit == "attempt" and not allowed
                require((run.returncode != 0 and "attempt partition refused" in run.stderr) if refusal
                        else run.returncode == 0, f"unexpected guard result: {run.stderr}")
                print(f"PASS guard allowed={allowed} unit={unit} exit={run.returncode}")
        shutil.copyfile(source, scratch)


def tiles(height):
    require(isinstance(height, int) and height > 0, "invalid scrollHeight")
    y = 0
    while True:
        size = min(3000, height-y)
        yield y, size
        if y+size == height:
            break
        y += size-200


def asset_failures(events, origin):
    urls, failures = {}, []
    for event in events:
        method, data = event.get("method"), event.get("params", {})
        rid = data.get("requestId")
        if method == "Network.requestWillBeSent":
            urls[rid] = data["request"]["url"]
        elif method == "Network.responseReceived":
            url, status = data["response"]["url"], data["response"]["status"]
            if status < 400:
                continue
        elif method == "Network.loadingFailed":
            url, status = urls.get(rid, ""), data["errorText"]
        else:
            continue
        if method != "Network.requestWillBeSent":
            scope = "local" if urlsplit(url).netloc == urlsplit(origin).netloc else "external"
            # Browser-cancelled requests (unmatched <picture> sources) and the absent favicon are
            # recorded for auditability but do not fail the page.
            fatal = not (status == "net::ERR_ABORTED" or urlsplit(url).path == "/favicon.ico")
            failures.append({"url": url, "status": status, "scope": scope, "fatal": fatal})
    return failures


def overflow(width, scroll_width):
    return scroll_width > width


def manifest_ok(row):
    keys = {"url","viewport","tile_index","y_offset","tile_height","file","scrollHeight","scrollWidth",
            "overflow","asset_failures","bound_check","dimensions"}
    if not keys <= row.keys():
        return False
    width, height = row["dimensions"]
    return (bool(row["file"]) and bool(urlsplit(row["url"]).hostname)
            and row["viewport"]["height"] > 0 and width > 0
            and row["overflow"] == overflow(row["viewport"]["width"], row["scrollWidth"])
            and row["tile_index"] >= 0 and 0 <= row["y_offset"] < row["scrollHeight"]
            and row["y_offset"] + height <= row["scrollHeight"]
            and row["bound_check"] and width == row["viewport"]["width"] <= LIMIT
            and 0 < height == row["tile_height"] <= 3000 and not row["overflow"]
            and not [f for f in row["asset_failures"] if f.get("scope") == "local" and f.get("fatal", True)])


def self_test():
    def coverage():
        for height in (1,200,2999,3000,3001,5800,8192,19570):
            plan = list(tiles(height))
            require(plan[0][0] == 0 and sum(plan[-1]) == height, "missing endpoint")
            require(all(0<h<=3000 and max(1440,h)<=LIMIT for _,h in plan), "tile bounds")
            require(all(0<b-a<=h-200 for (a,h),(b,_) in zip(plan,plan[1:])), "overlap")
    def assets():
        origin = "http://127.0.0.1:5555"
        events = [{"method":"Network.responseReceived","params":{"response":{"url":origin+"/x","status":404}}},
                  {"method":"Network.requestWillBeSent","params":{"requestId":"2","request":{"url":"https://example.org/x"}}},
                  {"method":"Network.loadingFailed","params":{"requestId":"2","errorText":"unavailable"}},
                  {"method":"Network.requestWillBeSent","params":{"requestId":"3","request":{"url":origin+"/fig-mobile.svg"}}},
                  {"method":"Network.loadingFailed","params":{"requestId":"3","errorText":"net::ERR_ABORTED"}}]
        require([(f["scope"],f["status"],f["fatal"]) for f in asset_failures(events,origin)] ==
                [("local",404,True),("external","unavailable",True),("local","net::ERR_ABORTED",False)],
                "asset classification")
    def widths():
        require(not overflow(390,390) and overflow(390,391), "overflow classification")
    def manifest():
        row = dict(url="http://localhost/note",viewport={"width":390,"height":900},tile_index=0,y_offset=0,
                   tile_height=500,file="tile.png",scrollHeight=500,scrollWidth=390,overflow=False,
                   asset_failures=[],bound_check=True,dimensions=[390,500])
        require(manifest_ok(row) and all(not manifest_ok({k:v for k,v in row.items() if k != key})
                                          for key in row), "manifest completeness")
    for name, test in (("tile coverage and bounds",coverage),("asset failures",assets),
                       ("overflow",widths),("manifest completeness",manifest)):
        try:
            test()
        except Exception:
            print("FAIL self-test", name)
            raise
        print("PASS self-test", name)


@contextmanager
def managed_process(argv, **kwargs):
    with subprocess.Popen(argv, **kwargs) as proc:
        try:
            yield proc
        finally:
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()


class Chromium:
    """DevTools JSON messages delimited by NUL on Chromium's fd 3 and 4."""
    def __init__(self, proc):
        self.proc = proc
        self.buffer = bytearray()
        self.sequence = 0
        self.events = []
        self.session = None

    def receive(self, deadline):
        while 0 not in self.buffer:
            remaining = deadline-time.monotonic()
            require(remaining > 0 and select.select([self.proc.stdout], [], [], remaining)[0],
                    "timed out waiting for Chromium")
            chunk = os.read(self.proc.stdout.fileno(), 65536)
            require(chunk, "Chromium closed the DevTools pipe")
            self.buffer.extend(chunk)
        end = self.buffer.index(0)
        message = json.loads(self.buffer[:end])
        del self.buffer[:end+1]
        if message.get("method") and self.session and message.get("sessionId") == self.session:
            self.events.append(message)
        return message

    def call(self, method, **params):
        self.sequence += 1
        request = {"id":self.sequence, "method":method, "params":params}
        if self.session:
            request["sessionId"] = self.session
        self.proc.stdin.write(json.dumps(request).encode()+b"\0")
        self.proc.stdin.flush()
        deadline = time.monotonic()+90
        while True:
            message = self.receive(deadline)
            if message.get("id") == self.sequence:
                require("error" not in message, f"{method}: {message.get('error')}")
                return message["result"]

    def evaluate(self, expression):
        reply = self.call("Runtime.evaluate", expression=expression, awaitPromise=True, returnByValue=True)
        require("exceptionDetails" not in reply, f"page evaluation: {reply.get('exceptionDetails')}")
        return reply["result"].get("value")


def capture_page(browser, url, width, directory, label, rows):
    height = 900
    if browser.session is None:
        target = browser.call("Target.createTarget", url="about:blank")["targetId"]
        browser.session = browser.call("Target.attachToTarget", targetId=target, flatten=True)["sessionId"]
        for domain in ("Page","Network","Runtime"):
            browser.call(domain+".enable")
        browser.call("Page.setLifecycleEventsEnabled", enabled=True)
        browser.call("Network.setCacheDisabled", cacheDisabled=True)
    browser.call("Emulation.setDeviceMetricsOverride", width=width, height=height, deviceScaleFactor=1, mobile=False)
    browser.events.clear()
    navigation = browser.call("Page.navigate", url=url)
    require("loaderId" in navigation and "errorText" not in navigation, f"navigation: {navigation}")
    deadline = time.monotonic()+60
    while browser.evaluate("document.readyState") not in ("interactive","complete"):
        require(time.monotonic() < deadline, "page did not reach an interactive readyState")
        time.sleep(0.25)
    browser.evaluate("""(async () => {
        for (const img of document.images) img.loading = 'eager';
        await Promise.all(Array.from(document.images, img => img.decode().catch(() => {})));
        await document.fonts.ready;
        await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
    })()""")
    measure = """({height:document.documentElement.scrollHeight, width:document.documentElement.scrollWidth,
                  viewport:innerWidth, broken:Array.from(document.images).filter(i => !i.naturalWidth)
                    .map(i => i.currentSrc || i.src)})"""
    geometry = browser.evaluate(measure)
    require(geometry["viewport"] == width, f"viewport mismatch: {geometry}")
    start = len(rows)
    for index, (y,size) in enumerate(tiles(geometry["height"])):
        browser.call("Emulation.setDeviceMetricsOverride", width=width, height=size,
                     deviceScaleFactor=1, mobile=False)
        browser.evaluate(f"window.scrollTo(0,{y})")
        browser.evaluate("new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))")
        shot = browser.call("Page.captureScreenshot", format="png", fromSurface=True)
        path = directory / f"{label}-{width}-{index:03d}.png"
        data = base64.b64decode(shot["data"], validate=True)
        require(data[:8] == b"\x89PNG\r\n\x1a\n" and data[12:16] == b"IHDR", "invalid screenshot")
        dimensions = struct.unpack(">II",data[16:24])
        path.write_bytes(data)
        rows.append(dict(url=url, viewport={"width":width,"height":size},tile_index=index,
                         y_offset=y,tile_height=size,file=str(path.relative_to(HERE)),scrollHeight=geometry["height"],
                         scrollWidth=geometry["width"],overflow=overflow(width,geometry["width"]),
                         asset_failures=[],dimensions=list(dimensions),
                         bound_check=dimensions == (width,size) and max(dimensions)<=LIMIT))
    browser.call("Emulation.setDeviceMetricsOverride", width=width, height=height,
                 deviceScaleFactor=1, mobile=False)
    final = browser.evaluate(measure)
    require(abs(final["height"]-geometry["height"]) <= 50 and final["width"] == geometry["width"],
            f"layout changed during capture: {geometry} -> {final}")
    failures = asset_failures(browser.events,url)
    for broken in geometry["broken"]:
        if not any(f["url"] == broken for f in failures):
            failures.append({"url":broken,"status":"image decode failed","scope":
                             "local" if urlsplit(broken).netloc == urlsplit(url).netloc else "external"})
    for row in rows[start:]:
        row["asset_failures"] = failures


def save_json(path, data):
    path.write_text(json.dumps(data,indent=2)+"\n")


def capture():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM):
            pass
    except PermissionError:
        print("CAPTURE_UNAVAILABLE reason=socket-denied")
        return 3
    directory = HERE/"render-evidence"
    if directory.exists():
        shutil.rmtree(directory)
    directory.mkdir()
    manifest = directory / "manifest.json"
    rows, errors = [], []
    completed = 0
    try:
        binary = next((shutil.which(b) for b in ("chromium","chromium-browser","google-chrome")
                       if shutil.which(b)), None)
        if not binary:
            cache = Path.home()/".cache/ms-playwright"
            binary = next((str(p) for p in sorted(cache.glob("chromium-*/chrome-linux*/chrome"),reverse=True)),None)
        require(binary, "no Chromium executable")
        with ExitStack() as stack:
            server = stack.enter_context(managed_process(
                [sys.executable,"-u","-m","http.server","0","--bind","127.0.0.1","--directory",str(ROOT)],
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True))
            line = server.stdout.readline()
            match = re.search(r"port (\d+)",line)
            require(match, f"HTTP server failed to announce port: {line}")
            origin = f"http://127.0.0.1:{match[1]}/notes/{SLUG}/"
            for label, page in (("note","index.html"), ("appendix","evidence-notes/index.html")):
                for width in (1440,390):
                    # A fresh browser per page: a long-lived renderer accumulates state and stalls
                    # after roughly a dozen full-height captures (measured 2026-11-21).
                    try:
                        with ExitStack() as inner:
                            profile = inner.enter_context(tempfile.TemporaryDirectory())
                            # Duplicate stdin/stdout onto the DevTools pipe descriptors before redirecting Chromium stdio.
                            proc = inner.enter_context(managed_process(
                                ["sh","-c",'exec "$@" 3<&0 4>&1 </dev/null >/dev/null',"chrome",binary,
                                 "--headless=new","--remote-debugging-pipe","--disable-gpu","--hide-scrollbars",
                                 "--no-sandbox","--disable-background-networking",
                                 "--host-resolver-rules=MAP * ~NOTFOUND,EXCLUDE 127.0.0.1",
                                 f"--user-data-dir={profile}","about:blank"],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE))
                            capture_page(Chromium(proc),origin+page,width,directory,label,rows)
                        completed += 1
                    except Exception as exc:
                        errors.append(f"{label}@{width}: {exc}")
    except Exception as exc:
        errors.append(str(exc))
    passed = sum(map(manifest_ok,rows))
    ok = completed == 4 and passed == len(rows) and not errors
    save_json(manifest,rows)
    save_json(HERE/"render-check.json",dict(result="PASS" if ok else "FAIL",completed_pages=completed,
              checked_tiles=len(rows),passed_tiles=passed,manifest=str(manifest.relative_to(HERE)),errors=errors))
    print(f"RESULT PASS {passed}/{len(rows)}" if ok else f"RESULT FAIL ({passed}/{len(rows)} tiles) {errors}")
    return 0 if ok else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for opt in ("static","guard","self-test","capture"):
        parser.add_argument("--"+opt, action="store_true")
    opts = parser.parse_args()
    default = not any(vars(opts).values())
    for enabled, phase in ((opts.static, static),(opts.guard,guard),(opts.self_test,self_test)):
        if default or enabled:
            phase()
    return capture() if default or opts.capture else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, IndexError) as error:
        sys.exit(f"RESULT FAIL: {error}")
