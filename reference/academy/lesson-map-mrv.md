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
