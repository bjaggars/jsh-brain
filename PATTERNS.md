# JSH Patterns

Reusable designs, each with its reference implementation in MyRealtyVault
(github.com/bjaggars/myhomevault). New products COPY and adapt (Rule of
Three — see README). Listed with the reasoning that shaped them, so
copies inherit the WHY, not just the code.

## 1. Comms rail (Resend, platform-sent)
The platform sends email itself — never "open your mail app" handoffs.
- **Outbound:** Netlify functions → Resend; from
  `"<Tenant> via <Product>" <share@domain>`; branded auth emails via
  custom SMTP; ImprovMX for inbound forwarding of named addresses.
- **Reply relay:** every platform send sets Reply-To to a branded relay
  address `"<Tenant> <reply+<contactId>@log.domain>"`. Inbound webhook
  (Resend catch-all → function) logs the client's reply as INBOUND on the
  card and forwards the full message to the agent's real inbox with
  Reply-To = client + an auto-log address — so a natural inbox reply
  reaches the client AND files itself. One round-trip per hop by design;
  deeper capture belongs to a mailbox-integration tier.
- **BCC capture:** an always-on logger address for user-originated mail;
  AI quote-splitting extracts the quoted client message into its own
  attributed INBOUND entry (best-effort; never blocks the primary log).
- **Retrieval needs a full-access provider key** — webhook payloads are
  metadata-thin; the body is fetched by id (sending-tier keys 401).
- **Inbound processing order matters:** relay/special branches run BEFORE
  sender-attribution (a replying client is not a platform login).
- Reference: `netlify/functions/inbound-log.mjs`, `_relay.mjs`,
  `send-email.mjs` family.

## 2. Identity layering (person / card / participant)
- **Person** = identity: email is the login key, one auth per person.
- **Card (contact) = the relationship unit**, and it is a PARTY: person /
  household / entity, with 1..n member people (`contact_members`).
  Cache columns (email/phone) mirror the PRIMARY member via trigger —
  machine-maintained, never hand-edited; UI locks them when members
  exist. Auto-wrap trigger keeps every new person-backed card a party of
  one. Backfill = wrap existing cards (degenerate case IS the old model).
- **Participant** = the person's role on a transaction/engagement
  (primary / co-client / co-signer): multi-person was a day-one intent.
- **Greeting and audience travel together, per message:** multi-member
  cards get audience pills (whole party or one member) driving BOTH the
  salutation AND the send targets; thread entries note solo sends.
  Entities greet the human, never the LLC.
- Matching (BCC, relay, dedupe) resolves through ANY member with legacy-
  column fallback so pre-schema deploys stay green.
- Reference: script 029/030, `AgentWorkspace.jsx` PartySection,
  `smoke-party.mjs`.

## 3. Capture loop (❓ AI assist → structured backlog)
User feedback and feature requests are captured in-product with AI
assistance, dual-written: `feature_requests` table (source of truth) +
GitHub Issues (Claude-readable). CI failures self-report as Issues too —
the robot files its own bugs. Sessions read Issues as part of BRAIN
context. How-tos and defect reports ride the same rail.

## 4. Mission Control
An in-product founder console: **Quality** tab (E2E runs reported by the
robot via an e2e_runs table) and **Releases** tab (release approvals
recorded — the human gate made visible). Extend per product, keep the
two core tabs. Reference: Mission Control views + `e2e_runs`,
`release_approvals` scripts.

## 5. Deploy preflight & version stamp
Build stamps the commit sha into the app AND writes `dist/build.json`.
E2E preflight polls the deployed build.json until it matches the commit
under test. Function-cached SPA shells and deploy races die here.
Reference: `vite.config.js` stamp, build script, e2e.yml "Wait for
deploy" step.

## 6. Render engine (editorial images in serverless)
`@resvg/resvg-js` in a Netlify function renders SVG → PNG with BUNDLED
TTF fonts (`loadSystemFonts:false` → deterministic pixels), ~30ms for
display-type compositions → Cloudinary → email `<img>` / social assets.
Exists because email clients can't load webfonts; display typography
ships as rendered images with real-text body copy (deliverability).
Netlify config: `external_node_modules` for the native binary +
`included_files` for fonts. Proven 8/2/26; also renders the JSH/product
logos (generators live with the brand assets — identity is reproducible,
not a one-off PNG).

## 7. Campaign Studio architecture (design system, not design tool)
- **Brand Kit** (per tenant): type pair (display serif + script accent),
  palette, logo, PHOTO LIBRARY (load-bearing — great blocks with bad
  photos lose), voice notes.
- **Editorial Block Library:** ~12 composable blocks harvested from
  real-world best-in-class emails (display hero, eyebrow caps, script
  accent, numbered-step-over-photo, testimonial cards, phone-frame,
  vertical wordmark rail, checklist, portrait-beside-type, pill CTA,
  framed card, footer). Type-heavy blocks render as images (pattern 6);
  body blocks stay table-HTML text.
- **Claude composes; the human art-directs with words.** No WYSIWYG
  editor — that's rebuilding the incumbent's moat instead of exploiting
  ours: the DATA (stage, deadlines, party, listings) that generic email
  tools never have. Same blocks emit email + social crops.
- Sequences (triggers/delays/exit) are linear chains in observed practice
  — a vertical list UI, not a graph editor. Runner is its own phase.

## 8. Public compliance surface
Every product maintains no-auth static pages: privacy, terms, and an
`/about` describing the business and any regulated program (messaging,
data display) with evidence embedded. Static files in `public/` bypass
the SPA (redirect rule WITHOUT `!` force); extensionless aliases.
Compliance bots and reviewers must see full text without JavaScript or
login. Reference: `public/about.html`, netlify.toml redirects.

## 9. External data feeds (MLS et al.)
- Access is paperwork + approval queues: start the clocks immediately,
  build against DEMO data in parallel, swap credentials on approval.
- License obligations → build checklist in the product BRAIN on signing
  day (attribution blocks, refresh cadence, reports, DMCA).
- Importers are incremental timestamp-cursor syncs (minimal load is a
  contractual obligation, not just good manners).
- Scope check before feature use: which licensed USE covers each feature
  (IDX display vs. Participant Listings Use vs. CRM) — don't ship on a
  squint.
