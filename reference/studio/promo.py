"""MRV infomercial promo — 1080x1920, 30 fps, timed to the voice-over. Videos-as-code."""
import json, math, random, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
GREEN, GREEN_D, CREAM, BRASS = (40, 64, 46), (24, 40, 29), (243, 241, 230), (212, 175, 92)
INK, RED = (17, 19, 23), (232, 72, 60)
F = '/usr/share/fonts/opentype/inter/'
def font(w, s): return ImageFont.truetype(F + f'InterDisplay-{w}.otf', s)
def ease(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def eout(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def back(x, s=1.7): x = max(0.0, min(1.0, x)); x -= 1; return x * x * ((s + 1) * x + s) + 1
def lerp(a, b, k): return a + (b - a) * k

VOICE = sys.argv[2] if len(sys.argv) > 2 else 'af_heart'
vo = {m['key']: m for m in json.load(open(f'vo/vo_{VOICE}.json'))}
START = {}
t = 1.95
COVER = 1.65
GAP = {'hook': .35, 'chaos1': .12, 'chaos2': .25, 'chaos3': .5, 'turn': .35, 'home': .3, 'show1': .2, 'show2': .4, 'deal': .3, 'brand': .4, 'vault': .5, 'cta': 0}
for k in ['hook', 'chaos1', 'chaos2', 'chaos3', 'turn', 'home', 'show1', 'show2', 'deal', 'brand', 'vault', 'cta']:
    START[k] = t; t += vo[k]['dur'] + GAP[k]
END = {k: START[k] + vo[k]['dur'] for k in START}
DUR = END['cta'] + 2.2

CAP = 'cap/'
shot = {n: Image.open(CAP + n + '.jpg').convert('RGB') for n in ['a_home', 'b_calendar', 'c_showings', 'd_receipt', 'f_closings', 'g_colors', 'h_gold', 'i_dark']}
shot['vault'] = Image.open('cap/vault.jpg').convert('RGB')
taps = json.load(open(CAP + 'taps.json'))
icon_mrv = Image.open('assets/AppIcon.png').convert('RGB')

# ---------- phone builder (generic device: dark bezel, rounded) ----------
PW = 640; SCR_W = PW - 28; SCR_H = int(SCR_W * 1920 / 886); PH = SCR_H + 28
_phone_cache = {}
def phone(name, box=None, tap=None):
    key = (name, box, tap)
    if key in _phone_cache: return _phone_cache[key]
    src = shot[name]
    scr = src.resize((SCR_W, SCR_H), Image.LANCZOS, box=box) if box else src.resize((SCR_W, SCR_H), Image.LANCZOS)
    ph = Image.new('RGBA', (PW, PH), (0, 0, 0, 0)); d = ImageDraw.Draw(ph)
    d.rounded_rectangle((0, 0, PW - 1, PH - 1), 64, fill=(14, 15, 18, 255))
    d.rounded_rectangle((3, 3, PW - 4, PH - 4), 62, outline=(70, 72, 78, 255), width=2)
    m = Image.new('L', (SCR_W, SCR_H), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, SCR_W - 1, SCR_H - 1), 50, fill=255)
    ph.paste(scr, (14, 14), m)
    if len(_phone_cache) < 40: _phone_cache[key] = ph
    return ph

def put_phone(img, ph, cx, cy, scale=1.0, rot=0.0, alpha=1.0, shadow=True):
    if scale <= 0.01 or alpha <= 0: return
    p = ph.resize((max(1, int(ph.width * scale)), max(1, int(ph.height * scale))), Image.BILINEAR)
    if abs(rot) > 0.05: p = p.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 1: p.putalpha(p.getchannel('A').point(lambda v: int(v * alpha)))
    if shadow:
        sh = Image.new('RGBA', p.size, (0, 0, 0, 0)); sh.putalpha(p.getchannel('A').point(lambda v: int(v * 0.45)))
        sh = sh.filter(ImageFilter.GaussianBlur(26))
        img.alpha_composite(sh, (int(cx - p.width / 2), int(cy - p.height / 2 + 30)))
    img.alpha_composite(p, (int(cx - p.width / 2), int(cy - p.height / 2)))

def tap_ring(img, x, y, p):
    if not (0 <= p < 1): return
    ov = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    r = 24 + 40 * eout(p); a = int(200 * (1 - p))
    d.ellipse((x - r, y - r, x + r, y + r), outline=(255, 255, 255, a), width=5, fill=(60, 60, 60, a // 3))
    img.alpha_composite(ov)

def screen_pt(name, css, cx, cy, scale):
    """css point on a capture -> stage point for a phone centered at cx,cy (no rotation)."""
    sx = css[0] * 2 / 886 * SCR_W + 14; sy = css[1] * 2 / 1920 * SCR_H + 14
    return cx + (sx - PW / 2) * scale, cy + (sy - PH / 2) * scale

# ---------- text ----------
def text_c(img, s, y, fnt, col, alpha=1.0, dy=0, cx=W / 2, scale=1.0):
    if alpha <= 0: return
    if scale != 1.0:
        fnt = font_scaled(fnt, scale)
    d = ImageDraw.Draw(img); w = d.textlength(s, font=fnt)
    d.text((cx - w / 2, y + dy), s, font=fnt, fill=col + (int(255 * alpha),))
_fs = {}
def font_scaled(fnt, k):
    key = (fnt.path, int(fnt.size * k))
    if key not in _fs: _fs[key] = ImageFont.truetype(fnt.path, max(8, int(fnt.size * k)))
    return _fs[key]

def caption(img, t, s0, s1, l1, l2, y=150, c1=CREAM, c2=BRASS, size=84):
    if not (s0 - 0.05 <= t < s1): return
    a = min(eout((t - s0) / 0.35), 1 - ease((t - (s1 - 0.2)) / 0.2))
    f1, f2 = font('Bold', size), font('ExtraBold', size)
    text_c(img, l1, y, f1, c1, a, 30 * (1 - eout((t - s0) / 0.4)))
    if l2: text_c(img, l2, y + size * 1.18, f2, c2, a * eout((t - s0 - 0.12) / 0.35), 30 * (1 - eout((t - s0 - 0.12) / 0.4)))

# ---------- backgrounds ----------
def grad(c0, c1):
    im = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(im)
    for y in range(H):
        k = y / H; d.line([(0, y), (W, y)], fill=tuple(int(c0[j] * (1 - k) + c1[j] * k) for j in range(3)) + (255,))
    return im
BG_DARK, BG_GREEN = grad((28, 31, 37), (12, 13, 16)), grad(GREEN, GREEN_D)
BG_GOLD, BG_NIGHT = grad((120, 92, 38), (54, 41, 18)), grad((30, 33, 40), (10, 11, 14))
vig = Image.new('L', (W, H), 0); ImageDraw.Draw(vig).ellipse((-300, -200, W + 300, H + 200), fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(160))
VIG = Image.new('RGBA', (W, H), (0, 0, 0, 0)); VIG.putalpha(vig.point(lambda v: int((255 - v) * 0.55)))

# ---------- chaos props ----------
APP_ICONS = [((59, 130, 246), 'person'), ((34, 197, 94), 'chat'), ((249, 115, 22), 'cal'), ((168, 85, 247), 'mail'),
             ((20, 184, 166), 'grid'), ((239, 68, 68), 'folder'), ((234, 179, 8), 'note'), ((99, 102, 241), 'phone')]
def make_icon(col, kind, s=190):
    im = Image.new('RGBA', (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, s - 1, s - 1), int(s * .23), fill=col + (255,)); w = (255, 255, 255, 255); c = s / 2
    if kind == 'person': d.ellipse((c - 28, 42, c + 28, 98), fill=w); d.pieslice((c - 58, 108, c + 58, 220), 180, 360, fill=w)
    elif kind == 'chat': d.rounded_rectangle((38, 48, s - 38, 128), 30, fill=w); d.polygon([(70, 120), (60, 152), (100, 124)], fill=w)
    elif kind == 'cal': d.rounded_rectangle((40, 50, s - 40, s - 40), 16, fill=w); d.rectangle((40, 50, s - 40, 82), fill=(255, 255, 255, 150)); [d.ellipse((60 + i * 26, 100 + j * 24, 72 + i * 26, 112 + j * 24), fill=col + (255,)) for i in range(3) for j in range(2)]
    elif kind == 'mail': d.rectangle((36, 60, s - 36, 132), fill=w); d.line([(36, 60), (c, 104), (s - 36, 60)], fill=col + (255,), width=8)
    elif kind == 'grid': [d.rectangle((44 + i * 36, 48 + j * 34, 72 + i * 36, 72 + j * 34), fill=w) for i in range(3) for j in range(3)]
    elif kind == 'folder': d.rounded_rectangle((36, 70, s - 36, 140), 12, fill=w); d.rounded_rectangle((36, 56, 96, 84), 10, fill=w)
    elif kind == 'note': [d.line([(50, 64 + i * 22), (s - 50, 64 + i * 22)], fill=w, width=9) for i in range(4)]
    elif kind == 'phone': d.rounded_rectangle((70, 40, s - 70, s - 40), 18, fill=w); d.rectangle((80, 56, s - 80, s - 64), fill=col + (255,))
    return im
ICONS = [make_icon(c, k) for c, k in APP_ICONS]
random.seed(7)
ICON_POS = [(170, 560, -14), (900, 520, 12), (300, 1180, 9), (820, 1260, -11), (560, 760, 4), (150, 1500, -6), (930, 1640, 15), (540, 1430, -8)]
def badge(img, x, y, n, a=1.0):
    d = ImageDraw.Draw(img); r = 34
    d.ellipse((x - r, y - r, x + r, y + r), fill=RED + (int(255 * a),))
    f = font('Bold', 34); s = str(n); w = d.textlength(s, font=f); d.text((x - w / 2, y - 22), s, font=f, fill=(255, 255, 255, int(255 * a)))

NOTIFS = [('MESSAGES', 'Jen (buyer)', 'Is 4pm still ok for the showing??', (34, 197, 94)),
          ('MAIL', 'Counter offer', 'RE: RE: RE: See attached… again', (59, 130, 246)),
          ('CALENDAR', 'Conflict', 'Two showings at 2:00 PM', (249, 115, 22)),
          ('PHONE', 'Missed call', '(352) 555-0199 · Buyer', (99, 102, 241))]
LOST = ('MESSAGES', 'Jen (buyer)', 'Never mind. We went with another agent.', (34, 197, 94))
def notif_card(n, w=940):
    app, title, body, col = n
    im = Image.new('RGBA', (w, 176), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, 175), 40, fill=(250, 250, 252, 246))
    d.rounded_rectangle((28, 30, 92, 94), 16, fill=col + (255,))
    d.text((116, 26), app, font=font('SemiBold', 26), fill=(120, 120, 128, 255)); d.text((w - 110, 26), 'now', font=font('SemiBold', 26), fill=(150, 150, 156, 255))
    d.text((116, 62), title, font=font('Bold', 36), fill=(20, 20, 24, 255)); d.text((116, 108), body, font=font('SemiBold', 34), fill=(60, 60, 66, 255))
    return im
NOTIF_IMG = [notif_card(n) for n in NOTIFS]; LOST_IMG = notif_card(LOST)
def sticky():
    s = 420; im = Image.new('RGBA', (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, s - 1, s - 1), fill=(253, 224, 71, 255)); d.rectangle((0, 0, s - 1, 46), fill=(250, 204, 21, 255))
    f = font('Bold', 46)
    for i, ln in enumerate(['Inspection', 'ends THU??', 'call lender!!', '— and Jen']):
        d.text((34, 80 + i * 72), ln, font=f, fill=(55, 48, 20, 255))
    return im
STICKY = sticky()

# ---------- callout chips (solution) ----------
def chip(label, glyph_col):
    f = font('Bold', 40); tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1))); w = int(tmp.textlength(label, font=f)) + 130
    im = Image.new('RGBA', (w, 100), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, 99), 50, fill=(255, 255, 255, 250))
    d.ellipse((22, 22, 78, 78), fill=glyph_col + (255,)); d.line([(36, 52), (46, 62), (66, 38)], fill=(255, 255, 255, 255), width=7)
    d.text((98, 26), label, font=f, fill=(20, 24, 22, 255))
    return im
