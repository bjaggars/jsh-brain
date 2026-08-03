# JSH Standard Stack

The default kit for new products. Deviations are allowed but documented
in the product BRAIN with reasoning.

## Frontend
- React + Vite. Build stamps `COMMIT_REF` (Netlify-injected) into the
  app and writes `dist/build.json` (sha + timestamp) for the preflight.
- Design law: scrolling is not your friend. Inline styles with CSS
  variables per product palette.

## Hosting & CI
- **Netlify** per product: prod site (main branch, custom .com domain,
  prod database) and TEST site (dev branch, .app domain, TEST database).
  Netlify deploys via its Git integration — GitHub Actions never deploys.
- **GitHub Actions:** CI (static gates), Smoke, E2E — on both branches.
  Runners: Node 24 (20 deprecated on GH runners, 8/2/26).
- Redirects: static files served before SPA fallback (`status = 200`,
  never `200!`); extensionless aliases for public pages.
- Functions with native modules: `[functions]` `external_node_modules`
  + `included_files` (fonts, assets).

## Database & auth
- **Supabase** (Postgres + Auth + RLS) — separate projects for prod and
  TEST, under the JSH org (consolidation of stragglers is doctrine).
- All schema via numbered DB change scripts (DOCTRINE §2). RLS at birth.
- Auth emails via custom SMTP (Resend) with branded templates.
- GoTrue admin: look up users BY ID (`/admin/users/{id}`); the list
  endpoint's `?email=` filter is a liar (pagination lesson).

## Email & comms
- **Resend**: platform sends + inbound (catch-all domain →
  `inbound-log` webhook with `?k=` shared key — plain alphanumeric).
  FULL-ACCESS key per site (retrieval needs it), named `<product>-
  <env>-full`. **ImprovMX** forwards named addresses (support@, etc.).
- **Twilio** for SMS where applicable: A2P 10DLC campaign with a public
  program page (PATTERNS §8); consent + STOP gates server-enforced.

## Media & AI
- **Cloudinary** per product (unsigned upload preset for client uploads;
  functions push rendered assets).
- **Anthropic API** in functions only (`ANTHROPIC_API_KEY`, Functions
  scope, secret): Sonnet for generation/extraction, Haiku for high-
  volume assistant chatter. AI calls are best-effort in data paths —
  never let an AI failure block a primary write.
- **@resvg/resvg-js** + bundled OFL fonts for image rendering
  (PATTERNS §6). Current editorial pair: Playfair Display + Pinyon
  Script (Ivar Fine licensing = open question, per-tenant).

## Payments
- **Stripe** (live mode under JSH LLC) where products charge.

## Repos & sessions
- One repo per product; BRAIN at `docs/BRAIN/`. This repo (jsh-brain)
  holds cross-product doctrine.
- Session PATs per DOCTRINE §6 (Contents RW, Issues RW, Actions RW).
- Brice's dev machine: locked-down corporate laptop; portable Node at
  `C:\Users\brice.jaggars\Tools\node-*`; `npm.cmd` / `netlify.cmd`
  conventions; `deploy.bat` one-click where used. Claude's sandbox can
  reach github.com/api.github.com + package registries only — live-site
  checks go through the E2E robot, not direct fetches.

## Environments checklist for a NEW product (copy-adapt from MyRealtyVault)
1. Repo + `docs/BRAIN/` seeded; dev/main branches.
2. Two Netlify sites (prod .com / TEST .app) wired to branches.
3. Two Supabase projects (JSH org); script 001 with RLS at birth.
4. Resend domain + full-access keys per env; ImprovMX; branded auth.
5. Cloudinary; ANTHROPIC_API_KEY per env.
6. CI/Smoke/E2E workflows copied; e2e agents seeded per env; secrets set
   per site AND per context; build.json stamp in place.
7. Mission Control (Quality + Releases) + e2e_runs/release_approvals.
8. Public compliance pages (privacy/terms/about) before any external
   submission names the domain.
