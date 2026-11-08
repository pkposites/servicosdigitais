import subprocess, os, sys
from PIL import Image, ImageDraw, ImageFont
REPO="/home/user/servicosdigitais"
OUT=REPO+"/assets/reels"
TMP="/tmp/claude-0/-home-user-servicosdigitais/437cbdf0-084d-526e-ad9a-398cdf28f1c1/scratchpad/build"
os.makedirs(OUT,exist_ok=True)
W,H=1080,1920
FB="/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
FM="/usr/share/fonts/opentype/inter/Inter-Medium.otf"
FS="/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
def font(p,s): return ImageFont.truetype(p,s)
def hexc(h): return tuple(int(h[i:i+2],16) for i in (1,3,5))

def bg(c1,c2,accent):
    im=Image.new("RGB",(W,H),c1)
    px=im.load()
    top,bot=hexc(c1),hexc(c2)
    d=ImageDraw.Draw(im)
    for y in range(H):
        t=y/H
        d.line([(0,y),(W,y)],fill=tuple(int(top[i]+(bot[i]-top[i])*t) for i in range(3)))
    # soft glow
    glow=Image.new("RGB",(W,H),(0,0,0))
    g=ImageDraw.Draw(glow)
    a=hexc(accent)
    g.ellipse([W//2-520,H//2-300,W//2+520,H//2+740],fill=tuple(int(x*0.22) for x in a))
    from PIL import ImageFilter, ImageChops
    glow=glow.filter(ImageFilter.GaussianBlur(160))
    return ImageChops.add(im,glow)

def wrap(d,text,f,maxw):
    words=text.split();lines=[];cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if d.textlength(t,font=f)<=maxw: cur=t
        else: lines.append(cur);cur=w
    lines.append(cur);return lines

def text_block(d,text,f,x,y,maxw,fill,lh=1.12):
    lines=wrap(d,text,f,maxw)
    for l in lines:
        d.text((x,y),l,font=f,fill=fill);y+=int(f.size*lh)
    return y

def brand(d,accent):
    d.text((70,440),"RDA",font=font(FB,46),fill=accent)
    d.text((70+d.textlength("RDA ",font=font(FB,46)),440),"Serviços Digitais",font=font(FM,46),fill="#F4F4F6")

def scene_text(cfg,title,sub,name,hl=None):
    im=bg(cfg["c1"],cfg["c2"],cfg["accent"]);d=ImageDraw.Draw(im)
    brand(d,cfg["accent"])
    y=text_block(d,title,font(FB,104),70,600,940,"#FFFFFF",1.08)
    if sub: text_block(d,sub,font(FM,52),70,y+40,900,"#D5D7E0",1.25)
    im.save(f"{TMP}/{cfg['key']}_{name}.png")

def scene_art(cfg,box,name):
    im=bg(cfg["c1"],cfg["c2"],cfg["accent"]);d=ImageDraw.Draw(im)
    brand(d,cfg["accent"])
    art=Image.open(f"{REPO}/assets/ads/ad-{cfg['slug']}.webp").convert("RGB").crop(box)
    s=980/art.width;art=art.resize((980,int(art.height*s)),Image.LANCZOS)
    y0=540+(900-art.height)//2
    m=Image.new("L",art.size,0);ImageDraw.Draw(m).rounded_rectangle([0,0,art.width,art.height],36,fill=255)
    im.paste(art,(50,y0),m)
    im.save(f"{TMP}/{cfg['key']}_{name}.png")

def scene_list(cfg,title,items,name):
    im=bg(cfg["c1"],cfg["c2"],cfg["accent"]);d=ImageDraw.Draw(im)
    brand(d,cfg["accent"])
    y=text_block(d,title,font(FB,84),70,600,940,"#FFFFFF",1.1)+50
    for it in items:
        d.rounded_rectangle([70,y,1010,y+130],28,fill=(20,22,38),outline=cfg["accent"],width=3)
        d.ellipse([100,y+35,160,y+95],fill=cfg["accent"])
        d.line([(115,y+66),(128,y+78),(148,y+52)],fill="#0A0A12",width=7)
        d.text((190,y+38),it,font=font(FS,50),fill="#FFFFFF")
        y+=160
    im.save(f"{TMP}/{cfg['key']}_{name}.png")

def scene_cta(cfg,line1,name):
    im=bg(cfg["c1"],cfg["c2"],cfg["accent"]);d=ImageDraw.Draw(im)
    brand(d,cfg["accent"])
    y=text_block(d,line1,font(FB,96),70,640,940,"#FFFFFF",1.08)+70
    d.rounded_rectangle([70,y,1010,y+170],85,fill=cfg["accent"])
    f=font(FB,62);t="Peça seu orçamento";w=d.textlength(t,font=f)
    d.text(((W-w)/2,y+52),t,font=f,fill="#0A0A12")
    text_block(d,"Preencha o formulário e fale com a gente no WhatsApp.",font(FM,44),70,y+230,900,"#D5D7E0",1.25)
    im.save(f"{TMP}/{cfg['key']}_{name}.png")

CFG=[
 dict(key="bio",slug="pagina-bio",c1="#0D0F1F",c2="#1B1630",accent="#FBBF24",crop=(0,540,1122,1310),
  hook=("Seu Instagram tem seguidores, mas falta um lugar que mostre tudo?","Falta onde mandar quem chega no seu perfil."),
  sol=("Uma página só sua, na bio.","Serviços, trabalhos e botão de WhatsApp em um só link."),
  items=["Página personalizada","Seus serviços e trabalhos","Botão direto pro WhatsApp"],
  cta="Seu negócio inteiro na bio."),
 dict(key="lp",slug="landing-page",c1="#0A0920",c2="#1A1236",accent="#A78BFA",crop=(0,545,1122,1320),
  hook=("Vai anunciar uma oferta e não tem uma página pra ela?","Mandar o cliente pro perfil ou pro WhatsApp frio perde contatos."),
  sol=("Uma página para a sua oferta.","Apresenta o serviço, responde as dúvidas e leva ao WhatsApp."),
  items=["Apresenta seu serviço","Responde as dúvidas","Leva o cliente ao WhatsApp"],
  cta="Uma página para a sua oferta."),
 dict(key="setup",slug="configuracao-anuncios",c1="#050A14",c2="#06231C",accent="#34D77B",crop=(0,740,1122,1170),
  hook=("Quer anunciar e não sabe por onde começar?","Conta, campanha, pixel, eventos… dá pra travar fácil."),
  sol=("A gente configura pra você.","Sua conta de anúncios e suas campanhas, com teste no final."),
  items=["Estrutura da campanha","Eventos de conversão","Rastreamento testado"],
  cta="Anuncie sem travar na configuração."),
 dict(key="artes",slug="artes-e-videos",c1="#050A14",c2="#06231C",accent="#34D77B",crop=(60,500,1070,1260),
  hook=("Precisa de criativos pra anunciar e não sabe criar?","Anúncio sem boa arte nem vídeo passa batido."),
  sol=("A gente cria suas artes e vídeos.","Criativos feitos para divulgar a sua oferta."),
  items=["Artes para feed e stories","Vídeos curtos (Reels)","Prontos para anunciar"],
  cta="Artes e vídeos para anunciar."),
]
DUR=[3.6,3.6,4.2,3.6,3.6]; XF=0.5
for c in CFG:
    scene_text(c,*c["hook"],"s1")
    scene_text(c,*c["sol"],"s2")
    scene_art(c,c["crop"],"s3")
    scene_list(c,"O que você recebe",c["items"],"s4")
    scene_cta(c,c["cta"],"s5")
    ins=[];fc=[]
    for i,d in enumerate(DUR):
        n=d+XF
        ins+=["-framerate","30","-loop","1","-t",f"{n}","-i",f"{TMP}/{c['key']}_s{i+1}.png"]
        fc.append(f"[{i}:v]setpts=PTS-STARTPTS,scale=w='trunc(1080*(1+0.05*t/{n})/2)*2':h='trunc(1920*(1+0.05*t/{n})/2)*2':eval=frame,crop=1080:1920,fps=30,format=yuv420p,setsar=1[v{i}]")
    # xfade chain
    chain="[v0]";off=0
    for i in range(1,5):
        off+=DUR[i-1]
        chain+=f"[v{i}]xfade=transition=fade:duration={XF}:offset={off}"+("[x%d];[x%d]"%(i,i) if i<4 else "[out]")
    fcs=";".join(fc)+";"+chain
    outp=f"{OUT}/reel-{c['key']}.mp4"
    cmd=["ffmpeg","-y","-loglevel","error",*ins,"-filter_complex",fcs,"-map","[out]","-t",f"{sum(DUR)}",
         "-c:v","libx264","-preset","medium","-crf","20","-pix_fmt","yuv420p","-movflags","+faststart","-r","30",outp]
    subprocess.run(cmd,check=True);print("ok",outp)