CHIPS = [chip('Buyer texted', (34, 160, 90)), chip('Buyer emailed', (34, 160, 90)), chip('Seller notified', (34, 160, 90))]

# ---------- scenes ----------
HOUSE = Image.open('cap/house.jpg').convert('RGB')   # Pexels #210617 (free license) + composited sign — make_house.py
_hc = {}
def house_frame(z):
    """full-bleed vertical crop of the house photo, centred on the sign, pushed in by z"""
    k = round(z, 3)
    if k in _hc: return _hc[k]
    hw, hh = HOUSE.size; ch = hh / z; cw = ch * W / H; cx = 1380 - 240 * min(1, (z - 1.15) / 0.22)   # home first, drifting onto the sign
    x0 = min(max(cx - cw / 2, 0), hw - cw); y0 = (hh - ch) * 0.80
    im = HOUSE.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch)).convert('RGBA')
    if len(_hc) < 60: _hc[k] = im
    return im
TOPSHADE = Image.new('RGBA', (W, H), (0, 0, 0, 0))
_d = ImageDraw.Draw(TOPSHADE)
for y in range(520): _d.line([(0, y), (W, y)], fill=(0, 0, 0, int(150 * (1 - y / 520) ** 1.6)))
NEW_REQ = notif_card(('MESSAGES', '(352) 555-0171', 'Can we see 88 Heron Bend tomorrow?', (34, 197, 94)))

