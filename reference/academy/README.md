# JSH Training Academy — clickable prototype (11/12/26)

Pilot campus: JSH AI Workshop Platform (founder: pilot on AWP before MRV). `src.html` is the page; the narration
(`lesson.mp3`, Kokoro af_heart) is inlined as base64 in place of `__AUDIO__` at publish time.
Curriculum (7 modules, 26 lessons) is written from AWP's how-to manual (`netlify/lib/productDocs.mjs`) at R6.1.
Only "Create a new engagement" plays; it is a storyboard, not real footage — AWP's Supabase host
(comtcpdhainyrjazztpj.supabase.co) is not reachable from the cloud workspace yet.
Published: https://claude.ai/artifact/V38hJrxWCTowfLhfsFToLc

## Real lessons (11/12/26)
`film/` records AWP itself: `login.py` (film-set staff login filmset.academy@jshinnovations.com on AWP's single Supabase
project; password is local only — reset it in the dashboard), `capture.py` (local dev build, Demo engagement, read-only:
jobs + functions stubbed, other clients' names replaced in the list), `lesson.py <id>` (dynamic camera, highlights,
captions, Kokoro voice-over). First lesson: `new` (Create a new engagement, 40 s).
Lesson learned: landing on an engagement with the questionnaire focus auto-creates a draft questionnaire. The capture
now never lets the create job finish. Founder ruling 11/12: manual invites only for now; automatic invites and
required training are on hold.
