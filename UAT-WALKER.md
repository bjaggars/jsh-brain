# The UAT Walker

**What it is:** a Claude session whose job is to use the product the way a new customer would and read
every screen, so the founder does not have to do user acceptance testing at scale. Founder-ratified on
MyRealtyVault, 2026-11-19, for every JSH product.

**Why it exists:** a design-partner customer (Wendy, MRV) kept finding defects that the automatic tests
had passed. The automatic tests ask "does it work?". Nobody was asking "would a person understand this,
and does what this screen says agree with the screen before it?". The Academy filming sessions found
those defects by accident, because filming forces a session to use the product for real. The Walker
does that on purpose.

## Two kinds of testing, two names

| | SIT — the ring | UAT — the walk |
|---|---|---|
| Question | Does it work? | Would a customer understand it, and is it right? |
| Who | The automatic end-to-end tests | The Walker (a session that did NOT build the change) |
| Finds | Crashes, broken saves, broken sends | Wrong numbers, two screens that disagree, jargon, dead ends, things a real person types that the form mishandles, layout that breaks on a phone |
| Measured against | The inventory | The inventory |

Both are measured against an **inventory generated from the product's code** (every screen and every
action, grouped into areas by kind of user). Coverage is reported per area as: not walked, part, full —
separately for computer size, phone size and iPhone.

## The Walker is many people, and looks along many lines

The Walker is not one tester running one script. It is **each kind of person who uses the product**, and for
each of them it looks along **several lines at once**. A walk that only asks "did it crash?" is the ring's
job done twice. The lines below are what make it worth having.

### It walks as each role — and each role cares about different things

| Walking as | What that person cares about | What the Walker found walking as them (MRV) |
|---|---|---|
| **The professional (agent)** on a busy day | Speed, the right number, not typing things twice, nothing lost | "425k" read as $425; an offer refused with a database message; two meanings of "showings this week"; a deadline listed twice; the search that timed out |
| **Their client (buyer, seller)** who did not choose this app | Do I understand this? Is it about me? What do I do next? Can I trust the number? | "In your pocket $400,125" with no mortgage in it; "No tours booked yet" above last week's tour; the assistant telling a client with an agent that she has none; an appointment the agent booked that never reached her |
| **The homeowner** with no professional | Plain words, no jargon, honest about what the app cannot do | "No FEMA flood map here" for an address the map could not find; a calculator that misread what was typed |
| **A member of the public** arriving from a link, on a phone | Does the page load, does it say something true, can I act with a thumb? | A cancelled listing still "For sale" and taking showing requests; a main button wrapped to three lines |
| **The office manager (broker)** | Are the totals right, who needs me, can I add and remove people safely? | "jamie@" accepted as an email; a start date shown as a missed deadline; counts that disagreed between two screens |
| **The outsider let in for one job** (lender, title company, guest) | Did I get what I was promised, and nothing else? | Wrong-link pages; the document request that opened on the wrong kind of person |
| **Staff (Mission Control)** | Can I see and fix what a customer reports? | Read-only pass; the release sign-off is never touched |

Two rules follow. **A change is followed to the other side:** after acting as one role, sign in as the role
on the receiving end and look. And **each role gets its own saved login on the film set**, so the Walker
sees exactly what that person sees — never an admin's view of it.

### The lines it looks along (every screen, every role)

1. **Does it work?** Fill it the way people type. Empty, half-typed, too many, the wrong kind of file.
2. **Is it true?** Every number and every sentence. Add the parts up. Compare it with the screen before.
3. **Does it make sense to this person?** Our words or theirs? Would a new user know what this is and what
   to do next? A sentence that needs our vocabulary ("the pencil's Merge door", "monitor the funnel") is a
   finding.
4. **Do the screens agree with each other?** The same fact in two places, the same word for the same
   thing, the same count on the tile and on the page it opens.
5. **What does the other person see?** Privacy and promises: what reached the client, what should not
   have, what was promised and never arrived.
6. **Is it fast enough, as the real user?** Time it signed in as that person, not as the owner. Count the
   taps. Notice the wait.
7. **Does it fit the device?** Computer, phone, iPhone. Off the edge, too small for a thumb, cut off.
8. **Can everyone use it?** Every box and button has a name a screen reader can say.
9. **Is the help right?** Ask the assistants what a customer would ask; check the answer against the screen.
10. **Could it be better?** This is not optional. The Walker steps back and asks what would make this
    screen do its job with less effort or less doubt for the person using it — a default that is usually
    right, a question asked at the moment it matters, a name where there was a count, one row where there
    were two. It **recommends**, with the reason, in the customer's terms. Founder, 11/19: *"I really like
    how you are taking a step back to make the app better."* and *"The walker needs to be
    multi-dimensional."*

**Examples of line 10 on MRV, each proposed by the Walker and approved by the founder:** the import
preview names who is added and who is skipped instead of showing the file's first three rows; a spouse
who shares a phone number is added, not skipped as a duplicate; accepting an offer asks whether the
public page should now say "Sale pending"; "Ask for documents" opens on Lender in the Pre-approval folder;
an appointment can be shown in the client's vault with one tick; an email that still shows an old price
offers "Update this email" before it is sent; two phone numbers are labelled Office and Mobile.

A walk report therefore has three kinds of entry: **defects** (fixed), **questions for a ruling**
(held), and **recommendations** (why this would serve the person better). A walk that returns only
defects was not a full walk.

