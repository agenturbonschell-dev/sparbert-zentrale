const {chromium}=require('playwright');const {spawn}=require('child_process');
const [,,url,start,end,out,ss]=process.argv;
(async()=>{
const b=await chromium.launch();
const ctx=await b.newContext({viewport:{width:1080,height:1920},deviceScaleFactor:+ss});
const p=await ctx.newPage();
await p.goto(`${url}?cap&ss=${ss}`);await p.waitForFunction('window.ready',null,{timeout:60000});
await p.addStyleTag({content:'canvas{height:1920px!important;width:1080px!important;border-radius:0!important}#ui{display:none!important}'});
const ff=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-','-vf','scale=1080:1920:flags=lanczos','-c:v','libx264','-crf','12','-preset','medium','-pix_fmt','yuv420p',out],{stdio:['pipe','inherit','inherit']});
for(let i=+start;i<+end;i++){
  await p.evaluate(t=>window.render(t),i/30);
  const buf=await p.locator('#c').screenshot({type:'jpeg',quality:94});
  if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));
}
ff.stdin.end();await new Promise(r=>ff.on('close',r));await b.close();
})();
