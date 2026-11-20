// Render contoh Remotion ke contoh/remotion/out.mp4
// Jika Remotion gagal memuat turun pelayarnya sendiri, set REMOTION_BROWSER ke Chrome/Chromium tempatan.
import {bundle} from '@remotion/bundler';
import {selectComposition, renderMedia} from '@remotion/renderer';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const dir = path.dirname(fileURLToPath(import.meta.url));
const browserExecutable = process.env.REMOTION_BROWSER || undefined;
const serveUrl = await bundle({entryPoint: path.join(dir, 'src/index.jsx')});
const composition = await selectComposition({serveUrl, id: 'Tajuk', browserExecutable});
const outputLocation = path.join(dir, 'out.mp4');
await renderMedia({serveUrl, composition, codec: 'h264', outputLocation, concurrency: 2, browserExecutable});
console.log('Siap:', outputLocation);
