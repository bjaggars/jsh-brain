# MyRealtyVault campus · Agent path · lesson map

Recorded 2026-11-12/13 on TEST (`xhntyqjhvvadtavtszgi`), film-set tenant Harbor & Oak Realty, agent Ava Marshall. Dev branch build of `bjaggars/myhomevault` run locally.

Every lesson is defined in `film/../film-mrv/films.py` (one dict per film: capture, highlight, tap, headline, narration). `shoot.py` drives the app and saves captures with element boxes; `render.py` builds the film. `ops/` is the record of every action taken on the film set.

## Films

| Module | Film | Captures it depends on |
|---|---|---|
| Module 1 · Your day on one screen | Find your way around (`tour`) | home, listings_panel, office |
| Module 1 · Your day on one screen | Clear what needs you (`needs`) | home, needs_panel, attention, digest |
| Module 1 · Your day on one screen | Ask your assistant (`assistant`) | needs_panel, ask, ask_answer, home, mic |
| Module 2 · Clients | Add a client (`addclient`) | home, clients_panel, add_blank, add_filled, add_done |
| Module 2 · Clients | Work a client card (`card`) | book, card, card_note, card_saved, card_hist |
| Module 2 · Clients | Your book, pipeline and import (`pipeline`) | clients_panel, book, pipeline, reach, import |
| Module 3 · Buyers | Start a buyer profile (`buyer`) | home, buyers_panel, buyer_blank, buyer_top, buyer_bottom, buyer_created, bp |
| Module 3 · Buyers | Log a pre-approval and track a home (`preapp`) | buyers_list, bp, pre_filled, pre_saved, track_filled, track_saved |
| Module 3 · Buyers | Log a tour (`logtour`) | track_saved, tour_filled, tour_saved, bp |
| Module 4 · Listings | Create a listing (`newlisting`) | home, listings_panel, nl_blank, nl_top, nl_bottom, listings4 |
| Module 4 · Listings | Photos, story and the listing page (`page`) | nl_actions, ep_photos, ep_story, ep_save, ep_saved, lp_top, lp_2 |
| Module 4 · Listings | Log a showing and change the price (`runlisting`) | hb_detail, hb_actions, hb_showing, hb_price |
| Module 5 · Showings and calendar | Confirm a showing request (`request`) | lp_top, needs_panel, req, req_done, cal_list |
| Module 5 · Showings and calendar | Use the calendar and add a task (`calendar`) | show_panel, cal_week, cal_list, cal_new, cal_task |
| Module 6 · Closings and documents | Follow a closing (`closing`) | home, closings, closing_detail, deadlines, attention |
| Module 6 · Closings and documents | Add a document to a client's vault (`vault`) | home, docs_panel, vault_filled, vault_done, vaults |
| Module 7 · Marketing | Create an open house sign-in form (`form`) | home, mkt_panel, forms, form_pick, form_draft, form_live |
| Module 7 · Marketing | Create a just listed email (`campaign`) | mkt_panel, emails, camp_moment, camp_ready, camp_made |
| Module 7 · Marketing | Workflows and results (`results`) | mkt_panel, flows, results |
| Module 1 · Your day on one screen | Your day on one screen (`intro1`) | home, attention, ask_answer |
| Module 2 · Clients | Clients (`intro2`) | book, card_note, pipeline |
| Module 3 · Buyers | Buyers (`intro3`) | bp, pre_saved, tour_saved |
| Module 4 · Listings | Listings (`intro4`) | listings4, lp_top, hb_actions |
| Module 5 · Showings and calendar | Showings and calendar (`intro5`) | req, cal_list |
| Module 6 · Closings and documents | Closings and documents (`intro6`) | closing_detail, deadlines, vaults |
| Module 7 · Marketing | Marketing (`intro7`) | mkt_panel, form_live, camp_made, results |
| Start here | MyRealtyVault for agents (`overview`) | home, attention, card, bp, lp_top, cal_list, vaults, camp_made, ask_answer |
| Agent path complete | You are ready (`wrap`) | home, attention |