def scene_cover(img, t):
    img.alpha_composite(house_frame(1.15 + 0.22 * (t / COVER)))

def scene_hook(img, t):
    img.alpha_composite(BG_DARK)
    q = (t - COVER) / 0.3
    if q < 1:
        ph = house_frame(1.37 + 0.25 * eout(q)).copy(); ph.putalpha(int(255 * (1 - eout(q))))
        img.alpha_composite(ph)
    s = START['hook']; words = [("You didn't become", 0.0, CREAM, 'Bold', 92), ('an agent', 0.6, CREAM, 'Bold', 92),
                                ('to fight with', 1.0, CREAM, 'Bold', 112), ('SOFTWARE.', 1.75, RED, 'Black', 150)]
    for i, (w_, off, col, wt, sz) in enumerate(words):
        p = (t - s - off) / 0.32
        if p <= 0: continue
        k = back(p, 2.2); y = 640 + i * 150 + (40 if i == 3 else 0)
        text_c(img, w_, y, font(wt, sz), col, min(1, p * 2), 0, scale=0.6 + 0.4 * k)
    img.alpha_composite(VIG)

def scene_chaos(img, t):
    img.alpha_composite(BG_DARK)
    s1, s2, s3 = START['chaos1'], START['chaos2'], START['chaos3']
    shake = 0
    if t > s3: shake = 10 * math.sin(t * 61) * max(0, 1 - (t - s3) / 1.2)
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for i, ic in enumerate(ICONS):                     # icons fly in from off-screen and pile up
        t0 = s1 + 0.25 + i * 0.42; p = (t - t0) / 0.5
        if p <= 0: continue
        x, y, r = ICON_POS[i]; ox = -400 if x < W / 2 else W + 400
        k = back(p, 1.6); cx = lerp(ox, x, k); cy = lerp(y - 500, y, k)
        rr = lerp(r * 4, r, eout(p)) + 3 * math.sin(t * 3 + i)
        im = ic.rotate(rr, resample=Image.BICUBIC, expand=True)
        layer.alpha_composite(im, (int(cx - im.width / 2 + shake), int(cy - im.height / 2)))
        n = int(min(99, max(1, (t - t0) * (4 + i * 2)))); badge(layer, int(cx + 75 + shake), int(cy - 75), n, min(1, p))
    img.alpha_composite(layer)
    dim = Image.new('RGBA', (W, H), (0, 0, 0, int(110 * ease((t - s1 - 1.8) / 0.6)))); img.alpha_composite(dim)
    for j, nimg in enumerate(NOTIF_IMG):                # notifications stack down from the top
        t0 = s1 + 1.6 + j * 0.75; p = (t - t0) / 0.4
        if p <= 0: continue
        later = sum(1 for jj in range(j + 1, len(NOTIF_IMG)) if t > s1 + 1.6 + jj * 0.75)
        y = lerp(-200, 210 + later * 196, eout(p)) if later == 0 else 210 + later * 196 - 196 * (1 - eout((t - (s1 + 1.6 + (j + later) * 0.75)) / 0.4))
        img.alpha_composite(nimg, (int((W - nimg.width) / 2 + shake), int(y)))
    if t > s2 - 0.1:                                    # the sticky note slaps on
        p = (t - (s2 + 0.35)) / 0.28
        if p > 0:
            sc = lerp(2.2, 1.0, eout(p)); im = STICKY.resize((int(420 * sc), int(420 * sc))).rotate(-8, resample=Image.BICUBIC, expand=True)
            img.alpha_composite(im, (int(W / 2 - im.width / 2 + 150 + shake), int(1180 - im.height / 2)))
    if t > s3:                                          # the loss
        p = (t - s3 - 0.2) / 0.35
        red = Image.new('RGBA', (W, H), RED + (int(70 * ease((t - s3) / 0.4)),)); img.alpha_composite(red)
        if p > 0:
            img.alpha_composite(LOST_IMG, (int((W - LOST_IMG.width) / 2 + shake), int(lerp(-200, 820, back(p, 1.3)))))
        text_c(img, 'Every missed text', 1560, font('Bold', 78), CREAM, ease((t - s3 - 0.6) / 0.3))
        text_c(img, '= a lost showing.', 1660, font('Black', 92), RED if False else (255, 214, 205), ease((t - s3 - 0.9) / 0.3))
    img.alpha_composite(VIG)

