const { chromium } = require('playwright'); const [S, f, out] = process.argv.slice(2);
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
 await p.goto('file://' + S + '/' + f); await p.waitForTimeout(1200); await p.screenshot({ path: out, type: 'jpeg', quality: 95 }); await b.close(); })();