## Film-set data created for the lessons (TEST only)

- Royalty-free Pexels photos on the three seeded listings and the new one (`property_photos`, `properties.photo_url`).
- Client Elena Park (buyer profile, pre-approval with Gulf Coast Lending, tracked home 2204 SE 9th Street, one logged tour).
- Listing 305 Cypress Hollow Lane for seller Owen Bradley (story, highlights, three photos; sqft set by hand because the form dropped `1,860` with a comma).
- A note on Maya Ellis, a logged showing with feedback on 88 Heron Bend Drive, a confirmed showing request, one task, one sample PDF in Owen Bradley's vault, an open house sign-in form (published), one draft just listed campaign (never sent).
- Nothing was emailed or texted. Netlify functions are stubbed in `shoot.py`; only `landing-page`, `assistant`, `compose-campaign` and `render-campaign` were proxied to the TEST site, each for one capture.
- A real person's name that exists in the film-set tenant is masked on screen as Jordan Avery (see `MASK` in `shoot.py`). The record itself was not changed.

## Product findings while filming (for the MRV robot)

1. New listing form: Sqft typed as `1,860` is saved as empty. Either accept commas or reject with a message.
2. Ask your assistant: answers that contain a markdown table show the raw pipes and dashes on the phone.
3. Campaign review shows `Rendered in undefinedms` when the render call has not returned.
4. Listing detail says `For sale, 6 days on market` on a listing created today (the public page too).
5. Form editor on a phone is a desktop layout squeezed into the screen; the lesson skips editing for that reason.
6. The film-set tenant holds a client record with the founder's real name and a family email address. Rename or remove it from the film set.
7. Pre-approval form placeholders name a real lender (`Synovus Mortgage`, `loans@synovus.com`).
8. Tapping a later stage on a buyer's step bar (Inspection) made no change and gave no message.

## Homeowner path (recorded 2026-11-13)

Scripts in `film-mrv/films_home.py`, captures in `caph/`. Filmed as the film-set homeowner Jordan Avery (no agent attached). Render with `FILMS=films_home python3 render.py all`; capture with `STATE=state.home.json CAP=caph python3 shoot.py ops/h*.json`.

| Module | Film | Captures it depends on |
|---|---|---|
| Module 1 · Your vault | Find your way around your vault (`h_tour`) | home, home2, home3 |
| Module 1 · Your vault | Use your checklist (`h_check`) | home, check, check_done, check2 |
| Module 2 · Buying a home | Work out what you can afford (`h_afford`) | home, afford, home2, mort, mort2 |
| Module 2 · Buying a home | Search for homes and save the ones you like (`h_search`) | home2, search, search2, search3, saved, rate, rate_done |
| Module 2 · Buying a home | Check a neighborhood (`h_hood`) | hood, hood2, hood3 |
| Module 3 · Your documents | Keep your documents in your vault (`h_docs`) | home2, docs, doc_add, doc_saved |
| Module 3 · Your documents | Share documents with a lender (`h_lender`) | home2, lender, lender2, lender3, lender_links |
| Module 4 · Selling and owning | Thinking of selling (`h_sell`) | home, sell, sell2, walk |
| Module 4 · Selling and owning | Your home and its records (`h_own`) | home, own, myhome1, myhome2, own2, tax, maint |
| Module 5 · Help, and your agent | Ask MRV (`h_ask`) | home, ask, ask2 |
| Module 5 · Help, and your agent | Keep your dates on My calendar (`h_cal`) | home3, cal, cal1, cal2 |
| Module 5 · Help, and your agent | Add your agent (`h_agent`) | home3, agent, rate_done |
| Module 1 · Your vault | Your vault (`h_intro1`) | home, check |
| Module 2 · Buying a home | Buying a home (`h_intro2`) | afford, rate_done, hood3 |
| Module 3 · Your documents | Your documents (`h_intro3`) | doc_saved, lender_links |
| Module 4 · Selling and owning | Selling and owning (`h_intro4`) | walk, myhome2 |
| Module 5 · Help, and your agent | Help, and your agent (`h_intro5`) | ask2, agent, cal2 |
| Start here | MyRealtyVault for homeowners (`h_overview`) | home, check, afford, rate_done, lender_links, walk, ask2 |
| Homeowner path complete | Your vault is ready (`h_wrap`) | home, check_done |

