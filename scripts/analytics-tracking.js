// Simple Analytics wiring. Keep event names aligned with analytics-events.md.
(function () {
  const eventQueue = [];
  const downloadExtensions = [
    '.pdf',
    '.zip',
    '.gz',
    '.tar',
    '.csv',
    '.tsv',
    '.xlsx',
    '.xls',
    '.pptx',
    '.ppt',
    '.docx',
    '.doc',
    '.png',
    '.jpg',
    '.jpeg',
    '.svg',
  ];

  const flushQueue = () => {
    if (typeof window.sa_event !== 'function') {
      return;
    }
    while (eventQueue.length) {
      const { name, metadata } = eventQueue.shift();
      window.sa_event(name, metadata);
    }
  };

  const queueInterval = setInterval(() => {
    if (typeof window.sa_event === 'function') {
      flushQueue();
      clearInterval(queueInterval);
    }
  }, 250);

  const sendEvent = (name, metadata = {}) => {
    if (!name) {
      return;
    }
    const payload = { ...metadata };
    if (typeof window.sa_event === 'function') {
      window.sa_event(name, payload);
      return;
    }
    eventQueue.push({ name, metadata: payload });
  };

  const buildMetadataFromDataset = (dataset) => {
    const meta = {};
    if (dataset.simpleNavItem) meta.item = dataset.simpleNavItem;
    if (dataset.simpleOutboundHost) meta.host = dataset.simpleOutboundHost;
    if (dataset.simpleCtaId) meta.cta_id = dataset.simpleCtaId;
    if (dataset.simpleContactEmailAddress) meta.email = dataset.simpleContactEmailAddress;
    if (dataset.simpleDownloadFile) meta.file = dataset.simpleDownloadFile;
    if (dataset.simpleDownloadType) meta.type = dataset.simpleDownloadType;
    if (dataset.simpleEventContext) meta.context = dataset.simpleEventContext;
    return meta;
  };

  const trackByDataset = (link) => {
    const eventName = link.dataset.simpleEvent;
    if (!eventName) {
      return false;
    }
    if (link.dataset.simpleEventTracked) {
      return true;
    }
    const metadata = buildMetadataFromDataset(link.dataset);
    sendEvent(eventName, metadata);
    link.dataset.simpleEventTracked = 'true';
    return true;
  };

  const normalizeHost = (hostname) => hostname.replace(/^www\./, '').toLowerCase();

  const isDownloadLink = (url) => {
    const lower = url.pathname.toLowerCase();
    return downloadExtensions.some((ext) => lower.endsWith(ext));
  };

  const autoTrackLink = (link) => {
    if (link.dataset.simpleEvent || link.dataset.simpleAutoTracked) {
      return;
    }
    const href = link.getAttribute('href') || '';
    if (!href || href.startsWith('#') || href.startsWith('javascript:')) {
      return;
    }
    if (href.startsWith('mailto:')) {
      const email = href.replace(/^mailto:/, '').split('?')[0];
      sendEvent('click_contact_email', { email });
      link.dataset.simpleAutoTracked = 'contact';
      return;
    }
    try {
      const url = new URL(href, window.location.origin);
      if (isDownloadLink(url)) {
        sendEvent('download_asset', {
          file: `${url.pathname}${url.search || ''}`,
          type: url.pathname.split('.').pop().toLowerCase(),
        });
        link.dataset.simpleAutoTracked = 'download';
        return;
      }
      if (normalizeHost(url.hostname) !== normalizeHost(window.location.hostname)) {
        sendEvent('click_outbound', {
          host: normalizeHost(url.hostname),
        });
        link.dataset.simpleAutoTracked = 'outbound';
      }
    } catch (error) {
      // Ignore invalid URLs
    }
  };

  document.addEventListener('click', (event) => {
    const link = event.target.closest('a');
    if (!link) {
      return;
    }
    if (trackByDataset(link)) {
      return;
    }
    autoTrackLink(link);
  });

  flushQueue();
})();
