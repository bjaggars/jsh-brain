"""MRV HOMEOWNER promo — 1080x1920, 30 fps. Own script (vo/vo_home.py), homeowner-vault footage only (cap_home/).
Reuses the studio's drawing helpers from promo.py. Founder 11/10/26."""
import json, math, os, subprocess, sys
os.environ.setdefault('MRV_CUT', 'full')
from promo import (W, H, FPS, GREEN, GREEN_D, CREAM, BRASS, RED, font, ease, eout, back, lerp, put_phone, tap_ring, text_c,
                   caption, BG_DARK, BG_GREEN, VIG, icon_mrv, notif_card, chip, shot, PW, PH, SCR_W, SCR_H, phone)
from PIL import Image, ImageDraw, ImageFilter

# ---------- timing (VO-driven) ----------
vo = {m['key']: m for m in json.load(open('vo/vo_home.json'))}
ORDER = ['h_open', 'h_chaos1', 'h_chaos2', 'h_turn', 'h_plan', 'h_onestop', 'h_afford', 'h_steps', 'h_docs', 'h_agent', 'h_cta']
GAP = {'h_open': .45, 'h_chaos1': .15, 'h_chaos2': .55, 'h_turn': .35, 'h_plan': .6, 'h_onestop': .4, 'h_afford': .35, 'h_steps': .35, 'h_docs': .5, 'h_agent': .45, 'h_cta': 0}
START, t = {}, 0.45
for k in ORDER: START[k] = t; t += vo[k]['dur'] + GAP[k]
END = {k: START[k] + vo[k]['dur'] for k in START}
COVER = END['h_open'] + 0.4           # the house holds through the opening line, then crashes to dark
DUR = END['h_cta'] + 2.0
VOF = {k: vo[k] for k in ORDER}; CUT = 'home'
CAP = 'cap_home/'

for n in ['a_setup', 'b_setup2', 'c_dash', 'e_calc_filled', 'f_checklist', 'g_docs', 'i_share_form', 'j_share_sent', 'k_dash_agent', 'l_agent']:
    shot['H_' + n] = Image.open(CAP + n + '.jpg').convert('RGB')
TAPS = json.load(open(CAP + 'taps.json'))
shot['H_m_full'] = Image.open(CAP + 'm_dash_full.jpg').convert('RGB')
TILES = json.load(open(CAP + 'tiles.json'))
TAPS['a_setup'] = [220, 571]; TAPS['b_setup2'] = [221, 737]          # "Keep my home organized", "Build my dashboard"
def spt(css, cx, cy, sc=1.0):
    sx = css[0] * 2 / 886 * SCR_W + 14; sy = css[1] * 2 / 1920 * SCR_H + 14
    return cx + (sx - PW / 2) * sc, cy + (sy - PH / 2) * sc

# ---------- opening photo: the dream (Pexels #210617, no sign) ----------
HOUSE = Image.open(CAP + 'house_clean.jpg').convert('RGB')
_hc = {}
def house(z):
    k = round(z, 3)
    if k not in _hc:
        if len(_hc) > 80: _hc.clear()
        hw, hh = HOUSE.size; ch = hh / z; cw = ch * W / H; cx = 2350 - 250 * min(1, (z - 1.1) / 0.2)   # the arched entry
        x0 = min(max(cx - cw / 2, 0), hw - cw); y0 = (hh - ch) * 0.62
        _hc[k] = HOUSE.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch)).convert('RGBA')
    return _hc[k]

def scene_cover(img, t):
    img.alpha_composite(house(1.1 + 0.2 * min(1, t / COVER)))
    q = (t - START['h_open'] - 0.1) / 0.5                      # soft line over the photo, no brand
    if q > 0:
        sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(sh)
        for y in range(1300, H): d.line([(0, y), (W, y)], fill=(0, 0, 0, int(150 * (y - 1300) / 620)))
        img.alpha_composite(sh)
        text_c(img, 'Buying a home', 1500, font('Bold', 88), CREAM, min(1, q), 20 * (1 - eout(q)))
        text_c(img, 'should be exciting.', 1610, font('ExtraBold', 88), CREAM, min(1, (q - 0.3) * 1.5), 20 * (1 - eout(q - 0.3)))

# ---------- chaos props: tabs, paperwork, lender asks ----------
def tab_card(title, sub, col, w=560):
    im = Image.new('RGBA', (w, 128), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, 127), 22, fill=(248, 248, 250, 255)); d.rounded_rectangle((22, 26, 70, 74), 10, fill=col + (255,))
    d.text((90, 18), title, font=font('Bold', 34), fill=(25, 25, 30, 255)); d.text((90, 66), sub, font=font('SemiBold', 28), fill=(110, 110, 118, 255))
    d.text((w - 54, 34), '×', font=font('Bold', 40), fill=(150, 150, 156, 255))
    return im
