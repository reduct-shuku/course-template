import { previewLifecycle } from '../preview-lifecycle.mts';
import { defineConfig, loadEnv, type Plugin } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const configuration = path.dirname(fileURLToPath(import.meta.url));
const repository = path.resolve(configuration, '../..');
const frontend = path.join(repository, 'runtime/frontend');
const dependencies: Plugin = {
  name: 'environment-dependencies',
  async resolveId(source, importer) {
    if (!importer || importer.includes('/node_modules/') || importer.includes('\\node_modules\\') || source.startsWith('.') || source.startsWith('/') || source.startsWith('\0')) return null;
    return this.resolve(source, path.join(configuration, 'package.json'), { skipSelf: true });
  },
};

function cloudRuntime(): Plugin {
  const candidates = process.env.IDL_CLOUD_REPOSITORY
    ? [process.env.IDL_CLOUD_REPOSITORY]
    : [path.resolve(repository, '../cloud-intuitive-deep-learning'), path.resolve(repository, '..')];
  const cloud = candidates.find(candidate => fs.existsSync(path.join(candidate, 'frontend/cloud-runtime.js')));
  if (!cloud) throw new Error('Set IDL_CLOUD_REPOSITORY before enabling Cloud runtime.');
  return {
    name: 'optional-cloud-runtime', apply: 'serve',
    transformIndexHtml() { return [{ tag: 'script', attrs: { src: '/__cloud-runtime.js' }, injectTo: 'head-prepend' }]; },
    configureServer(server) {
      server.middlewares.use('/__cloud-runtime.js', (_request, response) => {
        response.setHeader('Content-Type', 'application/javascript');
        response.end(fs.readFileSync(path.join(cloud, 'frontend/cloud-runtime.js'), 'utf8'));
      });
    },
  };
}

function fixedLessonCanvas(): Plugin {
  return {
    name: 'fixed-lesson-canvas', enforce: 'pre',
    transform(source, id) {
      const file = id.split('?')[0].replaceAll('\\', '/');
      if (!/\/courses\/modules\/[^/]+\/pages\/.*\.css$/.test(file)) return null;
      const css = source.replace(/@media\s*\(\s*(max|min)-width\s*:\s*([^)]+)\)/g,
        (_, boundary: string, value: string) => `@container lesson-slide (${boundary}-width: ${value.trim()})`);
      if (/@media[^{}]*\b(?:width|height|orientation|aspect-ratio)\b/.test(css)) throw new Error(`Fixed lesson canvas cannot use viewport breakpoints: ${file}`);
      return css === source ? null : { code: css, map: null };
    },
  };
}

// Read the real authoring documents at build time; the slide needs no filesystem access.
function creatorSkillDocuments(): Plugin {
  const moduleId = 'virtual:creator-skill-documents';
  const resolvedId = `\0${moduleId}`;
  let directory: string;
  function markdownFiles(root: string): string[] {
    return fs.readdirSync(root, { withFileTypes: true }).flatMap(entry => {
      const file = path.join(root, entry.name);
      return entry.isDirectory() ? markdownFiles(file) : entry.name.endsWith('.md') ? [file] : [];
    });
  }
  return {
    name: 'creator-skill-documents',
    configResolved(config) { directory = path.resolve(config.root, '../../creater-skills'); },
    resolveId(id) { if (id === moduleId) return resolvedId; },
    load(id) {
      if (id !== resolvedId) return;
      const documents = markdownFiles(directory).map(file => {
        this.addWatchFile(file);
        return { path: path.relative(directory, file).replaceAll('\\', '/'), content: fs.readFileSync(file, 'utf8') };
      }).sort((a, b) => a.path === 'SKILL.md' ? -1 : b.path === 'SKILL.md' ? 1 : a.path.localeCompare(b.path));
      return `export default ${JSON.stringify(documents)};`;
    },
    configureServer(server) {
      server.watcher.add(directory);
      const refresh = (file: string) => {
        if (!file.startsWith(directory + path.sep) || !file.endsWith('.md')) return;
        const module = server.moduleGraph.getModuleById(resolvedId);
        if (module) {
          server.moduleGraph.invalidateModule(module);
          server.ws.send({ type: 'full-reload' });
        }
      };
      server.watcher.on('add', refresh).on('change', refresh).on('unlink', refresh);
    },
  };
}

function courseSources(): Plugin {
  return {
    name: 'course-sources',
    configureServer(server) {
      const courses = path.join(repository, 'courses/modules');
      server.watcher.add(courses);
      let timer: ReturnType<typeof setTimeout> | undefined;
      const refresh = (file: string) => {
        if (!path.resolve(file).startsWith(courses + path.sep)) return;
        clearTimeout(timer);
        timer = setTimeout(() => {
          server.moduleGraph.invalidateAll();
          server.ws.send({ type: 'full-reload' });
        }, 200);
      };
      server.watcher.on('add', refresh);
      server.watcher.on('unlink', refresh);
      server.httpServer?.on('close', () => clearTimeout(timer));
    },
  };
}

export default defineConfig(({ mode, command }) => {
  const env = loadEnv(mode, configuration, '');
  return {
    base: process.env.SHUKU_EXPORT === '1' ? './' : '/',
    define: { 'import.meta.env.VITE_SHUKU_EXPORT': JSON.stringify(process.env.SHUKU_EXPORT === '1') },
    root: frontend,
    envDir: configuration,
    cacheDir: path.join(repository, 'runtime/data/cache/vite'),
    publicDir: path.join(repository, 'courses/assets'),
    resolve: {
      alias: [
        { find: '@shared', replacement: path.join(repository, 'creater-skills/shared') },
        { find: /^react-dom(\/.*)?$/, replacement: path.join(configuration, 'node_modules/react-dom') + '$1' },
        { find: /^react(\/.*)?$/, replacement: path.join(configuration, 'node_modules/react') + '$1' },
        { find: 'three', replacement: path.join(configuration, 'node_modules/three') },
        { find: '@icon-park/react', replacement: path.join(configuration, 'node_modules/@icon-park/react') },
      ],
    },
    plugins: [creatorSkillDocuments(), previewLifecycle('course-preview'), courseSources(), dependencies, fixedLessonCanvas(), react({ exclude: /runtime[\\/]data[\\/]cache/ }), tailwindcss(), ...(command === 'serve' && env.VITE_USE_CLOUD_RUNTIME === 'true' ? [cloudRuntime()] : [])],
    build: {
      outDir: path.join(repository, 'runtime/data/build/frontend'), emptyOutDir: true,
      copyPublicDir: process.env.SHUKU_EXPORT === '1' || !env.VITE_ASSET_BASE_URL?.trim(),
      rollupOptions: { input: {
        app: path.join(frontend, 'index.html'),
        webPpt: path.join(frontend, 'web_ppt/index.html'),
        webPptSlide: path.join(frontend, 'web_ppt/slide.html'),
      } },
    },
    server: {
      host: '127.0.0.1', port: 5173, strictPort: true,
      fs: { allow: [repository] },
      proxy: {
        '/api': { target: process.env.IDL_LOCAL_API_URL || 'http://127.0.0.1:8000', changeOrigin: true },
        '/__telemetry': { target: 'http://127.0.0.1:59411', changeOrigin: true },
      },
    },
  };
});
