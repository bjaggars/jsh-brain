# JSH Engineering Doctrine

The non-negotiables. Every rule here was paid for; the incident that
taught it is noted so future-us knows these are scars, not preferences.

## 1. Branches & releases
- Two branches: `dev` (Claude pushes freely) and `main` (customers).
  `main` moves ONLY via the release ritual — never a direct push.
- **Release ritual:** (1) RELEASES.md notes on dev; (2) all Actions green
  at the release sha; (3) any DB change scripts run BY BRICE on the prod
  database FIRST (new schema is invisible to old code — scripts-before-
  merge is the zero-risk order); (4) merge dev→main; (5) watch prod CI +
  Smoke + E2E to green. Founder approval precedes the merge, always.
- Hotfix-class changes (compliance pages, static fixes) use the same
  ritual, mini-sized. No "just this once" direct pushes.

## 2. Databases
- Terminology: **"DB change scripts"** in all human-facing communication
  — never "migrations." Numbered SQL files in `supabase/migrations/` are
  schema evolution scripts.
- Every script ends with `notify pgrst, 'reload schema';` (new tables/
  functions are invisible until PostgREST reloads — 8/1/26 lesson) AND a
  **prove-it query** with named PASS conditions, run and eyeballed on the
  NAMED target project. TEST first, prod only via the release ritual.
- **RLS at birth:** no table ships without its policies in the same
  script (MyRealtyVault 019/020 lesson — a naked table shipped once;
  never again). Emergency RLS hotfixes are the most expensive kind.
- One-time backfills need a companion answer for rows created AFTER the
  script: a trigger at the source, or an explicit decision not to
  (party-cards 029/030 lesson — the gap surfaced writing an E2E journey).
- Client inserts for restricted roles: beware `INSERT…RETURNING` under
  RLS; prefer client-generated `crypto.randomUUID()` without RETURNING.

## 3. Testing tiers (all products adopt all tiers)
1. **Static gates (predeploy):** `node --check` on every touched file;
   named-check audit (every handler resolves, every referenced ID exists);
   env contract check; migration sequence check. Runs locally and in CI.
2. **Behavioral smokes:** mocked-network tests through the REAL handlers
   (`scripts/smoke-*.mjs`). Green OLD smokes on NEW code paths prove
   nothing — new paths get new scenarios BEFORE the push, not after being
   asked (8/2/26 lesson). Synthetic payloads test your imagination;
   deliberately exercise fallback paths AND the happy path.
3. **E2E robot:** Playwright golden paths against the LIVE deployed site
   on every push to either branch. Deploy preflight polls `build.json`
   (sha stamped at build) until the deploy matches the commit under test.
   Failures self-report as GitHub Issues WITH ARIA snapshots — and the
   issue body is SCRUBBED of credentials before posting (snapshots
   capture textbox VALUES; the E2E password published itself once,
   8/2/26). Purge step keeps a clean floor using E2E-prefixed data names.
4. **Read the robot's confession before diagnosing.** The failure issue
   embeds the answer more often than not; the red-main "deploy race" of
   8/1/26 was actually `Invalid login credentials` printed verbatim in
   the snapshot. Trust the instrument you built.
- Verify-the-verifier: when a gate or gate-fix ships, prove the gate
  itself fires.

## 4. Code changes
- **Verify-after-write, every edit:** string replacement silently no-ops
  on stale targets; assert the change landed (grep/count) before commit.
- Component-scoped edits: location-sensitive changes need scoped anchors
  ("Delete button in the wrong component" is the canonical incident).
- Env var changes require a redeploy to bake in — functions hold values
  from deploy time. Repeated lesson; treat as law.
- Secrets: per-site AND per-context in Netlify; a secret installed on
  prod does not exist on TEST (the R10d full-access-Resend-key lesson).
  Never reuse a leaked credential — rotate to a NEW value.
- Query-string secrets: `+ & = space` are landmines (`+` decodes to a
  space server-side). Shared keys are plain alphanumeric, always.