TABS = [tab_card('3 bd · 2 ba · $339,900', 'Homes for sale near me', (59, 130, 246)), tab_card('Mortgage calculator', 'What will I really pay?', (34, 197, 94)),
        tab_card('4 bd · 3 ba · $412,000', 'Open house Saturday?', (249, 115, 22)), tab_card('How much house can I afford', 'search results', (168, 85, 247)),
        tab_card('Closing costs explained', 'article · 14 min read', (20, 184, 166)), tab_card('3 bd · 2 ba · $329,500', 'Price drop!', (239, 68, 68))]
TAB_POS = [(330, 520, -6), (760, 700, 7), (300, 900, 5), (770, 1080, -8), (330, 1270, -4), (760, 1460, 6)]
def paper(label, sz=(300, 380)):
    im = Image.new('RGBA', sz, (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, sz[0] - 1, sz[1] - 1), fill=(252, 252, 248, 255)); d.text((26, 26), label, font=font('Black', 38), fill=(30, 30, 34, 255))
    for i in range(7): d.line([(26, 100 + i * 34), (sz[0] - 30 - (i % 3) * 40, 100 + i * 34)], fill=(190, 190, 196, 255), width=8)
    return im
PAPERS = [paper('W-2'), paper('PAY STUB'), paper('BANK STMT'), paper('TAX RETURN')]
PAPER_POS = [(220, 760, -14), (860, 940, 11), (260, 1350, 9), (840, 1560, -10)]
ASKS = [('MAIL', 'Gulf Coast Lending', 'Please send 2 months of bank statements', (59, 130, 246)),
        ('MESSAGES', 'Mom', 'Did you get pre-approved yet??', (34, 197, 94)),
        ('MAIL', 'Gulf Coast Lending', 'Your pay stub is missing page 2', (59, 130, 246))]
ASK_IMG = [notif_card(a) for a in ASKS]
AGAIN = notif_card(('MAIL', 'Gulf Coast Lending', 'Can you resend your W-2?', (59, 130, 246)))

def scene_chaos(img, t):
    img.alpha_composite(BG_DARK)
    s1, s2 = START['h_chaos1'], START['h_chaos2']
    shake = 10 * math.sin(t * 61) * max(0, 1 - (t - s2) / 1.0) if t > s2 else 0
    for i, tb in enumerate(TABS):                              # "forty browser tabs"
        p = (t - s1 - 0.1 - i * 0.26) / 0.45
        if p <= 0: continue
        x, y, r = TAB_POS[i]; ox = -500 if x < W / 2 else W + 500
        im = tb.rotate(lerp(r * 3, r, eout(p)), resample=Image.BICUBIC, expand=True)
        img.alpha_composite(im, (int(lerp(ox, x, back(p, 1.4)) - im.width / 2 + shake), int(y - im.height / 2)))
    if t > s1 + 3.0:                                           # "paperwork everywhere"
        for i, pp in enumerate(PAPERS):
            p = (t - s1 - 3.0 - i * 0.22) / 0.45
            if p <= 0: continue
            x, y, r = PAPER_POS[i]
            im = pp.rotate(lerp(r * 5, r, eout(p)) + 2 * math.sin(t * 2 + i), resample=Image.BICUBIC, expand=True)
            img.alpha_composite(im, (int(x - im.width / 2 + shake), int(lerp(-400, y, back(p, 1.3)) - im.height / 2)))
    dim = Image.new('RGBA', (W, H), (0, 0, 0, int(120 * ease((t - s1 - 2.0) / 0.6)))); img.alpha_composite(dim)
    for j, nimg in enumerate(ASK_IMG):                         # the asks pile up
        t0 = s1 + 1.8 + j * 0.85; p = (t - t0) / 0.4
        if p <= 0: continue
        later = sum(1 for jj in range(j + 1, len(ASK_IMG)) if t > s1 + 1.8 + jj * 0.85)
        y = lerp(-200, 210 + later * 196, eout(p)) if later == 0 else 210 + later * 196 - 196 * (1 - eout((t - (s1 + 1.8 + (j + later) * 0.85)) / 0.4))
        img.alpha_composite(nimg, (int((W - nimg.width) / 2 + shake), int(y)))
    if t > s2:                                                 # "…Again."
        red = Image.new('RGBA', (W, H), RED + (int(70 * ease((t - s2 - 1.2) / 0.3)),)); img.alpha_composite(red)
        p = (t - s2 - 0.3) / 0.35
        if p > 0: img.alpha_composite(AGAIN, (int((W - AGAIN.width) / 2 + shake), int(lerp(-200, 820, back(p, 1.3)))))
        text_c(img, 'Again.', 1240, font('Black', 190), (255, 214, 205), ease((t - s2 - 1.35) / 0.25), 0, scale=0.7 + 0.3 * back((t - s2 - 1.35) / 0.3, 2.2))
    img.alpha_composite(VIG)

