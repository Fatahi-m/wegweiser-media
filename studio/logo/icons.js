const {chromium}=require('playwright');const fs=require('fs');const W=process.argv[2];(async()=>{const b=await chromium.launch();
const bgc={fa:'#0e1f4d',ku:'#ffffff'};
const jobs=[];for(const l of ['fa','ku']){jobs.push([l,`${l}-192.png`,192,'transparent',1],[l,`${l}-512.png`,512,'transparent',1],[l,`${l}-apple.png`,180,bgc[l],.9],[l,`${l}-mask-192.png`,192,bgc[l],.8],[l,`${l}-mask-512.png`,512,bgc[l],.8]);}
for(const [l,o,sz,bg,sc] of jobs){const p=await b.newPage({viewport:{width:sz,height:sz}});
const svg=fs.readFileSync(`logo-${l}.svg`,'utf8').replace('<svg ',`<svg width="${sz*sc}" height="${sz*sc}" `);
await p.setContent(`<html><body style="margin:0;background:${bg};display:grid;place-items:center;width:${sz}px;height:${sz}px">${svg}</body></html>`);
await p.screenshot({path:`${W}/public/icons/${o}`,omitBackground:bg==='transparent'});await p.close();}
await b.close()})()
