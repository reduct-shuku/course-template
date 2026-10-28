const debugPort = process.env.PPT_DEBUG_PORT || '9223';
const lessonUrl = process.env.PPT_LESSON_URL;
const slideIds = (process.env.PPT_SLIDE_IDS || '').split(',').map(id => id.trim()).filter(Boolean);
if (!lessonUrl || !slideIds.length) throw new Error('Set PPT_LESSON_URL and PPT_SLIDE_IDS.');


async function createTab(url) {
  const response = await fetch(`http://127.0.0.1:${debugPort}/json/new?${encodeURIComponent(url)}`, { method: 'PUT' });
  if (!response.ok) throw new Error(`Cannot create browser tab: ${response.status}`);
  return response.json();
}

async function auditSlide(id) {
  const urlObject = new URL(lessonUrl);
  urlObject.searchParams.set("slide", id);
  const url = urlObject.href;
  const tab = await createTab(url);
  const socket = new WebSocket(tab.webSocketDebuggerUrl);
  await new Promise((resolve, reject) => {
    socket.onopen = resolve;
    socket.onerror = reject;
  });

  let sequence = 0;
  const pending = new Map();
  socket.onmessage = (event) => {
    const message = JSON.parse(event.data);
    const resolve = pending.get(message.id);
    if (!resolve) return;
    pending.delete(message.id);
    resolve(message);
  };

  const send = (method, params = {}) => new Promise((resolve) => {
    const requestId = ++sequence;
    pending.set(requestId, resolve);
    socket.send(JSON.stringify({ id: requestId, method, params }));
  });

  await send('Runtime.enable');
  await send('Emulation.setDeviceMetricsOverride', {
    width: 1600,
    height: 900,
    deviceScaleFactor: 1,
    mobile: false,
  });
  await new Promise((resolve) => setTimeout(resolve, 800));
  const expression = `(() => {
    const surface = document.querySelector('.ppt-slide-surface, [data-slide-surface]');
    if (!surface) return { error: 'missing .ppt-slide-surface' };
    const surfaceRect = surface.getBoundingClientRect();
    const overflow = [];
    for (const element of surface.querySelectorAll('*')) {
      const rect = element.getBoundingClientRect();
      if (rect.width === 0 && rect.height === 0) continue;
      if (
        rect.left < surfaceRect.left - 0.5 ||
        rect.top < surfaceRect.top - 0.5 ||
        rect.right > surfaceRect.right + 0.5 ||
        rect.bottom > surfaceRect.bottom + 0.5
      ) {
        overflow.push({
          tag: element.tagName,
          className: String(element.className?.baseVal ?? element.className).slice(0, 80),
          left: +(rect.left - surfaceRect.left).toFixed(1),
          top: +(rect.top - surfaceRect.top).toFixed(1),
          right: +(rect.right - surfaceRect.right).toFixed(1),
          bottom: +(rect.bottom - surfaceRect.bottom).toFixed(1),
        });
      }
    }
    return {
      viewport: { width: innerWidth, height: innerHeight },
      surface: { width: surfaceRect.width, height: surfaceRect.height },
      scroll: { width: surface.scrollWidth, height: surface.scrollHeight },
      descendants: surface.querySelectorAll('*').length,
      overflowCount: overflow.length,
      overflow: overflow.slice(0, 12),
    };
  })()`;
  const response = await send('Runtime.evaluate', { expression, returnByValue: true });
  socket.close();
  return response.result.result.value ?? {
    error: response.result.exceptionDetails?.text ?? response.result.result.description ?? 'Evaluation failed',
  };
}

let failed = false;
for (const id of slideIds) {
  const result = await auditSlide(id);
  console.log(JSON.stringify({ id, ...result }));
  if (result.error || result.overflowCount > 0) failed = true;
}

if (failed) process.exitCode = 1;
