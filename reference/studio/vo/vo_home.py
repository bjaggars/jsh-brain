"""Voice-over for the HOMEOWNER promo (founder 11/10: its own script, homeowner-vault screens only)."""
import json, sys
import soundfile as sf
from kokoro_onnx import Kokoro
VOICE, SPEED = 'af_heart', 1.05
LINES = [
    ('h_open',   "Buying a home should be exciting."),
    ('h_chaos1', "Instead it's forty browser tabs, a mortgage you can't figure out, and paperwork everywhere."),
    ('h_chaos2', "And everyone wants your documents. Again."),
    ('h_turn',   "There's a better way. My Realty Vault. Free for homeowners."),
    ('h_plan',   "Tell it what you want to do, and it builds your plan."),
    ('h_afford', "Know what you can comfortably afford, before you fall in love with a house."),
    ('h_steps',  "Every step, in plain English. In any order, at your own pace."),
    ('h_docs',   "Keep every document in one private vault, and share it with your lender in one secure link that expires."),
    ('h_agent',  "When you're ready, bring your agent in. They only see what you share."),
    ('h_cta',    "My Realty Vault. Every home. Every document. For life. Free on the App Store today."),
]
k = Kokoro('models/kokoro-v1.0.onnx', 'models/voices-v1.0.bin'); meta = []
for key, text in LINES:
    a, sr = k.create(text, voice=VOICE, speed=SPEED, lang='en-us'); path = f'vo_home_{key}.wav'; sf.write('vo/' + path, a, sr)
    meta.append({'key': key, 'text': text, 'file': path, 'dur': len(a) / sr, 'sr': sr}); print(key, round(len(a) / sr, 2))
json.dump(meta, open('vo/vo_home.json', 'w'), indent=1)