def scene_turn(img, t):
    s = START['turn']; p = (t - s) / 0.5
    img.alpha_composite(BG_GREEN)
    # iris wipe from the dark chaos into vault green
    if p < 1:
        old = Image.new('RGBA', (W, H)); scene_chaos(old, END['chaos3'] + 0.3)
        m = Image.new('L', (W, H), 255); r = int(1300 * eout(p)); ImageDraw.Draw(m).ellipse((W / 2 - r, H / 2 - r, W / 2 + r, H / 2 + r), fill=0)
        img.paste(old, (0, 0), m)
    text_c(img, "There's a better way.", 560, font('Bold', 80), CREAM, ease((t - s - 0.2) / 0.35), 30 * (1 - eout((t - s - 0.2) / 0.4)))
    q = (t - s - 1.2) / 0.5
    if q > 0:
        sz = int(300 * back(q, 1.8)); ic = icon_mrv.resize((max(1, sz), max(1, sz)), Image.LANCZOS)
        m = Image.new('L', ic.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, sz - 1, sz - 1), int(sz * .225), fill=255)
        img.paste(ic, (int(W / 2 - sz / 2), int(930 - sz / 2 + 150)), m)
        text_c(img, 'MyRealtyVault', 1270, font('Black', 104), CREAM, ease(q * 1.5), 20 * (1 - eout(q)))

