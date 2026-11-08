const {chromium}=require('playwright');
(async()=>{
 const out=process.argv[2],fps=30,dur=34;
 const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
 await p.goto('file:///home/user/servicosdigitais/vsl/vsl.html');await p.waitForTimeout(500);
 for(let i=+(process.argv[3]||0);i<fps*dur;i++){await p.evaluate(t=>render(t),i/fps);await p.screenshot({path:`${out}/f${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:92});}
 await b.close();
})();
