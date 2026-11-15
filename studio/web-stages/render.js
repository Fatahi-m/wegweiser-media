// node render.js S from to out.mp4 scJSON
const { chromium } = require('playwright'); const { spawn } = require('child_process');
const [S, a, b, out, sc] = process.argv.slice(2); const FPS = 30;
(async () => { const br = await chromium.launch(); const p = await br.newPage({ viewport: { width: 1080, height: 1920 } });
 await p.goto('file://' + S + '/' + (process.env.STAGE||'stage.html')); await p.evaluate(sc => { window.SC = JSON.parse(sc); }, sc); await p.waitForTimeout(1000);
 const ff = spawn('ffmpeg', ['-loglevel','error','-y','-f','image2pipe','-framerate',String(FPS),'-c:v','mjpeg','-i','-','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p',out]);
 for (let f = Math.round(a*FPS); f < Math.round(b*FPS); f++) { await p.evaluate(t => render(t), f / FPS); const buf = await p.screenshot({ type: 'jpeg', quality: 92, timeout: 180000 }); if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r)); }
 ff.stdin.end(); await new Promise(r => ff.on('close', r)); await br.close(); })();
