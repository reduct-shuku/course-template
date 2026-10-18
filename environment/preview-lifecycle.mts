import type { IncomingMessage, ServerResponse } from 'node:http';

interface PreviewServer {
  middlewares: { use: (handler: (request: IncomingMessage, response: ServerResponse, next: () => void) => void) => unknown };
  close: () => Promise<void>;
}

/** Loopback-only lifecycle API for the Node preview launcher. */
export function previewLifecycle(service: string) {
  return {
    name: 'preview-lifecycle',
    configureServer(server: PreviewServer) {
      server.middlewares.use((request, response, next) => {
        if (request.url === '/__preview/health') {
          response.setHeader('Content-Type', 'application/json');
          response.end(JSON.stringify({ ok: true, service, instance: process.env.COURSE_PREVIEW_INSTANCE || null }));
          return;
        }
        if (request.url !== '/__preview/stop') return next();
        if (request.method !== 'POST' || !process.env.COURSE_PREVIEW_TOKEN || request.headers['x-preview-token'] !== process.env.COURSE_PREVIEW_TOKEN) {
          response.statusCode = 403;
          response.end('Forbidden');
          return;
        }
        response.end('Stopping');
        setTimeout(() => { void server.close().finally(() => process.exit(0)); }, 100);
      });
    },
  };
}
