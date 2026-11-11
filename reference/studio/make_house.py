"""Opening photo: Pexels #210617 (free license) + a composited red FOR SALE yard sign on the existing post."""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import random
src = Image.open('cap/pexels-210617.jpg').convert('RGB')
im = src.copy(); W, H = im.size
d = ImageDraw.Draw(im)
# sample the post's wood colour
wood = src.getpixel((1385, 1700)); wood_dark = tuple(max(0, c - 35) for c in wood)
print('wood', wood)
# extend the arm left (existing arm ~ y 1452-1478, x 1215-1440)
ay0, ay1 = 1450, 1482; ax0 = 880
d.rectangle((ax0, ay0, 1300, ay1), fill=wood); d.rectangle((ax0, ay1 - 6, 1300, ay1), fill=wood_dark)
d.rectangle((ax0, ay0, ax0 + 10, ay1), fill=wood_dark)
# sign panel
sx0, sy0, sx1, sy1 = 915, 1500, 1357, 1815
for x in (sx0 + 60, sx1 - 60):  # hooks
    d.line([(x, ay1), (x, sy0)], fill=(70, 70, 72), width=6)
shadow = Image.new('L', (W, H), 0); ImageDraw.Draw(shadow).rectangle((sx0 + 18, sy0 + 22, sx1 + 18, sy1 + 22), fill=110)
im = Image.composite(Image.new('RGB', (W, H), (0, 0, 0)), im, shadow.filter(ImageFilter.GaussianBlur(14)))
d = ImageDraw.Draw(im)
d.rectangle((sx0, sy0, sx1, sy1), fill=(244, 244, 240))
d.rectangle((sx0 + 16, sy0 + 16, sx1 - 16, sy1 - 16), fill=(206, 32, 38))
f = ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-Black.otf', 118)
for i, t in enumerate(['FOR', 'SALE']):
    w = d.textlength(t, font=f); d.text(((sx0 + sx1) / 2 - w / 2, sy0 + 28 + i * 128), t, font=f, fill=(250, 250, 248))
# sunlight from upper-left: gentle gradient across the panel
light = Image.new('L', (W, H), 0); ld = ImageDraw.Draw(light)
for y in range(sy0, sy1 + 1):
    ld.line([(sx0, y), (sx1, y)], fill=int(26 * (1 - (y - sy0) / (sy1 - sy0))))
im = Image.composite(Image.new('RGB', (W, H), (255, 252, 240)), im, light)
# match photo softness + grain inside the sign region
box = (ax0 - 10, ay0 - 10, sx1 + 40, sy1 + 40)
reg = im.crop(box).filter(ImageFilter.GaussianBlur(1.1))
px = reg.load(); random.seed(1)
for y in range(reg.height):
    for x in range(reg.width):
        n = random.randint(-6, 6); r, g, b = px[x, y]; px[x, y] = (max(0, min(255, r + n)), max(0, min(255, g + n)), max(0, min(255, b + n)))
im.paste(reg, box)
im.save('cap/house.jpg', quality=95)
im.crop((600, 1100, 1900, 2300)).resize((650, 600)).save('shots/sign_check.jpg', quality=88)
