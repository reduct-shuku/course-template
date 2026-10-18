import { previewLifecycle } from '../preview-lifecycle.mts';
import { defineConfig, type Plugin } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const configuration = path.dirname(fileURLToPath(import.meta.url));
const repository = path.resolve(configuration, '../..');
const dependencies: Plugin = {
  name: 'environment-dependencies',
  async resolveId(source, importer) {
    if (!importer || importer.includes('/node_modules/') || importer.includes('\\node_modules\\') || source.startsWith('.') || source.startsWith('/') || source.startsWith('\0')) return null;
    return this.resolve(source, path.join(configuration, 'package.json'), { skipSelf: true });
  },
};
export default defineConfig({
  root: path.join(repository, 'creater-skills/demos/web-agent'),
  envDir: configuration,
  cacheDir: path.join(repository, 'runtime/data/cache/agent-demo'),
  resolve: { alias: [
    { find: /^react-dom(\/.*)?$/, replacement: path.join(configuration, 'node_modules/react-dom') + '$1' },
    { find: /^react(\/.*)?$/, replacement: path.join(configuration, 'node_modules/react') + '$1' },
  ] },
  plugins: [previewLifecycle('web-agent-preview'), dependencies, react()],
  server: { host: '127.0.0.1', port: 5183, strictPort: true, fs: { allow: [repository] } },
  build: { outDir: path.join(repository, 'runtime/data/build/agent-demo'), emptyOutDir: true, chunkSizeWarningLimit: 1500 },
});
