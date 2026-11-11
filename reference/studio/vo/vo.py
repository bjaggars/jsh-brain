"""Voice-over for the MRV infomercial promo. One WAV per line so the edit is timed to the voice."""
import json, sys
import soundfile as sf
from kokoro_onnx import Kokoro

VOICE = sys.argv[1] if len(sys.argv) > 1 else 'af_heart'
SPEED = float(sys.argv[2]) if len(sys.argv) > 2 else 1.05
LINES = [
    ('hook',   "You didn't become an agent to fight with software."),
    ('chaos1', "One app for your contacts. Another for showings. Texts over here, emails over there..."),
    ('chaos2', "and your deadlines? On a sticky note."),
    ('chaos3', "Every text you miss is a showing you lose."),
    ('turn',   "There's a better way. Meet My Realty Vault."),
    ('home',   "Your whole business, on one screen. Built for agents on the go."),
    ('show1',  "A showing request comes in. One tap to confirm."),
    ('show2',  "Your buyer gets a text and an email, and the seller stays in the loop. Automatically."),
    ('deal',   "Every deal. Every deadline. Tracked from contract to close."),
    ('brand',  "And it wears your brand, not ours. White or dark. Your color."),
    ('vault',  "Your clients get a vault of their own, so when the deal closes, you're still on their phone."),
    ('cta',    "My Realty Vault. Every home. Every deal. One vault. Get it on the App Store today."),
    # cut-downs
    ('cta15',  "My Realty Vault. Every home. Every deal. One vault. Get it on the App Store today."),  # speed 1.14 in the 15 s cut
    ('bump',   "Stop fighting your software."),
    ('cta6',   "My Realty Vault. One vault."),
]
ONLY = sys.argv[3].split(',') if len(sys.argv) > 3 else None
k = Kokoro('models/kokoro-v1.0.onnx', 'models/voices-v1.0.bin')
import os
meta = json.load(open(f'vo/vo_{VOICE}.json')) if ONLY and os.path.exists(f'vo/vo_{VOICE}.json') else []
meta = [m for m in meta if not ONLY or m['key'] not in ONLY]
for key, text in LINES:
    if ONLY and key not in ONLY: continue
    audio, sr = k.create(text, voice=VOICE, speed=SPEED, lang='en-us')
    path = f'vo_{VOICE}_{key}.wav'; sf.write('vo/' + path, audio, sr)  # path is relative to vo/
    meta.append({'key': key, 'text': text, 'file': path, 'dur': len(audio) / sr, 'sr': sr})
    print(key, round(len(audio) / sr, 2))
json.dump(meta, open(f'vo/vo_{VOICE}.json', 'w'), indent=1)
