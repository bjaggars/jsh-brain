"""Mix: voice-over + music bed (ducked under VO) + synthesized SFX, timed from promo.py's START table."""
import json, sys
import numpy as np, soundfile as sf
sys.argv = [sys.argv[0], 'stills'] + sys.argv[1:]
import importlib.util
spec = importlib.util.spec_from_file_location('promo', 'promo.py')
SR = 48000
# pull timing without rendering: exec the timing part only
src = open('promo.py').read()
ns = {}
exec(src.split('CAP = ')[0], ns)
START, END, DUR, VOF, CUT = ns['START'], ns['END'], ns['DUR'], ns['VOF'], ns['CUT']
n = int(DUR * SR) + SR
t = np.arange(n) / SR
mix_vo = np.zeros(n); music = np.zeros(n); sfx = np.zeros(n)

def place(buf, sig, at, g=1.0):
    i = int(at * SR); j = min(n, i + len(sig))
    if i < n: buf[i:j] += g * sig[: j - i]

# voice
for k, m in VOF.items():
    a, sr = sf.read('vo/' + m['file'])
    if a.ndim > 1: a = a.mean(1)
    if sr != SR: a = np.interp(np.arange(int(len(a) * SR / sr)) * sr / SR, np.arange(len(a)), a)
    place(mix_vo, a / (np.max(np.abs(a)) + 1e-9) * 0.9, START[k])

# music: 112 BPM, tense minor for the problem, lifts to major at the turn
bpm = 112; beat = 60 / bpm
def nf(m): return 440 * 2 ** ((m - 69) / 12)
prob = [[45, 52, 57, 60], [41, 48, 53, 57], [43, 50, 55, 58], [40, 47, 52, 55]]
sol = [[48, 55, 60, 64, 71], [45, 52, 57, 60, 67], [41, 48, 57, 60, 64], [43, 50, 55, 59, 62]]
turn_t = START.get('turn', START['cta']) - 0.1
bar = beat * 4; b = 0; tt0 = 0.0
while tt0 < DUR:
    ch = (prob if tt0 < turn_t else sol)[b % 4]
    L = int((bar + 0.6) * SR); tt = np.arange(L) / SR
    env = np.minimum(1, tt / 0.25) * np.exp(-np.maximum(0, tt - bar) * 6)
    sig = sum(np.sin(2 * np.pi * nf(m + 12) * tt) + 0.25 * np.sin(2 * np.pi * nf(m + 12) * 2.002 * tt) for m in ch) * 0.045 * env
    sig += 0.09 * env * np.sin(2 * np.pi * nf(ch[0]) * tt)
    place(music, sig, tt0); tt0 += bar; b += 1
k = 0
while k * beat < DUR:
    at = k * beat; L = int(0.28 * SR); x = np.arange(L) / SR
    if at > 1.2:
        place(music, np.sin(2 * np.pi * (52 + 90 * np.exp(-x * 32)) * x) * np.exp(-x * 12), at, 0.30)          # kick
    if at > START.get('chaos1', START.get('turn', 0.6)) and k % 2 == 1:
        place(music, np.random.randn(int(0.12 * SR)) * np.exp(-np.arange(int(0.12 * SR)) / SR * 30), at, 0.05)  # snare-ish
    h = at + beat / 2; L2 = int(0.05 * SR)
    if at > START.get('chaos1', START.get('turn', 0.6)): place(music, np.random.randn(L2) * np.exp(-np.arange(L2) / SR * 70), h, 0.03)
    k += 1
# rest under the hook, a drop of silence right before the turn
music[: int(ns['COVER'] * SR)] *= 0.5
g = np.ones(n); _tt = START.get('turn', START['cta']); a0, a1 = int(max(0, _tt - 0.45) * SR), int((_tt + 0.1) * SR); g[a0:a1] = 0.15
music *= g

# duck music under the voice
vo_env = np.convolve(np.abs(mix_vo), np.ones(int(0.25 * SR)) / int(0.25 * SR), mode='same')
duck = np.where(vo_env > 0.01, 0.32, 1.0)
duck = np.convolve(duck, np.ones(int(0.2 * SR)) / int(0.2 * SR), mode='same')
music *= duck

