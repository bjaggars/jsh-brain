# Lesson map: JSH AI Workshop Platform campus

Which screens and source files each lesson shows. A release that changes one of these files must name
the lessons on that row in its "Academy impact" line (see `ACADEMY.md`). Lesson scripts live in
`reference/academy/film/lessons.py` and `lessons_more.py`. Recorded on release R6.1.

| Module | Lesson id | Lesson | Screens shown | Source files | Flagged |
|---|---|---|---|---|---|
| 1 | signin | Sign in with your email link | Sign-in page, engagements list | SignIn.jsx, Engagements.jsx | |
| 1 | list | Read the engagements list | Engagements list | Engagements.jsx | |
| 1 | around | Find your way back | Engagement header, sticky All engagements bar | EngagementDetail.jsx, App.jsx | |
| 2 | new | Create a new engagement | Engagements list, New engagement form | Engagements.jsx, NewEngagement.jsx | |
| 2 | setup | Edit setup and rebuild the expert voices | Edit setup form | NewEngagement.jsx | |
| 2 | delete | Delete an engagement safely | Edit setup form, delete confirmation | NewEngagement.jsx | |
| 3 | prep | Prepare and pre-fill the questions | Pre-workshop questionnaire panel (preparing) | IntakePanel.jsx, IntakeInput.jsx, intakeQuestions.js | |
| 3 | send | Preview it and email the client | Questionnaire panel (send), client page | IntakePanel.jsx, IntakePage.jsx | |
| 3 | back | Bring the answers into the Blueprint | Questionnaire panel (received, answers, meeting plan) | IntakePanel.jsx | |
| 3 | tools | Know their tools before the meeting | Meeting plan, Current apps card | IntakePanel.jsx, EngagementDetail.jsx | |
| 4 | present | Present to client: the client-safe view | Engagement (JSH view and client view) | EngagementDetail.jsx, Workshop.jsx | |
| 4 | open | Work the Open-with checklist | Client workshop tab, Open with | OpeningPoints.jsx, Workshop.jsx | |
| 4 | ask | Ask the next questions | Client workshop tab, question cards | Workshop.jsx | |
| 4 | chamber | Use the JSH chamber and import call notes | JSH chamber tab | Workshop.jsx | |
| 4 | ready | Mark Workshop 1 complete | Before the prototype panel | EngagementDetail.jsx | |
| 5 | bp | Read a Blueprint card | Blueprint cards, card dialog, progress bar | EngagementDetail.jsx | |
| 5 | recs | Adopt, rework or decline a recommendation | Recommendations card | EngagementDetail.jsx | |
| 5 | assume | Confirm or correct an assumption | Assumptions card | EngagementDetail.jsx | |
| 6 | dir | Propose and approve a design direction | Prototype panel (design direction) | Prototype.jsx | |
| 6 | build | Build it and click through | Clickable prototype | Prototype.jsx | |
| 6 | comment | Comment on a spot and tweak a screen | Clickable prototype (comments) | Prototype.jsx | |
| 6 | update | Update the Blueprint from feedback | Update the Blueprint | Prototype.jsx | |
| 6 | versions | Work with versions | Versions strip | Prototype.jsx | |
| 7 | share | Create a share link for the client | Share with the client, client share page | Prototype.jsx, ShareViewer.jsx | |
| 7 | check | Run the build-readiness check | Build readiness panel, what's left | EngagementDetail.jsx | |
| 7 | export | Export the build package | Build readiness panel (export not shown) | EngagementDetail.jsx | |

Also affected by broad changes: the AWP overview film, the seven module intros, and the wrap-up
(`film/overview_full.py`, `film/intros.py`). A change to the engagement page layout or the visual theme
(`theme.css`) touches nearly every lesson.
