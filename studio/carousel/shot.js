const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:1});
await p.goto('file://'+process.cwd()+'/index.html');await p.waitForTimeout(800);
const n=await p.$$eval('section',a=>a.length);
for(let i=1;i<=n;i++){const el=await p.$('#s'+i);const r=await el.evaluate(e=>{const b=e.querySelector('.body');return b.scrollHeight>b.clientHeight+2?'OVERFLOW':''});if(r)console.log(i,r);await el.screenshot({path:`slide-${String(i).padStart(2,'0')}.png`});}
await b.close()})()
