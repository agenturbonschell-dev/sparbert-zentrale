const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const svg=fs.readFileSync('/home/user/sparbert/assets/logos/logo.svg','utf8');
const b=await chromium.launch();const p=await b.newPage({viewport:{width:600,height:600}});
await p.setContent(`<body style="margin:0;background:transparent">${svg.replace('width="60" height="60"','width="600" height="600"')}</body>`);
await p.screenshot({path:'/home/user/sparbert/assets/logos/lidl.png',omitBackground:true,clip:{x:0,y:0,width:600,height:600}});await b.close()})();
