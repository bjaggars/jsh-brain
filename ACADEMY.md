# ACADEMY — the JSH Training Academy

Doctrine for training on every JSH product. Status, links and founder rulings: Claude Project doc
`claude/jsh-training-academy-status.md`. Prototype source and the film pipeline: `reference/academy/`.

## Why it exists
User adoption is the number one risk in product development. Every JSH product ships with its own
campus in the Academy, so people can actually use what we build. This is a JSH differentiator.

## What a campus is
1. A product overview film (about two minutes; one per audience).
2. Modules in the order people do the work. Each module opens with a short intro (optional to watch).
3. Lessons: one task each, under a minute, recorded on the real product, with a quick check.
   A lesson is complete when its quick check is answered correctly.
4. Practice inside the training window, with the steps visible beside it.
5. A wrap-up after the last lesson.

Lessons are produced from scripts (`reference/academy/film/`), not filmed by hand. That is what makes
the next rule affordable.

## THE ACADEMY LAW: every release states its Academy impact (founder, 11/12/26, all products)
Training that no longer matches the product is worse than no training. So:

1. **Every release note carries an "Academy impact" line.** One of:
   - `Academy impact: none` (no screen a lesson shows was changed), or
   - `Academy impact: <lesson ids>` with what changed on each screen.
2. **How to find the affected lessons.** Each campus keeps a lesson map: lesson id → the screens and
   source files it shows (AWP: `reference/academy/lesson-map-awp.md`). A release that touches a mapped
   file must name the mapped lessons, or say why they are unaffected.
3. **What happens next.** Named lessons are flagged in the Academy ("screen changed in <release>") and
   re-recorded from their scripts before or with the release. A wording change on a screen also means
   updating the lesson's script, steps and quick check.
4. **New screens and features.** A release that adds a screen or a task files the lesson for it in the
   same breath (NO ORPHAN HALVES applies): script it, or log it as an open loop linked to the release.
5. **Session sweep.** When a session opens on a product that has a campus, the open-loops sweep includes
   "lessons flagged and not yet re-recorded." A flagged lesson older than one release is a red.
6. **Product words win.** Lessons use the product's own terms exactly. If the product renames something,
   the lesson changes; the lesson never invents a name.

Until the Academy has its own database, the flags live in the campus's lesson map (a "Flagged" column)
and in the product BRAIN's open loops.

## Training mode by product (founder, 11/12/26)
| Product | Mode |
|---|---|
| MyRealtyVault | Instructor-led and self-study |
| JSH AI Workshop Platform (staff) | Instructor-led and self-study |
| RV Warranty | Self-study |
| MyCampVault | Self-study (probably) |
| JSH Expenses | Self-study |

## Access (founder, 11/12/26)
- JSH staff door: an internal dashboard of all campuses. The founder grants access, picks campuses and
  assigns a temporary password (changed at first sign-in, expires after 14 days).
- Product door: customers open the Academy from inside the product, or from that product's Academy link,
  with the product's own sign-in. They see only that product's campus.
- A larger customer can name its own trainer, who sees progress for that customer only.

## Filming rules (learned on the AWP campus)
- Film on demo or film-set engagements with fictional clients only. Replace real client names in any list.
- Never send an email or text to a real person while filming. Use "send the link myself" paths.
- Record every action taken on a live system in `reference/academy/film/ops/`.
- Say "Product Engineer," not "founder," in training. Say "pre-fill" (hyphenated) in voice-over.
- Quick-check answers are plain statements, never a field label or a question.
- Claims in investor-facing films are framed as JSH's belief or goal unless there is data behind them.
