const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
p.on('pageerror',e=>console.log('ERR',e.message));p.on('console',m=>{if(m.type()==='error')console.log('CON',m.text())});
await p.goto('file:///home/user/sparbert-zentrale/templates/offers.html?cap');await p.waitForFunction('window.ready',null,{timeout:20000});
await p.addStyleTag({content:'canvas{height:1920px!important;width:1080px!important;border-radius:0!important}#ui{display:none!important}'});
const ts=process.argv.slice(2).map(Number);
for(const t of ts){await p.evaluate(t=>window.render(t),t);await p.locator('#c').screenshot({path:`/tmp/h_${t}.jpg`,type:'jpeg',quality:88});}
console.log('DUR',await p.evaluate(()=>window.DUR));
await b.close()})();
