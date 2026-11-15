const {chromium}=require('playwright');const fs=require('fs');(async()=>{const b=await chromium.launch();
const jobs=[['logo-ku.svg','Wegweiser-Logo-Kurdi.png','transparent',1],['logo-fa.svg','Wegweiser-Logo-Farsi.png','transparent',1],
['logo-ku.svg','Wegweiser-Profilbild-Kurdi.png','#ffffff',.94],['logo-fa.svg','Wegweiser-Profilbild-Farsi.png','#0e1f4d',.94]];
for(const [s,o,bg,sc] of jobs){const p=await b.newPage({viewport:{width:1080,height:1080}});
const svg=fs.readFileSync(s,'utf8').replace('<svg ',`<svg width="${1080*sc}" height="${1080*sc}" `);
await p.setContent(`<html><body style="margin:0;background:${bg};display:grid;place-items:center;width:1080px;height:1080px">${svg}</body></html>`);
await p.waitForTimeout(300);await p.screenshot({path:'/mnt/user-data/outputs/'+o,omitBackground:bg==='transparent'});await p.close();}
await b.close()})()