def scene_turn(img, t):
    s = START['h_turn']; p = (t - s) / 0.5
    img.alpha_composite(BG_GREEN)
    if p < 1:
        old = Image.new('RGBA', (W, H)); scene_chaos(old, END['h_chaos2'] + 0.4)
        m = Image.new('L', (W, H), 255); r = int(1300 * eout(p)); ImageDraw.Draw(m).ellipse((W / 2 - r, H / 2 - r, W / 2 + r, H / 2 + r), fill=0)
        img.paste(old, (0, 0), m)
    text_c(img, "There's a better way.", 560, font('Bold', 80), CREAM, ease((t - s - 0.2) / 0.35), 30 * (1 - eout((t - s - 0.2) / 0.4)))
    q = (t - s - 1.15) / 0.5
    if q > 0:
        sz = int(300 * back(q, 1.8)); ic = icon_mrv.resize((max(1, sz), max(1, sz)), Image.LANCZOS)
        m = Image.new('L', ic.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, sz - 1, sz - 1), int(sz * .225), fill=255)
        img.paste(ic, (int(W / 2 - sz / 2), int(1080 - sz / 2)), m)
        text_c(img, 'MyRealtyVault', 1270, font('Black', 104), CREAM, ease(q * 1.5), 20 * (1 - eout(q)))
    r2 = (t - s - 2.0) / 0.4
    if r2 > 0:
        d = ImageDraw.Draw(img); f = font('Bold', 46); lab = 'Free for homeowners'; w = d.textlength(lab, font=f) + 90
        a = int(255 * min(1, r2)); y = 1440 + 25 * (1 - eout(r2))
        d.rounded_rectangle((W / 2 - w / 2, y, W / 2 + w / 2, y + 96), 48, outline=BRASS + (a,), width=4)
        d.text((W / 2 - w / 2 + 45, y + 22), lab, font=f, fill=BRASS + (a,))

def phone_in(img, t, s, name, cx=W / 2, cy=1180, frm='bottom', z=1.0, rot0=-10):
    p = (t - s + 0.15) / 0.6
    if frm == 'bottom': y = lerp(H + 700, cy, back(p, 1.2)); x = cx
    elif frm == 'right': x = lerp(W + 600, cx, eout(p)); y = cy
    else: x = lerp(-600, cx, eout(p)); y = cy
    put_phone(img, phone(name), x, y, z, lerp(rot0, 0, eout(p)))
    return x, y

def scene_plan(img, t):
    s, e = START['h_plan'], END['h_plan']
    img.alpha_composite(BG_GREEN)
    seq = [('H_a_setup', s - 1), ('H_b_setup2', s + 1.05), ('H_c_dash', s + 2.3)]
    cur = max(n for n, tt in seq if t >= tt) if t >= s - 1 else 'H_a_setup'
    phone_in(img, t, s, cur)
    for nm, key, tt in [('H_a_setup', 'a_setup', s + 0.85), ('H_b_setup2', 'b_setup2', s + 2.1)]:
        x, y = spt(TAPS[key], W / 2, 1180); tap_ring(img, x, y, (t - tt) / 0.45)
    caption(img, t, s, START['h_onestop'] - 0.1, 'Tell it your plan.', 'It builds the rest.')

def scene_afford(img, t):
    s, e = START['h_afford'], END['h_afford']
    img.alpha_composite(BG_GREEN)
    z = lerp(1.0, 1.25, ease((t - s - 1.1) / 1.2))
    off = (14 + 715 * 2 / 1920 * SCR_H) - PH / 2               # the "Up to about $316,000" box
    cy = lerp(1180, 1275, ease((t - s - 1.1) / 1.2))   # zoom in, phone top stays clear of the caption
    p = (t - s + 0.15) / 0.55
    put_phone(img, phone('H_e_calc_filled'), lerp(W + 600, W / 2, eout(p)), cy, z, lerp(10, 0, eout(p)))
    caption(img, t, s, e + 0.3, 'Know what you can afford.', 'Before you fall in love.')