def scene_home(img, t):
    s, e = START['home'], END['home']
    img.alpha_composite(BG_GREEN)
    p = (t - s + 0.15) / 0.75
    cy = lerp(H + 700, 1180, back(p, 1.25)); rot = lerp(-14, -3, eout(p)) + 3 * ease((t - s - 1) / 1.5)
    sc = lerp(1.0, 1.0, 0)
    put_phone(img, phone('a_home'), W / 2, cy, 1.0 * sc, rot)
    caption(img, t, s, START['show1'], 'Your whole business.', 'One screen.')
    q = (t - s - 2.2) / 0.45                            # sub-caption pops
    if q > 0: text_c(img, 'Built for agents on the go', 430, font('SemiBold', 40), CREAM, min(1, q) * (1 - ease((t - e - .1) / .2)))

def scene_show(img, t):
    s1, s2, e = START['show1'], START['show2'], END['show2']
    img.alpha_composite(BG_GREEN)
    p = (t - s1 + 0.1) / 0.55
    cx = lerp(W + 600, W / 2, eout(p)); rot = lerp(12, 0, eout(p))
    name = 'c_showings' if t < s1 + 2.15 else 'd_receipt'
    ph = phone(name); put_phone(img, ph, cx, 1180, 1.0, rot)
    if t > s1 + 1.7 and t < s1 + 2.3:
        x, y = screen_pt('c_showings', taps['c_showings'], W / 2, 1180, 1.0); tap_ring(img, x, y, (t - s1 - 1.75) / 0.5)
    caption(img, t, s1, s2, 'A showing request?', 'One tap.')
    caption(img, t, s2, e + 0.4, 'Buyer and seller,', 'handled.')
    for i, c in enumerate(CHIPS):                       # chips fly out of the phone
        q = (t - s2 - 0.45 - i * 0.55) / 0.45
        if q <= 0: continue
        x = lerp(W / 2, [90, 330, 130][i], back(q, 1.5)); y = lerp(1100, [700, 1560, 1760][i], back(q, 1.5))
        img.alpha_composite(c, (int(x), int(y)))

