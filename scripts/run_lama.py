import torch, numpy as np
from PIL import Image
torch.set_grad_enabled(False)
model = torch.jit.load('/home/lbx/.cache/iopaint/models/big-lama.pt', map_location='cpu')
model.to('cuda').eval()
def inpaint(img_path, mask_path, out_path):
    src = Image.open(img_path).convert('RGB')
    mk = Image.open(mask_path).convert('L')
    w,h = src.size
    pw,ph = (8-w%8)%8, (8-h%8)%8
    img, mask = src, mk
    if pw or ph:
        img = Image.new('RGB',(w+pw,h+ph),(128,128,128)); img.paste(src,(0,0))
        mask = Image.new('L',(w+pw,h+ph),0); mask.paste(mk,(0,0))
    x = np.array(img).astype(np.float32)/127.5-1.0
    m = np.array(mask).astype(np.float32)
    m = (m>127.0).astype(np.float32)
    xt = torch.from_numpy(x.transpose(2,0,1)[None]).cuda()
    mt = torch.from_numpy(m[None,None]).cuda()
    out = model(xt,mt)
    if isinstance(out,(tuple,list)): out = out[0]
    out = out.clamp(-1,1)[0].cpu().numpy().transpose(1,2,0)
    res = Image.fromarray(((out+1)/2*255).astype(np.uint8))
    if pw or ph: res = res.crop((0,0,w,h))
    res.save(out_path)
    return res
for name in ['gap_noprompt','gap_correct','gap_wrong']:
    r = inpaint(f'/tmp/h2/{name}.png','/tmp/h2/gap_mask.png',f'/tmp/h2/{name}_out.png')
    print(name,'done',r.size)
