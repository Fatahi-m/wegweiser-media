const { chromium } = require('playwright');
const [S, ...ts] = process.argv.slice(2);
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
 await p.goto('file://' + S + '/stage.html'); await p.waitForTimeout(800);
 for (const t of ts) { await p.evaluate(t => render(+t), t); await p.waitForTimeout(50); await p.screenshot({ path: `${S}/f-${t}.png` }); }
 await b.close(); })();