### Film-set data created for the homeowner lessons (TEST only)

- Two saved homes (305 Cypress Hollow Lane, 88 Heron Bend Drive) with film-set details and Pexels photos; one rated Love it with a note.
- One checklist step marked done; one sample PDF (Homeowners insurance policy) in Documents; a home on file (2714 Laurel Run Drive); one calendar entry.
- One lender share link to `loans@example.com` (Gulf Coast Lending). TEST reported that the email did not go out; the link exists and is listed.
- Check a neighborhood was run once for a public building's address (110 SE Watula Ave, Ocala). Add your agent was filled in but not submitted.
- Functions proxied to the TEST site for single captures: `link-preview`, `home-data`, `packet-create`, `ask-vault`.

### Product findings while filming the homeowner path

9. Saving our own listing page by link (`/l/<slug>`) lands as `Price not listed · Address unknown`; link preview does not read MyRealtyVault's own pages.
10. My home: a purchase date entered as Jun 14 shows as Jun 13 (time-zone shift on a date-only field).
11. The buying checklist says `1 of 24` on its own page and `1 of 25` on the vault home.
12. Share with a lender on TEST: `The link was created, but the email didn't go out` for an example.com address. Expected on TEST, but the two-line message reads like a failure.

## Agent path, second batch (recorded 2026-11-13)

Scripts in `film-mrv/films_agent2.py`, captures in `capa/`. Render with `FILMS=films_agent2 python3 render.py all`. Adds one lesson to Module 2, two to Module 3, and a new Module 8 (Your office) with its intro.

| Module | Film | Captures it depends on |
|---|---|---|
| Module 2 · Clients | Email or text a client (`a_msg`) | mail0, mail1, text1 |
| Module 3 · Buyers | Suggest a home to your buyer (`a_suggest`) | bp, suggest, suggest_done |
| Module 3 · Buyers | Draft an offer (`a_offer`) | bp, offer1, offer2, offer3, offer5, offer4 |
| Module 8 · Your office | Read your reports (`a_reports`) | reports, week, comm, comm2, comm3 |
| Module 8 · Your office | Set up your card (`a_card`) | profile, card0, card1 |
| Module 8 · Your office | Choose your look (`a_look`) | profile, look, look_dark, home_dark |
| Module 8 · Your office | Put your showings on your own calendar (`a_connect`) | profile, conn, weekly0, weekly |
| Module 8 · Your office | Build your bench (`a_bench`) | profile, bench0, bench1, bench2 |
| Module 8 · Your office | Get help and send feedback (`a_help`) | help, help2 |
| Module 8 · Your office | Your office (`intro8`) | reports, look, bench2 |

Film-set changes (TEST): one suggested home and one draft offer on Elena Park; profile card filled in for Ava Marshall; Grace Whitfield's commission percent corrected from 0.03 to 3 through the app; Dana Whitlock (Gulf Coast Lending) added to the bench. Weekly summary was switched to Monday for the capture and switched back to Off. Dark and Gold were previewed and not saved.
Not filmed on purpose: MLS search results (TEST holds real MLS listings and photos; founder ruling 10/1 keeps other brokerages' MLS photos out of our films). Still not covered: Outlook and SkySlope connections, sign-in and security, tab order, team and broker features.
Defects from all three batches are logged in the MRV Brain: `myhomevault/docs/BRAIN/BOARD.md` → Academy film-set findings (AF-1 to AF-16).
