const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const svg=fs.readFileSync('/home/user/sparbert/assets/logos/kaufland_footer.svg','utf8');
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:400},deviceScaleFactor:1});
await p.setContent(`<body style="margin:0;background:transparent"><div style="width:1200px;height:344px">${svg.replace('<svg ','<svg width="1200" height="344" ')}</div></body>`);
await p.locator('div').screenshot({path:'/home/user/sparbert/assets/logos/kaufland.png',omitBackground:true});await b.close()})();
