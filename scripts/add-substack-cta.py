#!/usr/bin/env python3
"""
Add Substack CTA to all note HTML files
"""
import os
import re

def add_substack_cta(file_path):
    """Add Substack CTA section before the footer in an HTML file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has Substack CTA
    if 'substack-cta' in content:
        print(f"✓ {file_path} already has Substack CTA")
        return False
    
    # 1. Add CSS link in head (after footer.css)
    css_pattern = r'(<link rel="stylesheet" href="/styles/footer\.css">)'
    css_replacement = r'\1\n    <link rel="stylesheet" href="/styles/substack-cta.css">'
    content = re.sub(css_pattern, css_replacement, content)
    
    # 2. Add Substack CTA section before footer
    # Try two patterns: one where footer is inside main, one where it's outside
    
    # Pattern 1: footer inside main (after </article>)
    cta_html_inside = '''        </article>

        <section class="substack-cta">
          <h3>Stay Updated</h3>
          <p>Get notified about new research notes and insights on AI-native engineering.</p>
          <div id="substack-cta-container" data-substack-url="rmax.substack.com"></div>
        </section>
      </main>

      <footer class="rmax-footer">'''
    
    footer_pattern_inside = r'(</article>)\s*</main>\s*<footer class="rmax-footer">'
    
    # Pattern 2: footer outside main/wrap (after </main> and </div>)
    cta_html_outside = '''        </article>

        <section class="substack-cta">
          <h3>Stay Updated</h3>
          <p>Get notified about new research notes and insights on AI-native engineering.</p>
          <div id="substack-cta-container" data-substack-url="rmax.substack.com"></div>
        </section>
      </main>

    </div>
    <footer class="rmax-footer">'''
    
    footer_pattern_outside = r'(</article>)\s*</main>\s*</div>\s*<footer class="rmax-footer">'
    
    # Try pattern 1 first
    new_content = re.sub(footer_pattern_inside, cta_html_inside, content)
    if new_content == content:
        # Pattern 1 didn't match, try pattern 2
        new_content = re.sub(footer_pattern_outside, cta_html_outside, content)
    
    content = new_content
    
    # 3. Add script reference before </body>
    script_pattern = r'(<script src="/scripts/analytics-tracking\.js"></script>)'
    script_replacement = r'\1\n    <script src="/scripts/substack-cta.js"></script>'
    content = re.sub(script_pattern, script_replacement, content)
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Updated {file_path}")
    return True

def main():
    # Determine notes directory relative to repository root, with optional override
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    notes_dir = os.environ.get("NOTES_DIR", os.path.join(repo_root, "notes"))
    
    # Find all index.html files in note directories (exclude notes/index.html itself)
    updated = 0
    for root, dirs, files in os.walk(notes_dir):
        if 'index.html' in files:
            file_path = os.path.join(root, 'index.html')
            # Skip the main notes index
            if file_path == os.path.join(notes_dir, 'index.html'):
                continue
            
            if add_substack_cta(file_path):
                updated += 1
    
    print(f"\n✓ Updated {updated} files")

if __name__ == '__main__':
    main()