def scene_steps(img, t):
    s, e = START['h_steps'], END['h_steps']
    img.alpha_composite(BG_GREEN)
    phone_in(img, t, s, 'H_f_checklist', frm='left', rot0=8)
    caption(img, t, s, e + 0.3, 'Every step.', 'In plain English.')
    q = (t - s - 1.6) / 0.45
    if q > 0: text_c(img, 'Any order. Your pace.', 430, font('SemiBold', 44), CREAM, min(1, q))

# one-stop shop: scroll the dashboard, light each tile as it's named (founder 11/10: full search experience ships at go-live)
OS_BEATS = [(1.45, ['Home search'], 'Search.'), (3.05, ['Check a neighborhood'], 'Neighborhoods.'),
            (4.65, ['Mortgage calculator', 'Cash to close'], 'Taxes & true cost.'), (6.85, ['Compare homes'], 'Compare.')]
def scene_onestop(img, t):
    s, e = START['h_onestop'], END['h_onestop']; lt = t - s
    img.alpha_composite(BG_GREEN)
    top = 700 if lt < 0.9 else lerp(700, 860, ease((lt - 0.9) / 0.6)) if lt < 2.6 else lerp(860, 1180, ease((lt - 2.6) / 0.6))
    top = int(top // 2 * 2); box = (0, top * 2, 886, top * 2 + 1920)
    p = (t - s + 0.15) / 0.6
    cx = lerp(W + 600, W / 2, eout(p)); cy = 1180
    put_phone(img, phone('H_m_full', box), cx, cy, 1.0, lerp(10, 0, eout(p)))
    act = [b for b in OS_BEATS if lt >= b[0]]
    if act:
        b0, names, word = act[-1]; k = (lt - b0)
        ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        for nm in names:
            x, y, w, h = TILES[nm]
            x0 = cx + (x * 2 / 886 * SCR_W + 14 - PW / 2); y0 = cy + ((y - top) * 2 / 1920 * SCR_H + 14 - PH / 2)
            x1 = x0 + w * 2 / 886 * SCR_W; y1 = y0 + h * 2 / 1920 * SCR_H
            g = 0.5 + 0.5 * math.sin(k * 6); a = int(255 * min(1, k / 0.2))
            d.rounded_rectangle((x0 - 6, y0 - 6, x1 + 6, y1 + 6), 26, outline=BRASS + (a,), width=7)
            d.rounded_rectangle((x0 - 14, y0 - 14, x1 + 14, y1 + 14), 32, outline=BRASS + (int(a * 0.35 * g),), width=5)
        img.alpha_composite(ov)
    a = min(eout((t - s) / 0.35), 1 - ease((t - (e + 0.2)) / 0.2))
    text_c(img, 'Your one-stop shop.', 150, font('Bold', 84), CREAM, a, 30 * (1 - eout((t - s) / 0.4)))
    if act:
        b0, _, word = act[-1]; q = (lt - b0) / 0.3
        text_c(img, word, 150 + 84 * 1.18, font('ExtraBold', 84), BRASS, a * min(1, q), 0, scale=0.75 + 0.25 * back(q, 2))

CHIPS2 = [chip('View-only', (34, 160, 90)), chip('Expires in 7 days', (34, 160, 90)), chip('See every open', (34, 160, 90))]
def scene_docs(img, t):
    s, e = START['h_docs'], END['h_docs']
    img.alpha_composite(BG_GREEN)
    name = 'H_g_docs' if t < s + 2.2 else 'H_i_share_form' if t < s + 3.7 else 'H_j_share_sent'
    phone_in(img, t, s, name, frm='right', rot0=10)
    x, y = spt(TAPS['i_share_form'], W / 2, 1180); tap_ring(img, x, y, (t - s - 3.55) / 0.45)
    if t < s + 2.3: caption(img, t, s, s + 2.3, 'Every document.', 'One private vault.')
    else: caption(img, t, s + 2.3, e + 0.5, 'Share with your lender.', 'One secure link.')
    for i, c in enumerate(CHIPS2):
        q = (t - s - 3.9 - i * 0.45) / 0.45
        if q <= 0: continue
        x2 = lerp(W / 2, [70, 400, 120][i], back(q, 1.5)); y2 = lerp(1150, [760, 1560, 1760][i], back(q, 1.5))
        img.alpha_composite(c, (int(x2), int(y2)))

def scene_agent(img, t):
    s, e = START['h_agent'], END['h_agent']
    img.alpha_composite(BG_GREEN)
    name = 'H_k_dash_agent' if t < s + 1.25 else 'H_l_agent'
    phone_in(img, t, s, name)
    x, y = spt(TAPS['k_dash_agent'], W / 2, 1180); tap_ring(img, x, y, (t - s - 1.05) / 0.45)
    caption(img, t, s, e + 0.4, 'Bring your agent in.', 'When you’re ready.')
    q = (t - s - 1.9) / 0.45
    if q > 0: text_c(img, 'They only see what you share', 430, font('SemiBold', 42), CREAM, min(1, q))

def scene_cta(img, t):
    s = START['h_cta']; img.alpha_composite(BG_GREEN)
    p = (t - s) / 0.6; sz = int(280 * back(p, 1.6)) if p > 0 else 1
    if sz > 2:
        ic = icon_mrv.resize((sz, sz), Image.LANCZOS); m = Image.new('L', ic.size, 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, sz - 1, sz - 1), int(sz * .225), fill=255); img.paste(ic, (int(W / 2 - sz / 2), int(560 - sz / 2)), m)
    text_c(img, 'MyRealtyVault', 780, font('Black', 104), CREAM, ease((t - s - 0.2) / 0.4))
    for i, (w_, col) in enumerate([('Every home.', CREAM), ('Every document.', CREAM), ('For life.', BRASS)]):
        q = (t - s - 1.05 - i * 0.5) / 0.3
        text_c(img, w_, 1010 + i * 105, font('ExtraBold', 86), col, min(1, max(0, q)), 0, scale=0.7 + 0.3 * back(q, 2))
    q = (t - s - 3.2) / 0.4
    if q > 0:
        d = ImageDraw.Draw(img); f = font('Bold', 46); lab = 'Free on the App Store today'; w = d.textlength(lab, font=f) + 110
        a = int(255 * min(1, q)); y = 1520 + 30 * (1 - eout(q))
        d.rounded_rectangle((W / 2 - w / 2, y, W / 2 + w / 2, y + 110), 55, fill=CREAM + (a,))
        d.text((W / 2 - w / 2 + 55, y + 28), lab, font=f, fill=GREEN_D + (a,))