## What the Walker does

1. **Signs in as each kind of user** on the TEST site (never production): the professional, their client,
   a member of the public, the office manager, staff.
2. **Uses each area for real.** Fills forms the way people type — "425k", "$475,000", "www.site.com",
   "@handle", "352.555.0113", a half-typed email, a name with a comma, an accent, eight items where six
   are allowed, a PDF where a photo is wanted, an empty form.
3. **Reads every screen as a customer.** Every word, every number, every button name. Asks: is this
   true? Does it agree with the other screens? Would a new user know what to do next? Is any word ours
   rather than theirs?
4. **Follows a change to the other side.** After the agent does something, signs in as the client and
   checks what the client now sees (and the other way round).
5. **Checks phone size.** Sideways scrolling, anything off the edge, tap targets too small, text cut off.
6. **Asks the help assistants** real how-to questions and checks the answers against the screens.
7. **Logs every finding** in the product BRAIN with a short code, what a person sees, and whether it is
   fixed, re-walked, or waiting for a ruling.
8. **Fixes what is plainly a defect**, on the development branch only, then opens the screen again on
   TEST to confirm (the re-walk is part of the fix).
9. **Adds the check** that would have caught it, so it cannot come back.

## What the Walker may decide alone, and what it may not

The founder's standing instruction (11/19): *"Carry on and don't stop. I'll go with your recommendations
and you can show me the list when all done."* — within these limits:

- **May do without asking:** wording, labels, layout, plain bug fixes. Anything easy to undo.
- **Must list first, built the safer way:** anything that changes what a customer receives or who can see
  what.
- **Must hold for a ruling:** anything that would overturn a decision the founder already made (an
  approved design, a ratified rule). Leave the product as it is and put the question on the list.
- **Never:** ship to production, change production data, press a real Send to a real person, approve the
  founder's own sign-off screens, touch the founder's own test people.

Every choice goes on one list, `docs/BRAIN/uat/DECISIONS-FOR-REVIEW.md`, with what changed, why, and how
to undo it. The founder reviews the list at the end.

## Rules learned the hard way (MRV, 11/18–11/19)

1. **Check before you log.** Open the code or the database before calling something a defect. Several
   "defects" were the Walker's own tool (it held back a page's own lookup; it typed into the wrong box).
2. **Green gates are not a walked screen.** A build that passes every check can still crash on open.
   After any push that touches a screen, open that screen.
3. **One gate script makes every commit.** Edit → validate → build → checks → commit → push, stopping at
   the first failure (`set -euo pipefail`). A `;` or a `| tail` in a hand-typed chain let a half-applied,
   unchecked commit out twice.
4. **Write the commit message after the edit**, from the diff. A message written with the plan described
   a change that had not run.
5. **An edit script changes everything in memory, then writes.** One that stops halfway leaves half an
   edit on disk.
6. **TEST can hold real people.** MRV's TEST database carries real agents' names and emails from the MLS
   feed. The Walker's tool holds back every back-end call that could send unless it is named as safe.
7. **Say what was not seen.** A fix that passes the offline checks but has not been opened on screen is
   reported as "not yet seen on screen", every time.
8. **Report in the customer's words.** What a person sees, what they see now, what is still open. No
   code names in the summary to the founder.
9. **Put it back.** Anything changed on the film set is restored or listed as left behind.
10. **The same question asked as the signed-in user.** A database query that takes 79 ms as the owner
    took over 60 s as a signed-in agent. Measure as the user.

## What it found on MyRealtyVault in two days (so the value is on record)

Present in the released product and unnoticed until the walk: the brand-font upload was dead; a buyer's
tour-times email was never sent; a client could see a draft offer; "Search the MLS" timed out for any
search with a city and a price range (measured on the production database); the help assistant told
agents that contact import did not exist and showed raw code in three answers of seventeen; a cancelled
listing's public page went on saying "For sale" and taking showing requests; a price typed "425k" was
read as $425; clients never saw an appointment their agent booked. About 150 findings were logged in
two days; most were fixed the same day, on the development branch, for one release.

## How a product adopts the Walker

1. **Inventory.** Copy `scripts/uat-inventory.mjs` from MRV and adapt it: it reads the code and writes
   `docs/BRAIN/uat/INVENTORY.md` (screens and actions by area), fails when a screen belongs to no area,
   and can list the areas a change touches.
2. **A film set on TEST.** One made-up business with realistic data, and one saved login per kind of
   user. Never the founder's own test people.
3. **The walking tool.** Copy `scripts/uat/` from MRV: `walk.mjs` (drives a browser from a list of plain
   steps; reads a screen the way a person would; holds back sends), `ask.mjs` (puts how-to questions to
   the help assistants), `gate.sh` (the one gate).
4. **The four BRAIN files** under `docs/BRAIN/uat/`: `APPROACH.md` (the rules for this product),
   `walks.json` (what has been walked, by area), `DECISIONS-FOR-REVIEW.md`, and the findings on the
   product's BOARD.
5. **Two rounds per release.** Round 1 before release: walk the areas the change touches. Round 2 in the
   background: walk the rest. One full ring at the end, the founder's OK, one release.
6. **The customer is the scorecard.** Every defect a customer reports is traced to the check that should
   have caught it, and that check is added.

## The founder's part

Rulings, a spot check, and the set-up only he can do (a test inbox, a test phone number). The Walker
carries the rest.