# sfx
def whoosh(d=0.45, up=True):
    L = int(d * SR); x = np.arange(L) / SR; noise = np.random.randn(L)
    out = np.zeros(L); y = 0; fc = np.linspace(0.02, 0.35, L) if up else np.linspace(0.35, 0.02, L)
    for i in range(L): y += fc[i] * (noise[i] - y); out[i] = y
    return out * np.sin(np.pi * x / d) ** 2 * 1.8
def pop(f=880, d=0.12):
    x = np.arange(int(d * SR)) / SR; return np.sin(2 * np.pi * f * (1 + 2 * np.exp(-x * 40)) * x) * np.exp(-x * 35)
def ding(f=1320):
    x = np.arange(int(0.6 * SR)) / SR; return (np.sin(2 * np.pi * f * x) + 0.4 * np.sin(2 * np.pi * f * 2.7 * x)) * np.exp(-x * 7)
def thud():
    x = np.arange(int(0.7 * SR)) / SR; return np.sin(2 * np.pi * (40 + 60 * np.exp(-x * 9)) * x) * np.exp(-x * 4.5)
def click():
    x = np.arange(int(0.03 * SR)) / SR; return np.random.randn(len(x)) * np.exp(-x * 300)

COVER = ns['COVER']
if COVER: place(sfx, thud(), COVER, 0.55); place(sfx, whoosh(0.3, False), COVER - 0.1, 0.3)
if 'bump' in START: place(sfx, thud(), START['bump'] + 0.78, 0.7)
if 'chaos1' in START:
  s1 = START['chaos1']
  for i in range(8): place(sfx, pop(600 + 90 * i), s1 + 0.25 + i * 0.42 + 0.25, 0.22)
  for j in range(4): place(sfx, ding(1500 - j * 120), s1 + 1.6 + j * 0.75, 0.14)
  place(sfx, thud(), START['chaos2'] + 0.35, 0.3); place(sfx, whoosh(0.2), START['chaos2'] + 0.3, 0.25)                         # sticky slap
  place(sfx, thud(), START['chaos3'] + 0.05, 0.7); place(sfx, ding(990), START['chaos3'] + 0.2, 0.12)
if 'turn' in START: place(sfx, whoosh(0.7), START['turn'] - 0.05, 0.35); place(sfx, ding(1760), START['turn'] + 1.25, 0.18)
for key in ['home', 'show1', 'deal', 'brand', 'vault', 'cta']:
    if key in START: place(sfx, whoosh(0.45), max(0, START[key] - 0.2), 0.28)
if 'show1' in START:
    place(sfx, click(), START['show1'] + 1.75, 0.6); place(sfx, ding(1320), START['show1'] + 1.8, 0.16)
    for i in range(3): place(sfx, pop(1100 + 150 * i, 0.15), START.get('show2', START['show1'] + 2.25) + 0.45 + i * 0.55, 0.25)
if 'brand' in START:
    for dt in [1.05, 2.15]: place(sfx, click(), START['brand'] + dt, 0.6)
for i in range(3 if CUT == 'full' else 1): place(sfx, pop(700 + 120 * i), START['cta'] + (1.0 if CUT == 'full' else 0.85) + i * 0.42, 0.18)
place(sfx, ding(1760), START['cta'] + 0.1, 0.15)

out = mix_vo * 1.0 + music * 0.9 + sfx
fade = np.ones(n); _f = int(min(2.0, DUR / 4) * SR); fade[-_f:] = np.linspace(1, 0, _f); out *= fade
out = out[: int(DUR * SR)]
out = np.tanh(out / np.max(np.abs(out)) * 1.4) * 0.85
st = np.stack([out, np.roll(out, 120)], 1)
sf.write('out/promo_mix.wav' if CUT == 'full' else f'out/promo_mix_{CUT}.wav', st, SR); print('ok', round(DUR, 2))
