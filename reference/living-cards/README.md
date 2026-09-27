# Living cards — reference implementation

Born in the JSH AI Workshop Platform (`bjaggars/ai-workshop-platform`, commit f7e9476, 9/27/26).
Doctrine: `PATTERNS.md` → "Dashboard: boxes of living cards".

- `Illo.jsx` — the illustration library: one hand-coded SVG per category, animated with CSS keyframes.
  Add a new category by adding a key to `ART`. Colors are CSS variables, never hex, so art follows the product palette and light/dark.
- `cards.css` — box, card grid, detail panel, and every animation keyframe, plus the reduced-motion kill switch.

Copy both into a product, map the product's palette onto the tokens, then draw that product's categories.
The AWP copy is the canonical source; refresh this reference when AWP's changes.