## 5. Compliance & external reviewers
- **Reviewers must verify without credentials.** Any submission naming a
  URL (carrier campaigns, MLS applications, app stores) points at a
  PUBLIC page that answers the reviewer's checklist on its face —
  business identity, the regulated flow described precisely, evidence
  embedded (Twilio 30921 lesson, 8/2/26). The app's login wall is a
  privacy feature; explain it, don't make a reviewer hit it.
- Submission text and public pages must tell ONE story — an evidenced
  claim in a filing is never contradicted by the website (the
  "exclusively via web form" alignment, 8/2/26). When a prior filing's
  text is strong and evidenced, align the page to it, not vice versa.
- Data-license obligations become build-time checklist items in the
  product BRAIN the day the agreement is signed (MLS Grid 8/3/26:
  DMCA notice + agent registration, domains reports, refresh cadence,
  attribution blocks, breach-notification clock).

## 6. Session protocol
- **One named JSH session token** (adopted 8/3/26 after a five-token
  archaeology session): a single fine-grained PAT named recognizably
  (e.g. `JSH-session-<month>`), covering ALL product repos, with
  **Contents RW + Issues RW + Actions RW + Workflows RW**. Workflows
  write is required to push `.github/workflows/*.yml` (copying CI to a
  new product fails without it). Actions write lets Claude re-run/
  dispatch/cancel runs — deploys happen via Netlify's Git integration,
  not Actions, so blast radius is tests, not releases. Expiry: 7 days
  default, 30 acceptable. Regenerate weekly; DELETE stray tokens — the
  GitHub UI never re-shows a secret, so unnamed duplicates are
  unidentifiable risk. One token, one paste, any product session.
- Anthropic API keys are NOT session credentials: never paste in chat;
  they live in Netlify env vars only. A key exposed in chat is revoked
  at console.anthropic.com and replaced — never reused (8/3/26).
- Read the product BRAIN first; update BRAIN in the same commits as the
  work. BRAIN wins over conversation memory for product facts.
- Token scopes govern what Claude CAN do; the release ritual governs what
  Claude MAY do. Widening the first never loosens the second.

### 4b. Scripted-edit discipline (added 8/3/26 — two escapes in one day)
- A verification script that fails must STOP everything after it: chain
  edit → verify → build → commit → push with `&&`, never newlines. Both
  8/3 escapes had passing asserts and a commit that sailed anyway.
- Heredoc match strings use REAL characters (paste from the file), never
  escape sequences — `\u2019` through a quoted heredoc matches nothing.
- Anchor match strings are read from the CURRENT file immediately before
  editing, not reconstructed from memory of writing them.

### 6b. Session hygiene (added 8/3/26 — the $200/day chat-cost lesson)
- Fresh chat per work block; BRAIN carries state between them, so session
  amnesia is free. Marathon chats compound cost: every message re-processes
  the entire history.
- Breakpoint at gate-green: when a feature ships and the robot passes,
  close the session and start the next item clean.
- Heavy uploads (PDF dumps, agreements) get a dedicated short-lived chat:
  distill to BRAIN, close; the intel survives without the payload riding
  every subsequent message.
- The product's API spend is measured separately (ai_usage pattern) and is
  expected to be small; chat-session spend is a build cost, managed by the
  practices above.

## 7. Culture
- Honest assessment over cheerleading. State the caveat with the win.
- Corrections reshape doctrine — when Brice corrects architecture or
  terminology, the correction lands in BRAIN, not just the reply.
- "Scrolling is not your friend" — design law, all products.
- Survey how incumbents model the domain BEFORE designing the domain
  model; competitor products are a compressed record of a decade of
  field-driven schema corrections (party-cards lesson, 8/2/26).
  Enumerate the domain's real-world shapes at design time.
- Research spikes before builds when access/feasibility is the risk:
  kill the riskiest unknown first, keep paperwork clocks and build work
  parallel (resvg spike; MLS Grid demo-feed unlock, 8/3/26).
- Like-for-like ("Pepsi challenge") is the quality bar for anything
  replacing a tool a customer already loves: theirs beside ours,
  customer as judge.
