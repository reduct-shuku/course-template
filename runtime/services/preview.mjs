import { spawn } from 'node:child_process';
import { mkdir, open, readFile, writeFile, access } from 'node:fs/promises';
import { randomUUID, randomBytes } from 'node:crypto';
import { dirname, resolve, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const repository = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const args = process.argv.slice(2);
const option = (name, fallback) => args.includes(name) ? args[args.indexOf(name) + 1] : fallback;
const kind = option('--kind', 'frontend');
if (!['frontend', 'agent-demo'].includes(kind)) throw new Error('Unknown preview kind.');
const configDir = join(repository, 'environment', kind);
const stateFile = join(repository, 'runtime/data/services', `${kind}.json`);
let state = {};
try { state = JSON.parse(await readFile(stateFile, 'utf8')); } catch (error) { if (error.code !== 'ENOENT') throw error; }
const requestedPort = option('--port', undefined);
const port = Number(requestedPort || state.port || (kind === 'frontend' ? 5173 : 5183));
if (!Number.isInteger(port) || port < 1 || port > 65535) throw new Error('Invalid port.');
const base = `http://127.0.0.1:${port}`;
const expectedService = kind === 'frontend' ? 'course-preview' : 'web-agent-preview';
async function health() {
  try {
    const response = await fetch(`${base}/__preview/health`, { signal: AbortSignal.timeout(1000) });
    const data = await response.json();
    return data.service === expectedService ? data : null;
  } catch { return null; }
}
const current = await health();
if (args.includes('--status')) {
  console.log(`${kind}: ${current ? 'ready' : 'not running'} (${port})`);
} else if (args.includes('--stop')) {
  if (current && current.instance === state.instance && state.token) {
    const response = await fetch(`${base}/__preview/stop`, { method: 'POST', headers: { 'X-Preview-Token': state.token }, signal: AbortSignal.timeout(3000) });
    if (!response.ok) throw new Error(`Stop refused: ${response.status}`);
    for (let i = 0; i < 50 && await health(); i++) await new Promise(done => setTimeout(done, 100));
    if (await health()) throw new Error('Preview did not stop.');
    await writeFile(stateFile, '{}\n');
    console.log(`${kind}: stopped owned preview`);
  } else {
    console.log(`${kind}: no owned preview to stop`);
  }
} else if (current) {
  console.log(`${kind}: already ready at ${base}`);
} else {
  if (state.port && requestedPort && Number(state.port) !== port) {
    try {
      const other = await fetch(`http://127.0.0.1:${state.port}/__preview/health`, { signal: AbortSignal.timeout(1000) });
      if ((await other.json()).instance === state.instance) throw new Error('Stop the existing preview before changing its port.');
    } catch (error) { if (error.message.startsWith('Stop the existing')) throw error; }
  }
  const vite = join(configDir, 'node_modules/vite/bin/vite.js');
  try { await access(vite); } catch { throw new Error(`Run environment/install.ps1 -Kind ${kind} first.`); }
  await mkdir(dirname(stateFile), { recursive: true });
  const logDirectory = join(repository, 'runtime/data/logs');
  await mkdir(logDirectory, { recursive: true });
  const output = await open(join(logDirectory, `${kind}.log`), 'w');
  const instance = randomUUID();
  const token = randomBytes(32).toString('hex');
  const child = spawn(process.execPath, [vite, '--config', join(configDir, 'vite.config.ts'), '--host', '127.0.0.1', '--port', String(port), '--strictPort'], {
    cwd: configDir, detached: true, windowsHide: true,
    stdio: ['ignore', output.fd, output.fd],
    env: { ...process.env, COURSE_PREVIEW_INSTANCE: instance, COURSE_PREVIEW_TOKEN: token },
  });
  let spawnError;
  child.on('error', error => { spawnError = error; });
  child.unref();
  await output.close();
  await writeFile(stateFile, JSON.stringify({ pid: child.pid, port, instance, token }, null, 2) + '\n');
  let ready = false;
  for (let i = 0; i < 100; i++) {
    if (spawnError) throw spawnError;
    const result = await health();
    if (result?.instance === instance) { ready = true; break; }
    if (result || child.exitCode !== null) break;
    await new Promise(done => setTimeout(done, 250));
  }
  if (!ready) {
    child.kill();
    throw new Error(`Preview failed to start. See runtime/data/logs/${kind}.log`);
  }
  console.log(`${kind}: ready at ${base}`);
}
