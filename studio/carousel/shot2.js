const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.cwd()+'/story.html');await p.waitForTimeout(800);
for(let i=1;i<=6;i++){const el=await p.$('#s'+i);const r=await el.evaluate(e=>{const b=e.querySelector('.body');return b.scrollHeight>b.clientHeight+2});if(r)console.log('OVERFLOW',i);await el.screenshot({path:`story-${i}.png`});}
await b.close()})()