SCENES = [(0.0, scene_cover), (COVER, scene_chaos), (START['h_turn'] - 0.02, scene_turn), (START['h_plan'] - 0.15, scene_plan), (START['h_onestop'] - 0.15, scene_onestop),
          (START['h_afford'] - 0.15, scene_afford), (START['h_steps'] - 0.15, scene_steps), (START['h_docs'] - 0.15, scene_docs),
          (START['h_agent'] - 0.15, scene_agent), (START['h_cta'] - 0.15, scene_cta)]
NOBLUR = {0, 2}

def frame(t):
    img = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    i = max(j for j, (s, _) in enumerate(SCENES) if t >= s)
    if i == 1 and t - COVER < 0.3:                             # the dream crashes to dark
        scene_chaos(img, t); q = (t - COVER) / 0.3
        ph = house(1.3 + 0.25 * eout(q)).copy(); ph.putalpha(int(255 * (1 - eout(q)))); img.alpha_composite(ph)
    else:
        SCENES[i][1](img, t)
    if i not in NOBLUR and t - SCENES[i][0] < 0.12:
        img = img.filter(ImageFilter.BoxBlur(int(14 * (1 - (t - SCENES[i][0]) / 0.12)) + 1))
    return img.convert('RGB')

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'video'
    if mode == 'stills':
        ts = [0.9, START['h_chaos1'] + 3.8, START['h_chaos2'] + 1.8, START['h_turn'] + 2.6, START['h_plan'] + 1.5, START['h_onestop'] + 2.0, START['h_onestop'] + 3.6, START['h_onestop'] + 5.5, START['h_onestop'] + 7.4, START['h_afford'] + 2.6,
              START['h_steps'] + 2.2, START['h_docs'] + 1.5, START['h_docs'] + 5.0, START['h_agent'] + 2.4, START['h_cta'] + 4.0]
        for k, tt in enumerate(ts): frame(tt).save(f'shots/hp_{k:02d}.jpg', quality=85)
        print(json.dumps({k: round(v, 2) for k, v in START.items()}), round(DUR, 2)); sys.exit()
    if mode == 'cover':
        frame(0).save('out/MRV_Promo_Homeowners_Cover_1080x1920.png'); sys.exit()
    out = 'out/promo_home_noaudio.mp4'
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-crf', '19', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', out + '.tmp.mp4'], stdin=subprocess.PIPE)
    for n in range(int(DUR * FPS)): ff.stdin.write(frame(n / FPS).tobytes())
    ff.stdin.close()
    if ff.wait() == 0: os.replace(out + '.tmp.mp4', out); print('ok', round(DUR, 2))