def scene_deal(img, t):
    s, e = START['deal'], END['deal']
    img.alpha_composite(BG_GREEN)
    p = (t - s + 0.1) / 0.5
    # camera: phone slides in, then pushes in hard on Grace's deal card
    z = lerp(1.0, 1.6, ease((t - s - 0.7) / 1.4))
    ph = phone('f_closings')
    cx = lerp(-600, W / 2, eout(p))
    card_off = (14 + 660 / 1920 * SCR_H) - PH / 2          # Grace's card, relative to phone centre
    cy = lerp(1180, 1200 - card_off * 1.6, ease((t - s - 0.7) / 1.4)) if t > s + 0.7 else 1180
    put_phone(img, ph, cx, cy, z, lerp(-10, 0, eout(p)))
    caption(img, t, s, e + 0.3, 'Every deal.', 'Every deadline.', y=150)

def scene_brand(img, t):
    s, e = START['brand'], END['brand']
    seq = [('g_colors', 0.0), ('h_gold', 1.25), ('i_dark', 2.35)]
    cur = max(i for i, (_, o) in enumerate(seq) if t >= s + o - 0.0001) if t >= s else 0
    bgs = [BG_GREEN, BG_GOLD, BG_NIGHT]
    img.alpha_composite(bgs[cur])
    if cur > 0:
        k = ease((t - s - seq[cur][1]) / 0.3)
        if k < 1: img.alpha_composite(Image.blend(bgs[cur - 1], bgs[cur], k))
    pop = 1 + 0.05 * math.sin(min(1, (t - s - seq[cur][1]) / 0.25) * math.pi) if cur > 0 else 1
    p = (t - s + 0.1) / 0.5
    put_phone(img, phone(seq[cur][0]), W / 2, lerp(H + 600, 1180, back(p, 1.2)), pop, 0)
    for nm, tt in [('g_colors', s + 1.05), ('h_gold', s + 2.15)]:
        x, y = screen_pt(nm, taps[nm], W / 2, 1180, 1.0); tap_ring(img, x, y, (t - tt) / 0.45)
    caption(img, t, s, e + 0.4, 'Your brand.', 'Not ours.')

def scene_vault(img, t):
    s, e = START['vault'], END['vault']
    img.alpha_composite(BG_GREEN)
    p = (t - s + 0.1) / 0.6; q = (t - s - 0.5) / 0.6
    put_phone(img, phone('i_dark'), lerp(W / 2, 330, eout(p)), 1230, lerp(1.0, 0.78, eout(p)), lerp(0, -7, eout(p)))
    if q > 0: put_phone(img, phone('vault'), lerp(W + 500, 760, back(q, 1.2)), 1270, 0.78, lerp(14, 6, eout(q)))
    caption(img, t, s, e + 0.4, 'Your clients get', 'a vault of their own.')
    r = (t - s - 2.3) / 0.4
    if r > 0: text_c(img, "You stay on their phone after closing", 440, font('SemiBold', 40), CREAM, min(1, r) * (1 - ease((t - e - .2) / .2)))

