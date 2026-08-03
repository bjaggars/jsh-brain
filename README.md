# JSH Brain

Shared engineering doctrine for all Jaggars Software Holdings products
(MyRealtyVault, MyBuilderVault, CampVault, Napkin, Pocket, and whatever
comes next).

## What lives here vs. in a product BRAIN
- **JSH Brain (this repo): HOW we build.** Process, patterns, stack
  conventions, hard-won lessons. Product-agnostic.
- **Product BRAIN (`docs/BRAIN/` in each product repo): WHAT the product
  is.** State, board, backlog, roadmap, product-specific learnings.

**Precedence:** for process questions, JSH Brain wins unless the product
BRAIN documents an explicit, reasoned exception. For product facts, the
product BRAIN wins, always. Conversation memory loses to both.

## Files
- `DOCTRINE.md` — the non-negotiables: deployment, database, testing,
  security, session protocol.
- `PATTERNS.md` — reusable designs with the scars that taught them:
  comms rail, identity layering, capture loops, Mission Control, render
  engine.
- `STACK.md` — the standard kit and its configuration wisdom.

## Inheritance rule (the Rule of Three)
New products COPY the reference implementations from MyRealtyVault
(github.com/bjaggars/myhomevault) and adapt — they do not import shared
code packages. We extract a true shared package only when a THIRD product
needs the same thing. Doctrine is shared from day one; code is shared only
once repetition proves the abstraction. Copy-paste inheritance plus shared
doctrine is the fast, safe road for a portfolio at this stage.

## Session protocol
Any JSH product session: read the product's BRAIN first, consult this repo
for process, update both in the same commits as the work they describe.
