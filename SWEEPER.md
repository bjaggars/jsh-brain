# The Sweeper — autonomous defect response (designed 8/5/26)

The Frontier Firm thesis applied to support: a customer defect report
becomes a tested candidate fix in minutes, ships on one founder syllable,
and closes its own loop with the customer — in JSH's voice, end to end.
Born from Brice's ask (hourly sweep agent, auto-remediate, auto-ship) and
the negotiated gate (8/5): **autonomy everywhere except the prod deploy,
which costs the founder exactly one word — for now, with an earned path
to full autonomy.**

## Lifecycle
1. **Capture** (exists): in-app ❓ → AI-structured report → feature_requests
   row + GitHub Issue (labels: bug/feature + tenant).
2. **Instant ack** (build): the capture function ALSO emails the submitter,
   JSH voice: "Got it — filed with the JSH team. Fixes are announced in
   release notes." Never names an individual. Feature requests: roadmap ack.
3. **Agent dispatch** (build): GitHub Actions on `issues: opened` w/ label
   `bug` (+ nightly cron catch-all sweep). Claude Code session: clone,
   read BRAIN + the Issue, attempt the fix ON DEV under full doctrine
   (verify-after-write, gates, BRAIN in-commit).
4. **Machine verdict** (exists): predeploy gates → behavioral smokes →
   E2E robot against the live TEST deploy.
5. **Founder summary** (build): email to JSH ops: report, root cause,
   diff summary, robot verdict, risk notes. If the fix needs a DB change
   script or exceeds the agent's lane: the email says "requires founder
   session" instead of offering ship.
6. **The gate**: founder replies "ship" (or labels the Issue `approved`).
   One word, from anywhere.
7. **Automated ritual** (build): merge dev→main per doctrine (enumerating
   the release-train range; refusing if ungated work is aboard — the 8/5
   scar as executable check), watch prod CI/Smoke/E2E to green.
8. **Closure comms** (build, fires ONLY on prod green, defect-class only):
   - Submitter email, fixed template + ONE generated sentence (civilian
     description sourced from the release note): remediated, tested, live,
     please try again. JSH voice. Bounded generation: template skeleton is
     code, not prompt output.
   - GitHub Issue closed w/ fix comment; feature_requests row → remediated.
   - BRAIN release notes updated (already in-commit from step 3).

## Trust ladder (autonomy is earned, not granted)
- Phase 1: every fix gated (step 6) — first N cycles build the record.
- Phase 2: whitelist narrow classes for full autonomy (CSS/contrast/copy/
  affordance labels — the classes robot-verifiable and low-blast-radius),
  founder gets the summary AFTER ship. Expansion by demonstrated record.
- Never autonomous: DB change scripts (founder-run by doctrine), auth/RLS
  surfaces, send-rail behavior changes, anything touching money.

## Hard rules
- "Tested" means the FULL tier stack green on the live TEST deploy — a
  robot floor, not a ceiling: visual/layout classes stay Phase-1-gated
  until visual regression exists (the grid-escape and upload-contrast
  incidents both passed a green robot).
- The customer is never told "live" before prod smoke green (the email is
  ritual step 8, not a promise issued at step 5).
- All customer-facing text says "the JSH team" — never an individual.
- Every Sweeper action lands in BRAIN + the Issue trail: the agent's work
  is auditable to the same standard as a session's.

## Build shape (MyRealtyVault first, pattern for all products)
- capture fn: + submitter ack email (small).
- .github/workflows/sweeper.yml: issue-trigger + cron, Claude Code
  harness, summary mailer (Resend), approve listener (label webhook or
  reply-to parsing on the ops address), ritual executor, closure mailer.
- Estimated: one focused build session for Phase 1 end-to-end.