def scene_cta(img, t):
    s = START['cta']; img.alpha_composite(BG_GREEN)
    p = (t - s) / 0.6; sz = int(280 * back(p, 1.6)) if p > 0 else 1
    if sz > 2:
        ic = icon_mrv.resize((sz, sz), Image.LANCZOS); m = Image.new('L', ic.size, 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, sz - 1, sz - 1), int(sz * .225), fill=255); img.paste(ic, (int(W / 2 - sz / 2), int(560 - sz / 2)), m)
    text_c(img, 'MyRealtyVault', 780, font('Black', 104), CREAM, ease((t - s - 0.2) / 0.4))
    for i, (w_, col) in enumerate([('Every home.', CREAM), ('Every deal.', CREAM), ('One vault.', BRASS)]):
        q = (t - s - 1.0 - i * 0.42) / 0.3
        text_c(img, w_, 1010 + i * 105, font('ExtraBold', 86), col, min(1, max(0, q)), 0, scale=0.7 + 0.3 * back(q, 2))
    q = (t - s - 2.9) / 0.4
    if q > 0:
        d = ImageDraw.Draw(img); f = font('Bold', 46); lab = 'Get it on the App Store today'; w = d.textlength(lab, font=f) + 110
        a = int(255 * min(1, q)); y = 1520 + 30 * (1 - eout(q))
        d.rounded_rectangle((W / 2 - w / 2, y, W / 2 + w / 2, y + 110), 55, fill=CREAM + (a,))
        d.text((W / 2 - w / 2 + 55, y + 28), lab, font=f, fill=GREEN_D + (a,))

SCENES = [('cover', scene_cover), ('hook', scene_hook), ('chaos1', scene_chaos), ('turn', scene_turn), ('home', scene_home), ('show1', scene_show),
          ('deal', scene_deal), ('brand', scene_brand), ('vault', scene_vault), ('cta', scene_cta)]
SCENE_START = [0.0, COVER] + [START[k] - 0.15 for k, _ in SCENES[2:]]
SCENE_START[3] = START['turn'] - 0.02   # the iris wipe owns its own transition

def frame(t):
    img = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    i = max(j for j, s in enumerate(SCENE_START) if t >= s)
    SCENES[i][1](img, t)
    # whip-pan blur flash on scene cuts (except the iris)
    if i not in (0, 3) and t - SCENE_START[i] < 0.12:
        img = img.filter(ImageFilter.BoxBlur(int(14 * (1 - (t - SCENE_START[i]) / 0.12)) + 1))
    return img.convert('RGB')

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'video'
    if mode == 'cover':
        frame(0).save('out/MRV_Promo_Cover_1080x1920.png'); sys.exit()
    if mode == 'stills':
        ts = [START['hook'] + 2.6, START['chaos1'] + 4.6, START['chaos2'] + 1.0, START['chaos3'] + 1.4, START['turn'] + 1.9,
              START['home'] + 2.6, START['show1'] + 1.9, START['show2'] + 3.0, START['deal'] + 2.6, START['brand'] + 1.6, START['vault'] + 3.0, START['cta'] + 3.6]
        for k, tt in enumerate(ts): frame(tt).save(f'shots/p_{k:02d}.jpg', quality=85)
        print(json.dumps({k: round(v, 2) for k, v in START.items()}), round(DUR, 2)); sys.exit()
    out = 'out/promo_noaudio.mp4'
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-crf', '19', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', out + '.tmp.mp4'], stdin=subprocess.PIPE)
    for n in range(int(DUR * FPS)):
        ff.stdin.write(frame(n / FPS).tobytes())
    ff.stdin.close()
    if ff.wait() == 0:
        import os; os.replace(out + '.tmp.mp4', out); print('ok', round(DUR, 2))
