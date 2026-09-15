from PIL import Image, ImageDraw, ImageFont
import os

def load(p): return Image.open(p).convert("RGB")

src_bird = load("/home/lbx/relab-objrel/inputs/img1_crop512.png")
p1_bird  = load("/tmp/wingnew/h38/bird/h38_pass1.png")
best_bird= load("/tmp/wingnew/h38/bird/h38_best.png")

src_peac = load("/tmp/h2/peacock512.png")
p1_peac  = load("/tmp/wingnew/h38/peacock/h38_pass1.png")
best_peac= load("/tmp/wingnew/h38/peacock/h38_best.png")

cell=512; label_h=46
def cell_with(img, title, sub):
    canvas=Image.new("RGB",(cell,label_h+cell),(20,20,20))
    canvas.paste(img.resize((cell,cell)),(0,label_h))
    d=ImageDraw.Draw(canvas)
    try:
        f1=ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",18)
        f2=ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf",15)
    except:
        f1=f2=None
    d.text((10,6),title,fill=(255,255,120),font=f1)
    d.text((10,26),sub,fill=(200,255,200),font=f2)
    return canvas

row1=[
 cell_with(src_bird,"A bird: SOURCE","SP=bird perching on bamboo"),
 cell_with(p1_bird,"A bird: pass1 (base)","prot MAE=10.66"),
 cell_with(best_bird,"A bird: h38 best a=1.5","prot MAE=6.97  (<7.4 WIN)"),
]
row2=[
 cell_with(src_peac,"B peacock: SOURCE/GT","SP=TP=a peacock"),
 cell_with(p1_peac,"B peacock: pass1","gap MAE=42.59"),
 cell_with(best_peac,"B peacock: h38 best a=1.0","prot MAE=6.73 (gap 42.8)"),
]
W=cell*3; H=label_h+cell
out=Image.new("RGB",(W,H*2),(0,0,0))
for i,c in enumerate(row1): out.paste(c,(i*cell,0))
for i,c in enumerate(row2): out.paste(c,(i*cell,H))
out.save("/tmp/wingnew/h38/h38_compare.png")
print("saved /tmp/wingnew/h38/h38_compare.png", out.size)
