# JSH Studio — videos as code

The marketing engine's production rig (doctrine: `/MARKETING.md`). Real app footage, filmed by script against a
fictional TEST tenant, composited and voiced in code — so every video **re-renders when the UI changes** instead of
being reshot. First product: MyRealtyVault. RV Warranty and JSH Expenses reuse this rig: new film set, new captures,
new scripts.

## What's here
| File | What it makes |
|---|---|
| `capture.py` | Signs in to the app as the film-set agent and captures every storyboard still + tap points (`cap/`) |
| `burst.py` | Burst-captures a fleeting moment (the showing-confirm receipt) |
| `render.py` | **A1 · Road Warrior** App Store preview — 25 s, 886×1920, captions, no VO |
| `promo.py` + `promo_audio.py` | **Agents Infomercial** — 49 s, 1080×1920, voice-over, music, SFX (founder-approved v7, 11/10/26) |
| `music.py` | Placeholder music bed for A1 (swap for a licensed track) |
| `vo/vo.py` | Voice-over lines (Kokoro-82M, voice `af_heart` @ 1.05 — founder's pick) |
| `vo/casting.py` | 4-voice casting sample |
| `filmset/` | TEST film-set notes + take-reset SQL |

## Run it
```bash
./fetch_models.sh                       # voice model + python deps (once)
python3 vo/vo.py af_heart 1.05          # voice-over → vo/
python3 promo.py stills                 # key-moment stills → shots/ (check before a full render)
python3 promo_audio.py                  # mix → out/promo_mix.wav
python3 promo.py video                  # picture → out/promo_noaudio.mp4
ffmpeg -i out/promo_noaudio.mp4 -i out/promo_mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k \
       -shortest -movflags +faststart out/MRV_Promo_AgentsInfomercial_1080x1920.mp4
```
Recapturing footage: `FILMSET_PASSWORD=… python3 login.py` once, run the app locally (`npx vite` in myhomevault with TEST env), reset the film set
(`filmset/*.sql`), then `python3 capture.py` and `python3 burst.py`. The confirm call to
`/.netlify/functions/showing-notify` is **stubbed** during capture with production's success shape — no texts or emails go out.

## Rules (founder rulings 11/10/26)
- Footage is the real app; people, clients and homes on screen are fictional (Harbor & Oak film set). Never other
  brokerages' MLS photos, never real client data.
- Opening frame gives nothing away: no logo, no punch line. MRV first appears at "There's a better way."
- Voice: Kokoro `af_heart` @ 1.05. Spell the brand "My Realty Vault" in VO text; avoid words she stumbles on
  ("real estate", "babysit").
- Opening photo `cap/house.png` must be a **licensed full-resolution** image (gitignored). The 11/10 cut used an
  unlicensed iStock preview → outputs stay marked PREVIEW until the licensed file is dropped in.
- Fonts: Inter Display (system `/usr/share/fonts/opentype/inter/`).
