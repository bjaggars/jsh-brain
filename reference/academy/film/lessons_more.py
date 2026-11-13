# The remaining Facilitator-path lessons. Imported by lessons.py (kept separate so the beat list is easy to edit).
WIDE=((0,0,1440),(70,40,1300)); DLG=((180,0,1080),(300,60,900))
M1,M2,M3,M4,M5,M6,M7=['Module %d · %s'%(i+1,n) for i,n in enumerate(['Get in and get around','Start an engagement','The pre-workshop questionnaire','Run Workshop 1','Read and shape the Blueprint','Build the prototype','Share and hand off'])]
def L_(title,module,file,beats): return dict(title=title,module=module,file=file,beats=[dict(shot=b[0],cam=b[1],hl=b[2],cap=b[3],vo=b[4],**(b[5] if len(b)>5 else {})) for b in beats])
MORE={
 'signin':L_('Sign in with your email link',M1,'Sign_in',[
   ('signin',((0,0,1440),(90,50,760)),[(138,168,440,62)],'Enter your JSH email',"Go to the Workshop Platform, and enter your JSH email address."),
   ('signin',((90,50,760),(90,50,760)),[(457,172,114,54)],'Choose Send link',"Choose Send link. A sign-in link arrives in your inbox.",dict(click=(461,176,105,46))),
   ('list',WIDE,[],'One link per device',"Open the link, and you're in. You stay signed in on that browser. A new device just needs a new link.")]),
 'list':L_('Read the engagements list',M1,'Read_the_engagements_list',[
   ('list',((0,0,1440),(100,60,1240)),[(144,186,1152,245)],'Every client engagement, in one list',"All engagements lists every client engagement, with its client, industry and stage on the right."),
   ('list',((100,60,1240),(100,180,1000)),[(144,388,470,36)],'Tags show where things stand',"Tags show where things stand. Demo marks the practice engagement, and the questionnaire tags tell you if it's to send, sent, or back."),
   ('list',((100,180,1000),(100,180,1000)),[(144,388,470,36)],'Choose an engagement to open it',"Choose any engagement to open it.",dict(click=(144,394,200,24),shot2='top2'))]),
 'around':L_('Find your way back',M1,'Find_your_way_back',[
   ('fs_top',((0,0,1440),(60,40,1000)),[(144,83,148,36)],'All engagements, top left',"Inside an engagement, All engagements sits at the top left."),
   ('q_round',((0,0,1440),(60,0,1000)),[(138,6,170,36)],'It stays with you as you scroll',"It stays in view as you scroll, so home is always one click away."),
   ('fs_top',((0,0,1440),(60,40,1000)),[(144,143,620,50)],'Every engagement has its own address',"Every engagement has its own address, so you can bookmark it, or use your browser's Back button.")]),
 'setup':L_('Edit setup and rebuild the expert voices',M2,'Edit_setup',[
   ('fs_top',((0,0,1440),(200,60,1040)),[(535.6,228,76,36)],'Choose Edit setup',"Next to the client line, choose Edit setup.",dict(click=(535.6,228,76,36),shot2='fs_setup_a')),
   ('fs_setup_a',((200,0,1040),(260,20,800)),[(381,103,560,480)],'Name, client, industry, purpose',"Change the name, the client, the industry, or what the app should do."),
   ('fs_setup_b',((260,20,800),(260,150,800)),[(383,234,556,137),(383,387,556,161)],'Starting point, and who answers what',"Set where they're starting from, and who answers what. Changing who answers what re-routes the sections."),
   ('fs_setup_b',((260,150,800),(260,220,800)),[(381,564,560,48)],'Rebuild the expert voices',"If you change the industry, the client, or the purpose, tick Rebuild the expert voices so they match. It's logged as a decision."),
   ('fs_setup_b',((260,220,800),(260,220,800)),[(381,636,118,44)],'Save setup',"Then choose Save setup.",dict(click=(381,636,118,44)))]),
 'delete':L_('Delete an engagement safely',M2,'Delete_an_engagement',[
   ('fs_setup_b',((260,150,800),(260,330,800)),[(381,729,560,36)],'At the bottom of Edit setup',"At the bottom of Edit setup, choose Delete this engagement.",dict(click=(590,729,140,36),shot2='fs_delete')),
   ('fs_delete',((260,330,800),(280,380,740)),[(381,668,560,43)],'Type the name to confirm',"Type the engagement's name to confirm. That's your safety check."),
   ('fs_delete',((280,380,740),(280,380,740)),[(381,729.5,159,35)],'It cannot be undone',"Delete permanently removes everything: the Blueprint, questions, prototypes, share links, questionnaire and client files. It can't be undone."),
   ('fs_delete',((280,380,740),(280,380,740)),[(547.7,729,53,36)],'Not sure? Keep it',"Not sure? Choose Keep it.")]),
 'prep':L_('Prepare and pre-fill the questions',M3,'Prepare_and_prefill',[
   ('fs_prep_top',((0,0,1440),(100,80,1000)),[(165,156.7,760,85)],'You’re preparing this for the client',"On the engagement, the Pre-workshop questionnaire opens in a preparing view. The client doesn't see this yet."),
   ('fs_prep_top',((100,80,1000),(100,150,1000)),[(165,257.7,720,253)],'Who it goes to, your name, a short note',"Check who it goes to, add your name, and a short note for the top."),
   ('fs_prep_app',((0,0,1440),(100,90,1000)),[(165,155,770,112)],'Pre-fill what you heard on the call',"Pre-fill anything you heard on the call. The client sees it marked From our conversation, and can change it."),
   ('fs_prep_custom',((0,200,1440),(100,440,1000)),[(165,648,770,62)],'Add up to three of your own',"Add up to three questions of your own."),
   ('fs_prep_files',((0,0,1440),(100,90,1000)),[(165,150,770,170)],'Add screenshots you already have',"And add screenshots you already have, so the client doesn't send them again.")]),
 'send':L_('Preview it and email the client',M3,'Preview_and_send',[
   ('fs_send_actions',((0,150,1440),(100,330,1000)),[(275.8,559.7,169.4,39)],'Preview as the client',"Before you send, choose Preview as the client to see exactly what they'll get."),
   ('fc_top',((0,0,1440),(300,0,840)),[],'A simple page that saves as they go',"It's a simple, JSH-branded page. It works on a phone, and saves as they go."),
   ('fs_send_actions',((100,330,1000),(100,330,1000)),[(653.7,560.7,159.6,37)],'Email it to the client',"Email it to the client sends it from the Workshop Platform, with your note and a Start the questions button."),
   ('fs_sent',((0,0,1440),(120,60,1200)),[(165,315,1110,80)],'Or send the link yourself',"Or choose I'll send the link myself, and copy the link into your own message."),
   ('fs_sent',((120,60,1200),(120,60,1200)),[(165,168.7,1110,24)],'See when it’s sent and opened',"The panel shows when it was sent, and when it's opened. You get an email the moment they submit.")]),
 'back':L_('Bring the answers into the Blueprint',M3,'Bring_the_answers_in',[
   ('fs_back0',((0,0,1440),(120,60,1200)),[(165,168.7,1110,24)],'Received',"When the client submits, the panel shows it's been received."),
   ('fs_answers',((0,0,1440),(100,180,1000)),[],'Show their answers',"Show their answers lists everything they said. Anything they skipped is marked, and anything they changed from what you heard is flagged."),
   ('fs_back0',((120,60,1200),(120,60,1200)),[(165,208.7,453.7,44)],'Bring it into the Blueprint',"Choose Bring it into the Blueprint and prepare the meeting plan. It takes about a minute.",dict(click=(165,208.7,453.7,44),shot2='fs_plan')),
   ('fs_plan',((120,60,1200),(120,100,1200)),[(165,208.7,1110,344)],'Client said facts, and a meeting plan',"Their answers become Client said facts, and you get a meeting plan: what to open with, the questions for the meeting, and recommendations worth raising.")]),
 'tools':L_('Know their tools before the meeting',M3,'Know_their_tools',[
   ('fs_plan',((0,0,1440),(120,100,1200)),[(165,208.7,1110,344)],'Every tool they named is looked up',"When the answers come in, every tool the client named is looked up from public sources."),
   ('fs_tools',((200,90,1100),(300,160,860)),[],'Open Current apps',"Open Current apps to see them. Each shows what it does, and whether other software can connect to it."),
   ('fs_tools_found',DLG,[],'Show what we found',"Show what we found opens the profile: what it holds, how it connects, what its users complain about, and whether to keep and connect it, or replace it."),
   ('fs_tools_found',((300,60,900),(320,120,840)),[],'Check the match with the client',"Walk into the meeting already knowing their setup. And check the match with the client, in case it's a different product.")]),
 'open':L_('Work the Open-with checklist',M4,'Open_with_checklist',[
   ('fs_open',((0,0,1440),(100,110,1240)),[(165,229.7,1110,374)],'Open with: your opening points',"In the Client workshop tab, the meeting plan's opening points sit at the top, as a checklist called Open with."),
   ('fs_open',((100,110,1240),(120,180,1100)),[(180,355.7,1080,73)],'Tick each one as you cover it',"Tick each one as you cover it in the meeting.",dict(click=(184,360.7,13,13),shot2='fs_open_tick')),
   ('fs_open_note',((120,180,1100),(140,300,1100)),[(206,488.7,1054,118)],'Add a note saves it to the Blueprint',"Add a note saves what the client said straight into the Blueprint, and ticks the point off."),
   ('fs_open_tick',((120,180,1100),(120,180,1100)),[(180,242.7,1080,24)],'The header counts what’s left',"The header counts what's left. Anything not covered shows in the readiness panel, but it won't block marking Workshop 1 complete.")]),
 'chamber':L_('Use the JSH chamber and import call notes',M4,'JSH_chamber',[
   ('ch_tab',((0,150,1440),(100,280,1100)),[(165,354.7,1110,42)],'The JSH chamber: hidden from the client',"The JSH chamber is the second tab. The client never sees it."),
   ('ch_tab',((100,280,1100),(100,300,1000)),[(165,448.7,208.6,44)],'The technical questions JSH owns',"Ask the next questions brings the technical questions JSH owns: screens, data, and integrations."),
   ('ch_tab',((100,300,1000),(100,300,1000)),[(381.6,447.7,234.5,46),(165,503.7,680,84)],'Assume the rest and log it',"Assume the rest lets the platform answer what's left, the way most teams building this kind of app would. Each answer is logged as an assumption."),
   ('ch_import',((0,150,1440),(100,330,1240)),[(165,435.7,1110,357)],'Import notes from a call',"Have notes from a call? Paste them in and choose Import notes. Everything lands in the Blueprint as client-stated.")]),
 'bp':L_('Read a Blueprint card',M5,'Read_a_Blueprint_card',[
   ('bp_full',((0,0,1440),(120,60,1200)),[(155,150,1130,330)],'Ten cards, each with a score',"The Blueprint is ten cards. Each shows how complete that section is, and who answers it: the client, or JSH."),
   ('bp_full',((120,60,1200),(120,60,1200)),[(838,220,212,210)],'Click a card to open it',"Click a card to open it.",dict(click=(838,220,212,210),shot2='jr2')),
   ('jr2',DLG,[(389,302,77.3,22)],'Every fact shows its source',"Every fact shows where it came from: Client said, JSH decided, Industry default, or Recommended and adopted."),
   ('top2',((0,0,1440),(100,180,1240)),[(144,429.9,1152,21)],'Prototype-ready at 60%, build-ready at 90%',"The bar at the top adds it up. Prototype-ready at sixty percent, build-ready at ninety.")]),
 'recs':L_('Adopt, rework or decline a recommendation',M5,'Recommendations',[
   ('rc_open',((180,0,1080),(300,100,900)),[],'Better ways of working, from the domain expert',"Recommendations are better ways of working that the domain expert suggests. Each shows the industry practice behind it, and its impact."),
   ('rc_open',((300,100,900),(320,250,800)),[(381,459.5,76,42.5)],'Adopt',"Adopt it, and it shapes the prototype.",dict(click=(381,459.5,76,42.5))),
   ('rc_feedback',((320,250,800),(320,280,800)),[(381,456.5,678,208.5)],'Feedback: the expert reworks it',"Choose Feedback to have the expert rework it around what you say. The history is kept."),
   ('rc_open',((320,250,800),(320,250,800)),[(577.7,463.5,54,34.5)],'Decline, with a reason',"Or Decline, with a reason. A declined recommendation becomes a constraint the workshop respects."),
   ('recs_adopted',DLG,[],'Only adopted ones shape the prototype',"Only adopted recommendations shape the prototype. You can decide the rest any time.")]),
 'assume':L_('Confirm or correct an assumption',M5,'Assumptions',[
   ('as_open',((180,0,1080),(300,150,900)),[(948.7,302,107.3,22)],'Each assumption is tagged',"An assumption is something the platform answered for you. Each is tagged: Industry default, JSH to decide, or Confirm with client."),
   ('as_open',((300,150,900),(320,220,800)),[(381,397,81,35)],'Right? Confirm',"If it's right, choose Confirm.",dict(click=(381,397,81,35))),
   ('as_correct',((320,220,800),(320,250,800)),[],'Wrong? Correct it',"If it's wrong, choose Correct, type what's true, and say whether it came from the client or JSH."),
   ('as_open',((300,150,900),(300,150,900)),[],'Confirm with client must be settled',"Anything marked Confirm with client must be settled before the engagement is build-ready.")]),
 'dir':L_('Propose and approve a design direction',M6,'Design_direction',[
   ('w1_complete',((0,0,1440),(100,250,1100)),[(160,545,250,50)],'Propose a design direction',"Once Workshop 1 is complete, choose Propose a design direction. It takes about a minute.",dict(click=(166,552,234,36))),
   ('dd_top',WIDE,[(165,109.8,550,39)],'A look built around who uses the app',"The platform proposes a look built around who uses the app, and where: a name, colors, type, and tone."),
   ('dd_sample',((300,0,1140),(600,20,800)),[],'One sample screen',"It designs one sample screen, so you can judge the look before the rest are built."),
   ('dd_plan',WIDE,[(160,110,1120,330)],'Every screen, planned',"And it plans every screen, from the day-in-the-life journeys."),
   ('dd_plan',((70,40,1300),(100,200,1000)),[(165,459.7,202.5,44)],'Approve this direction',"Happy with it? Choose Approve this direction. If not, give feedback, and it tries again.",dict(click=(165,459.7,202.5,44)))]),
 'build':L_('Build it and click through',M6,'Build_and_click_through',[
   ('proto_a2',WIDE,[],'Build the prototype',"With the direction approved, choose Build the prototype. Every planned screen is built, and wired together."),
   ('proto_a2',((70,40,1300),(140,40,1180)),[(500,103,133,36)],'Enter as each kind of user',"Enter as each kind of user, to see the app the way they would.",dict(click=(500,103,133,36),shot2='proto_route2')),
   ('proto_route2',((140,40,1180),(140,80,1000)),[],'Click through like a real app',"Click through like a real app. Anything with a dashed outline on hover is live."),
   ('proto_a2',((140,40,1180),(400,300,1000)),[(950,520,330,290)],'All screens, and who each is for',"All screens lists every screen, and who it's for. The data is sample data, and logins and integrations aren't live.")]),
 'comment':L_('Comment on a spot and tweak a screen',M6,'Comment_and_tweak',[
   ('cm_saved',((0,0,1440),(150,120,1150)),[(788,205,150,44)],'Switch to Add comments',"Above the prototype, switch from Click through to Add comments."),
   ('cm_saved',((150,120,1150),(150,160,1100)),[(165,250,400,560)],'Click the exact spot',"Then click the exact spot you want to talk about, and type your comment. Mark it as from JSH, or from the client."),
   ('cm_saved',((150,160,1100),(500,160,820)),[(968,249.8,294,235)],'Pinned to the spot, listed beside it',"It's pinned to that spot, and listed beside the screen."),
   ('cm_saved',((500,160,820),(500,160,820)),[(1000,354.8,206,35)],'Tweak the screen with this',"Tweak the screen with this rebuilds just that screen, as a new version, in about thirty seconds.",dict(click=(1000,354.8,206,35))),
   ('cm_saved',((500,160,820),(500,160,820)),[(1000,397.8,220,35)],'Bigger change? Update the Blueprint',"For something bigger than a tweak, send it to Update the Blueprint. Or choose Resolve when it's handled.")]),
 'update':L_('Update the Blueprint from feedback',M6,'Update_the_Blueprint',[
   ('ub_typed',((0,0,1440),(100,60,1240)),[(165,178.3,1110,118)],'Say what’s missing, in plain words',"Seeing the prototype often shows what's missing. In Update the Blueprint, say it in plain words, and mark whether JSH or the client said it."),
   ('ub_typed',((100,60,1240),(100,60,1240)),[(165,355.3,72,44)],'Choose Send',"Choose Send.",dict(click=(165,355.3,72,44),shot2='ub_triaged')),
   ('ub_triaged',((100,60,1240),(120,330,1160)),[(160,420,1120,160)],'Blueprint change, design tweak, or out of scope',"The platform sorts it: a Blueprint change, a design tweak, or out of scope, parked for phase two."),
   ('ub_triaged',((120,330,1160),(120,330,1160)),[(322,585,210,48)],'Update the prototype',"Review and edit the read-back if you need to, then choose Update the prototype. The Blueprint and the screens change together.",dict(click=(328,589,197,40),shot2='ub2'))]),
 'versions':L_('Work with versions',M6,'Work_with_versions',[
   ('versions2',((0,0,1440),(130,60,900)),[(158,114,304,52)],'Every change makes a new version',"Every change makes a new version. The Versions strip shows them all, and which one is current."),
   ('vs_open',((0,0,1440),(100,80,1000)),[(180,340.8,211,46)],'Bring this version back',"Open any version to look at it. Bring this version back makes it current again."),
   ('vs_open',((100,80,1000),(100,120,1000)),[],'Branch, or delete with Undo',"You can also re-edit the feedback you gave on a version to branch from it, or delete a version, with Undo. Version numbers are never reused.")]),
 'share':L_('Create a share link for the client',M7,'Share_link',[
   ('share',((0,0,1440),(100,40,1100)),[(165,90.1,1110,24)],'Share with the client',"Under the prototype, Share with the client creates a private link to the current version."),
   ('share',((100,40,1100),(100,120,900)),[(160,286,300,48)],'Copy it, or open it as the client',"Copy the link to send it, or open it as the client sees it."),
   ('PHONE',None,[],'Who are you today? Then the app',"The client sees a branded page that asks, Who are you today? Then the clickable app. On a phone it fills the screen, with no sign-in."),
   ('share',((100,120,900),(100,120,900)),[],'It stays on the version you shared',"The link stays on the version you shared until you move it. And you can turn it off any time.")]),
 'check':L_('Run the build-readiness check',M7,'Build_readiness_check',[
   ('w1_complete',((0,0,1440),(100,60,1100)),[(160,325,250,44)],'Run the build-readiness check',"After Workshop 1, run the build-readiness check. It takes about a minute.",dict(click=(166,332,234,26))),
   ('readiness2',((0,0,1440),(130,40,1000)),[(160,134,300,44)],'Scored against what the build needs',"It scores every section against what the build needs, not just the prototype."),
   ('readiness2',((130,40,1000),(130,40,1000)),[(168,223.8,1107,21),(168,253.8,218,33)],'Each gap becomes a question',"Each gap becomes a question, for JSH, or for the client in Workshop 2."),
   ('br_left',DLG,[],'See what’s left and answer it',"See what's left and answer it puts everything outstanding in one place. Answer what you can, then run the check again."),
   ('readiness2',((130,40,1000),(130,40,1000)),[(160,134,300,44)],'Build-ready: 90%, nothing to confirm',"Build-ready means a score of ninety percent or more, and nothing left to confirm with the client.")]),
 'export':L_('Export the build package',M7,'Export_the_build_package',[
   ('readiness2',((0,0,1440),(130,40,1000)),[],'The last step: the build package',"When the engagement is build-ready, the last step is the build package."),
   ('bp_full',((0,0,1440),(120,60,1200)),[],'Everything the workshop captured',"It carries everything the workshop captured: the Blueprint, the design direction, the feedback log, and a gallery of every screen."),
   ('top2',((0,0,1440),(100,180,1240)),[],'A Product Engineer exports it',"Exporting is a Product Engineer's step, so you won't see the button. Your job is to get the engagement build-ready, and let them know.")]),
}
