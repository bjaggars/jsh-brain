"""A1 · iOS App Preview — "The Road Warrior" (25s, 886x1920, 30 fps).
Real MRV footage (TEST film-set tenant) inside a branded frame. Videos-as-code: rerun after any UI change."""
import json, math, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS, DUR = 886, 1920, 30, 25.0
GREEN, GREEN_D = (40, 64, 46), (27, 44, 32)
CREAM, BRASS = (243, 241, 230), (212, 175, 92)
IW, IH = 652, 1413                      # phone inset (0.736 of a 886x1920 capture)
IX, IY = (W - IW) // 2, 452
RAD = 46
CAP = 'cap/'
F = '/usr/share/fonts/opentype/inter/'
font = lambda w, s: ImageFont.truetype(F + f'InterDisplay-{w}.otf', s)

shots = {n: Image.open(CAP + n + '.jpg').convert('RGB') for n in
         ['a_home', 'b_calendar', 'c_showings', 'd_receipt', 'f_closings', 'g_colors', 'h_gold', 'i_dark']}
taps = json.load(open(CAP + 'taps.json'))
SW, SH = shots['a_home'].size            # 886x1920 (443x960 css @2x)

def ease(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def ease_out(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3

# ---- screen timeline: (start, end, shot, zoom0, zoom1, focus_xy_in_shot_px, zoom_delay)
SEG = [
    (0.0, 4.0, 'a_home', 1.00, 1.035, (443, 900), 0.0),
    (4.0, 5.7, 'b_calendar', 1.0, 1.0, (443, 960), 0.0),
    (5.7, 8.2, 'c_showings', 1.0, 1.06, (443, 700), 0.3),
    (8.2, 11.2, 'd_receipt', 1.0, 1.12, (443, 640), 0.2),
    (11.2, 15.6, 'f_closings', 1.0, 1.10, (443, 620), 0.5),
    (15.6, 17.3, 'g_colors', 1.0, 1.0, (443, 960), 0.0),
    (17.3, 18.9, 'h_gold', 1.0, 1.0, (443, 960), 0.0),
    (18.9, 21.0, 'i_dark', 1.0, 1.0, (443, 960), 0.0),
]
# transitions into segment i: 'push' (iOS nav slide) or 'fade'
TRANS = {1: ('push', .38), 2: ('push', .38), 3: ('fade', .14), 4: ('push', .42), 5: ('fade', .30), 6: ('fade', .12), 7: ('fade', .12)}
# taps: time, shot whose frame is on screen, css point
TAPS = [(3.55, 'a_home', taps['a_home']), (5.30, 'b_calendar', taps['b_calendar']),
        (7.85, 'c_showings', taps['c_showings']), (17.05, 'g_colors', taps['g_colors']),
        (18.65, 'h_gold', taps['h_gold'])]

def crop_box(seg, t):
    s0, s1, name, z0, z1, (fx, fy), d = seg
    z = z0 + (z1 - z0) * ease((t - s0 - d) / max(0.01, (s1 - s0 - d)))
    cw, ch = SW / z, SH / z
    x0 = min(max(fx - cw / 2, 0), SW - cw); y0 = min(max(fy - ch / 2, 0), SH - ch)
    return (x0, y0, x0 + cw, y0 + ch)

def view(i, t):
    seg = SEG[i]; box = crop_box(seg, t)
    im = shots[seg[2]].resize((IW, IH), Image.LANCZOS, box=box)
    for (tt, nm, (cx, cy)) in TAPS:                       # touch indicator
        if nm == seg[2] and tt <= t < tt + 0.5:
            p = (t - tt) / 0.5
            x = (cx * 2 - box[0]) / (box[2] - box[0]) * IW; y = (cy * 2 - box[1]) / (box[3] - box[1]) * IH
            ov = Image.new('RGBA', (IW, IH), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
            r = 26 + 34 * ease_out(p); a = int(150 * (1 - p))
            d.ellipse((x - r, y - r, x + r, y + r), fill=(70, 70, 70, a // 2), outline=(255, 255, 255, a), width=3)
            if p < 0.35:
                r2 = 22; d.ellipse((x - r2, y - r2, x + r2, y + r2), fill=(40, 40, 40, int(110 * (1 - p / 0.35))))
            im = Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB')
    return im

def screen(t):
    i = max(k for k, s in enumerate(SEG) if t >= s[0]) if t >= 0 else 0
    i = min(i, len(SEG) - 1)
    cur = view(i, t)
    if i in TRANS:
        kind, dur = TRANS[i]; p = (t - SEG[i][0]) / dur
        if p < 1:
            prev = view(i - 1, t); q = ease(p)
            if kind == 'fade':
                cur = Image.blend(prev, cur, q)
            else:   # push: new screen slides in from the right, old one parallaxes left and dims
                out = Image.new('RGB', (IW, IH))
                pv = Image.blend(prev, Image.new('RGB', (IW, IH), (0, 0, 0)), 0.25 * q)
                out.paste(pv, (int(-IW * 0.3 * q), 0)); out.paste(cur, (int(IW * (1 - q)), 0))
                cur = out
    return cur

# ---- static frame pieces
bg = Image.new('RGB', (W, H), GREEN)
g = ImageDraw.Draw(bg)
for y in range(H):
    k = y / H; c = tuple(int(GREEN[j] * (1 - k) + GREEN_D[j] * k) for j in range(3)); g.line([(0, y), (W, y)], fill=c)
mask = Image.new('L', (IW, IH), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, IW - 1, IH - 1), RAD, fill=255)
shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
ImageDraw.Draw(shadow).rounded_rectangle((IX, IY + 18, IX + IW, IY + IH + 18), RAD, fill=(0, 0, 0, 120))
shadow = shadow.filter(ImageFilter.GaussianBlur(28))
frame_bg = Image.alpha_composite(bg.convert('RGBA'), shadow)
ring = Image.new('RGBA', (W, H), (0, 0, 0, 0))
ImageDraw.Draw(ring).rounded_rectangle((IX - 3, IY - 3, IX + IW + 2, IY + IH + 2), RAD + 3, outline=(243, 241, 230, 70), width=3)

# ---- captions: (start, end, line1, line2)
CAPS = [(0.0, 4.0, 'Your whole business.', 'One screen.'),
        (4.0, 8.2, 'Showing requests,', 'handled in one tap.'),
        (8.2, 11.2, 'Buyer texted.', 'Seller in the loop.'),
        (11.2, 15.6, 'Every deal.', 'Every deadline.'),
        (15.6, 21.0, 'Your brand.', 'Not ours.')]
F1, F2 = font('Bold', 76), font('ExtraBold', 76)

def draw_caption(img, t):
    for (s, e, l1, l2) in CAPS:
        if s <= t < e:
            pin = ease_out((t - s) / 0.45); pout = 1 - ease((t - (e - 0.22)) / 0.22) if e < 21.0 or t > 20.6 else 1
            a = pin * pout
            if a <= 0: return
            layer = Image.new('RGBA', (W, 400), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
            for k, (txt, fnt, col) in enumerate([(l1, F1, CREAM), (l2, F2, BRASS)]):
                w = d.textlength(txt, font=fnt); dy = int(26 * (1 - ease_out((t - s - 0.08 * k) / 0.45)))
                d.text(((W - w) / 2, 150 + k * 96 + dy), txt, font=fnt, fill=col + (int(255 * a),))
            img.alpha_composite(layer, (0, 0))

# ---- end card
icon = Image.open('assets/AppIcon.png').convert('RGB')
FW, FT, FS = font('Bold', 84), font('ExtraBold', 70), font('SemiBold', 34)

def end_card(t):
    img = bg.copy().convert('RGBA'); d = ImageDraw.Draw(img)
    p = ease_out((t - 21.0) / 0.7)
    sz = int(260 * (0.9 + 0.1 * p))
    ic = icon.resize((sz, sz), Image.LANCZOS); m = Image.new('L', (sz, sz), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, sz - 1, sz - 1), int(sz * 0.225), fill=int(255 * p))
    shadow2 = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow2).rounded_rectangle(((W - sz) // 2, 470 + 14, (W + sz) // 2, 470 + sz + 14), int(sz * .225), fill=(0, 0, 0, int(90 * p)))
    img.alpha_composite(shadow2.filter(ImageFilter.GaussianBlur(20)))
    img.paste(ic, ((W - sz) // 2, 470 + (260 - sz) // 2), m)
    def txt(s, fnt, y, col, t0):
        q = ease_out((t - t0) / 0.5)
        if q <= 0: return
        w = d.textlength(s, font=fnt); d.text(((W - w) / 2, y + 20 * (1 - q)), s, font=fnt, fill=col + (int(255 * q),))
    txt('MyRealtyVault', FW, 790, CREAM, 21.35)
    txt('Every home.', FT, 1010, CREAM, 21.9)
    txt('Every deal.', FT, 1100, CREAM, 22.3)
    txt('One vault.', FT, 1190, BRASS, 22.7)
    txt('For agents, brokers and homeowners', FS, 1600, (243, 241, 230), 23.3)
    return img

def frame(t):
    img = frame_bg.copy()
    if t < 21.4:
        img.paste(screen(min(t, 20.99)), (IX, IY), mask)
        img.alpha_composite(ring); draw_caption(img, t)
    if t >= 21.0:
        e = end_card(t); a = ease((t - 21.0) / 0.45)
        img = Image.blend(img, e, a) if a < 1 else e
    return img.convert('RGB')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        for t in [1.0, 4.2, 7.9, 10.6, 15.0, 17.1, 20.0, 24.5]:
            frame(t).save(f'shots/still_{t:05.2f}.jpg', quality=88)
        sys.exit()
    out = sys.argv[1] if len(sys.argv) > 1 else 'video_noaudio.mp4'
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', str(FPS), out + '.tmp.mp4'], stdin=subprocess.PIPE)
    for n in range(int(DUR * FPS)):
        ff.stdin.write(frame(n / FPS).tobytes())
    ff.stdin.close(); rc = ff.wait()
    if rc == 0:
        import os; os.replace(out + '.tmp.mp4', out); print('ok', out)
