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

### 1b. The dev branch is a release train (added 8/5/26)
- Everything on dev ships TOGETHER. Before any merge to main, enumerate
  the full commit range (git log main..dev --oneline) and confirm every
  release in it is gated — "merge the hotfix" is not a thing the merge
  button can do once other work has landed on dev.
- When prod needs a fix while dev carries ungated work: branch the hotfix
  FROM MAIN, merge that branch to main, then merge main back to dev.
- "All Actions green" means every workflow CONCLUDED green at the release
  sha — a run still in progress is not green (8/5: merged on Smoke-only;
  prod's own E2E happened to pass; luck is not process).
- Scar: 8/5 — a two-file PDF hotfix merge carried an ungated release
  (schema-tolerant reads + a guarded write button kept prod safe; the
  doctrine exists so safety never depends on those accidents).

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
  **Contents RW + Issues RW + Actions RW + Workflows RW + Pull requests
  RW**. Workflows write is required to push `.github/workflows/*.yml`
  (copying CI to a new product fails without it). Checks is NOT in the
  set because fine-grained PATs cannot be granted it (GitHub offers no
  Checks permission on PATs — learned 8/8 hunting a "missing scope");
  check-run/annotation reads happen INSIDE workflows via GITHUB_TOKEN
  with a `checks: read` permissions block, never from a session token. Actions write lets Claude re-run/
  dispatch/cancel runs — deploys happen via Netlify's Git integration,
  not Actions, so blast radius is tests, not releases. Expiry: 7 days
  default, 30 acceptable. Regenerate weekly; DELETE stray tokens — the
  GitHub UI never re-shows a secret, so unnamed duplicates are
  unidentifiable risk. One token, one paste, any product session.
  **Pasting the session PAT in chat is its normal delivery mechanism and
  never triggers rotation** — rotation is CALENDAR-driven (the weekly
  regenerate) or compromise-driven, never paste-driven (8/10/26: the
  end-of-session "rotate the PAT" nag misapplied the API-key rule; killed).
  Preferred delivery: the token lives in the Claude Project's custom
  instructions, updated once at each weekly rotation — one paste per week,
  not per chat.
- **Walk it before the walker** (adopted 8/10/26, Brice's CDO tenet: test
  the UAT cases BEFORE the client does — satisfaction and trust compound
  when the client's walk finds nothing). The Testing tab is Brice's UAT;
  every card is pre-walked by Claude before the walk is handed over:
  smokes locally, probes against the DEPLOYED endpoints (every new
  endpoint ships with one), and the surface's E2E golden path in CI —
  and Claude WATCHES the Actions runs to green via the API before
  reporting "ready to walk." The build container cannot reach the TEST
  site directly; the Actions API is Claude's eyes on the deployed truth.
  A red CI run means the walk is not offered, full stop. Only judgment
  and feel remain for the human gate — machine-checkable steps arriving
  broken to Brice is a delivery failure, not a testing failure.
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

---

## §8 · The North Star and the step-back discipline (added 2026-08-05, from the MBV Phase A/B marathon)

**North star:** every JSH product aims to be the most advanced platform in its
market. What incumbents do is the BASELINE — the floor we audit against, never
the target. We take the baseline to the next level.

**The failure mode this guards against — "going through the motions":**
building the increment the last increment implies. Canonical incident: MBV
personas were designed as five access tiers until a forced step-back with real
domain research grew them to 28, surfaced two missing subsystems (work orders,
time entries), and exposed that dashboard customization — table stakes for
decades — was absent from the design.

**The discipline:**
1. **Step-back checkpoint at every new surface or subsystem boundary.** Before
   designing, answer in writing: what do the market leaders do here (research,
   not memory), what is table stakes, and what is the level beyond it?
2. **Table-stakes audit is a named design step.** Missing something the
   industry has had for decades is a defect, not an oversight.
3. **Rich UI experience is a requirement, not polish.** Information density,
   motion, hierarchy — the design laws below are the accumulating bar.
4. **The trigger signal:** when a design feels like filling in a template,
   stop. That feeling IS the checkpoint bell. Scope: surface/subsystem
   boundaries — not every ticket; step-back everywhere is paralysis.
5. **The parity brief is a WRITTEN artifact, and it audits the EXPERIENCE,
   not just the artifact** (added 8/10/26 — second incident: MRV Marketing
   Studio S3). The Studio shipped with a describe-then-render loop while
   Flodesk — the NAMED north star — is a direct-manipulation editor; the
   Pepsi challenge had been defined output-side only (does our render match
   theirs) and nobody defined experience-side parity (does MAKING it feel
   as good). Root biases, named so they can be caught: differentiator-
   before-table-stakes (the AI door before the editor; users leave a loved
   incumbent only for a tool that takes nothing away — the AI is why they
   try it, the editor is why they stay); gate tunnel vision (built to pass
   the Testing card, and the gate became the ceiling); and silent
   sequencing-by-build-cost (the cheaper UX shipped without the trade-off
   ever being surfaced as a founder decision). THE RULE: when a named
   incumbent exists, every surface build OPENS with a gesture-parity table
   — their gesture beside ours, row by row — and every row where ours is
   worse gets explicit founder sign-off as accepted debt, or gets built.
   Approving mockups is not approving the trade; the comparison IS the
   decision.

## §9 · Design laws (graduated from MBV LEARNINGS #11/#12, 2026-08-05)
- **Scrolling is not your friend** (founding law; restated for completeness).
- **No voids:** wide list rows are columnar grids filled with what the user
  actually scans (client, location, status, recency) with a header row —
  never content-left, lone-badge-right across a desert.
- **Every count is a door:** any box showing a count opens onto exactly what
  is enclosed — a drawer or detail of those items, never an adjacent page.
- **Personas define defaults, not prescriptions:** dashboards are widget
  catalogs; persona picks the starting layout; the seat customizes and
  persists.

## §10. Delivery: runnable scripts arrive in chat, always
Any DB change script or seed addendum Brice needs to run is ALWAYS pasted
in full in the chat — generated by cat-ing the committed file (byte-identical,
sha256 noted) — never delivered as "it's in the repo, go look." Brice should
never have to dig for something he has to run. (Standing practice, Brice
8/5/26; mechanics per MBV LEARNINGS #14: chat copy is GENERATED from the
committed file, never typed fresh, so drift is impossible.)
Refinement (8/5/26, same day): the paste goes in the MESSAGE BODY as a code
block — tool/console output can render collapsed in the chat client and
Brice won't see it. If it was delivered via a cat command, paste it again
as message text.

## §11 · The BRAIN as a positioning asset (Brice, 8/5/26)
The BRAIN pattern is not just internal tooling — it is Frontier Firm
differentiation, in Brice's own words: it keeps token usage down, expands
effective "memory" capacity, and keeps KT, key decisions, architecture, and
domain expertise at our fingertips.

**The pitch language (client-facing):**
- "Our AI doesn't just remember your project — it maintains an auditable
  engineering record: every architecture decision with its reasoning, every
  incident distilled into a standing rule, versioned in your repo."
- Token economics: a cold AI session burns its budget re-deriving old
  decisions; a BRAIN session reads distilled state in seconds and spends the
  entire budget on NEW work. Same context window, radically different yield.
- Compounding: one debugging afternoon becomes forty lines of LEARNINGS that
  nobody ever pays for again.
- Knowledge transfer: onboarding artifacts exist from day one — institutional
  knowledge is diffable and survives any person or session boundary. Most
  shops' domain expertise lives in one head; a JSH build's lives in git.

**The honest caveat that keeps it true (and belongs in the pitch — rigor
sells):** a BRAIN is only as good as its write discipline. Stale memory is
worse than no memory because it lies with confidence. The load-bearing rule
is "update the BRAIN in the same commits as the work" — memory as a
transaction, not an afterthought. JSH engagements ship WITH this discipline;
that is part of what the fixed price buys.

**Provenance note:** convergent with industry patterns (CLAUDE.md, AGENTS.md,
memory-bank files) but JSH doctrine adds what those lack: precedence rules
(BRAIN wins over conversation memory), same-commit write discipline,
incident-derived LEARNINGS law, two-tier product+shared structure, and
prove-it evidence woven into state.

## §12 · The pause ritual (Brice, 8/5/26)
A JSH product is never "abandoned" — it is paused, and a pause is an act,
not an absence. The BRAIN is what makes pausing safe: a product with a
current BRAIN can sleep for months and resume (by Brice, a future session,
or a new engineer) without the archaeology tax.

**Pausing a product (last session before the shelf):**
1. Distill: STATE brought to current truth; BOARD priorities re-ranked with
   a one-line "resume here first"; anything RUN-pending resolved or marked.
2. Sweep the loose ends: no uncommitted work, no un-pasted scripts, CI green
   at the resting sha (recorded in STATE).
3. Note the keys: which infra (Supabase/Netlify/DNS/etc.) the product
   touches, so resume day knows what access to check — names only, never
   secrets in the repo.

**Resuming:** read BRAIN first, run the quality rail against the resting
sha before building anything new, and trust STATE only as far as its date —
the world (deps, APIs, Twilio campaigns) moves while products sleep.

**Corollary:** a product WITHOUT a BRAIN cannot be safely paused — it can
only decay. CampVault and SiteVault remain in this state until they get the
distillation pass; that is technical debt of the memory system, tracked here.

## §13 · Sweep precedence (Brice, 8/9/26 — standing until further notice)
**The issue sweep is the FIRST act of every session and takes precedence
over the session's planned agenda.** Before any build work — before even
presenting the plan — sweep open GitHub Issues on the product repo and
report what's there. If the sweep surfaces customer-filed bugs or verdicts
(e.g. a Lighthouse partner confirming or failing a shipped fix), those are
triaged with Brice BEFORE the planned work begins; the agenda yields.

Why this is doctrine and not habit: customers file when something is
broken FOR THEM, right now. A session that builds features for two hours
on top of an unread bug report has its priorities inverted — the pipeline
sells outcomes, and a customer waiting on a known break is the outcome
that matters most. The Sweeper automates part of this for machine-fixable
defects; the session sweep is the human-judgment layer above it.

Scope: applies to every JSH product session, every product, until Brice
says otherwise. The sweep result is always reported even when empty
("no new issues") so silence is never ambiguous.

## §14 · The Walk Brief (Brice, 8/14/26 — founder-ratified format, all products)

When a build completes and a founder walk opens, the OFFER of the walk is a
**Walk Brief** in this exact shape. Brice: "This is the type of format I'd
like to see when you have built something and I need to test."

**Part 1 — What's new, from the USER'S perspective.** A high-level bullet
summary written as the product's end user (the agent, the builder, the
camper-owner) would experience it:
- Grouped under short experience-area headers that follow the user's journey
  (e.g. Getting started · Designing · Your audience · Sending), never the
  system's architecture.
- Each bullet = something they can now DO, in plain language. Gesture and
  button names in **bold**, exactly as the surface prints them.
- Engine words never appear (no executor, resolver, rehydrate, RLS, bundle,
  webhook — see the agent-language riders). If a bullet can't be written
  without an engine word, the SURFACE copy is wrong, not the brief.
- Benefits stated as promises the walk can verify ("the facts line always
  shows the listing's real numbers"), not implementation notes.

**Part 2 — Test-execution context.** Immediately after the bullets, the
founder gets everything needed to actually run the walk, without hunting:
- WHERE: which environment/site and which database (named project ref),
  and which tenant/login if it matters.
- PRECONDITIONS: every DB change script and seed the walk depends on, each
  with RUN/not-run status — anything not yet RUN is pasted in full with
  checksum right there (§10: runnable scripts arrive in chat, always).
- THE CARD: which Testing card routes the walk and where it lives; which
  section to walk first.
- DIVISION OF PROOF: what the robot already proved green (so the founder
  doesn't re-walk it) vs. what only human eyes/inbox/phone can verify —
  the founder's list is the walk.
- CARRIED ITEMS: anything riding the walk from prior sessions (open
  verifications, one-glance checks) named explicitly.

The Walk Brief is the offer, not the checklist — the TESTING card remains
the checklist of record. Applies to every JSH product.

## §15 · The deploy layer is inside the release perimeter (8/14/26, from the MRV branch-config incident)
A repo can obey dev/main discipline perfectly while the deploy layer routes
around it: MRV's prod Netlify site had PRODUCTION BRANCH = dev, so every dev
push deployed to prod and the ship-merge to main deployed nothing. RULES,
all products: (1) a ship is complete only when the prod site is VERIFIED to
track main and to be serving the merge sha (build.json or equivalent);
(2) deploy-layer config changes (branch tracking, build commands, env vars)
are release-perimeter changes — never assumed, always verified at ritual
time; (3) every gate's verdict must land on a surface Claude can read
(issues/API), never only in logs Claude cannot download.

## §16 · The size gate: BRAIN files are read bounded, or not at all (8/14/26, from the MRV three-dead-chats incident)

INCIDENT: three consecutive MyRealtyVault sessions died mid-response at the
same point — the BRAIN-first opening read. Root cause was not corruption but
VOLUME + ORDER: STATE.md had grown to 72KB with session sections physically
scrambled (newest entries mid-file, "supersedes above/below" pointers in both
directions), so "read from the last closing stamp forward" was unexecutable
without ingesting the entire ~360KB BRAIN corpus. Each session exhausted its
context during the opening report, after its work landed — deterministic,
reproducible, silent.

RULES (all products, session-open and session-close):

1. **Newest-first is law.** Every session-log/STATE file keeps its newest
   entry at the TOP, directly under the header. The closing stamp is the
   first section a reader meets. "Read from the stamp" means "read the top."
2. **Size audit before any read.** Session-open runs `ls -laS` (or
   equivalent) on the BRAIN directory BEFORE reading content. Any file over
   ~100KB or any binary in the BRAIN read path is reported to the founder
   before proceeding — never read wholesale.
3. **The 20KB ceiling.** When the live STATE file passes ~20KB at session
   close, rotation is part of the close: everything below the current arc
   moves to a dated `STATE-ARCHIVE-*.md`, verbatim, nothing edited. Archives
   are never read at session-open unless a live section explicitly points
   into them.
4. **Bounded reads for the reference files.** LEARNINGS / TESTING / BOARD /
   BACKLOG are read by targeted grep or section at session-open, never
   wholesale. Wholesale reads of reference files require a stated reason.
5. **No bulk artifacts in the live log.** Pasted scripts, prove-it output,
   screenshots-as-text, and other bulk payloads go to dedicated files
   (intel-*.md, archive files, repo assets) — the live STATE file carries
   pointers, not payloads. Binaries never live inside the BRAIN read path.
6. **Consolidate same-day sprawl at close.** Multiple sections written for
   the same session/day collapse into one coherent record at session close;
   raw originals move to the archive.

The BRAIN exists to make sessions cheap to open. A BRAIN that kills the
session that reads it has inverted its own purpose.
