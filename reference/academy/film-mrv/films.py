"""Every MyRealtyVault Agent-path film: overview, module intros, lessons, wrap-up. One dict per film.
beat = shot (capture name), hl (element keys from cap/<shot>.json, or [x,y,w,h] in phone px), click, shot2, cap (headline), vo.
talk beats (intros, overview, wrap-up) show the phone plus bullet points instead of the zoom window.
House rules: say "tap" (it is a phone app), plain statements, only what the film set actually shows."""
PATH='Agent path'
M=['', 'Module 1 · Your day on one screen','Module 2 · Clients','Module 3 · Buyers','Module 4 · Listings','Module 5 · Showings and calendar','Module 6 · Closings and documents','Module 7 · Marketing']
def L(m,title,file,beats,**k): return dict(module=M[m],title=title,file='Lesson_'+file,beats=beats,m=m,**k)
def T(shot,cap,vo,pts=(),**k): return dict(talk=True,shot=shot,cap=cap,vo=vo,pts=list(pts),**k)
def B(shot,cap,vo,hl=(),**k): return dict(shot=shot,cap=cap,vo=vo,hl=list(hl),**k)
CALL=[16,156,132,54]; TEXT=[156,156,132,54]; EMAIL=[295,156,132,54]
FILMS={
# ---------------- Module 1
'tour':L(1,'Find your way around','Find_your_way_around',[
  B('home','Today is your home screen',"When you open MyRealtyVault, you land on Today. It greets you and shows what's next on your calendar.",['greet','next'],cam='top'),
  B('home','Text or Go, right from the card',"From that card you can text the client, or tap Go for directions.",['text','go']),
  B('home','Eight tiles run your business',"Below it are eight tiles. Each one is a part of your business, with a count and a one-line status.",['needs','buyers','listings','clients','showings','marketing','closings','documents'],cam=((0,205,443),(0,600,443))),
  B('home','Tap a tile to open it',"Tap a tile to open it. Let's open Listings.",['listings'],click='listings',shot2='listings_panel'),
  B('listings_panel','Each tile opens its own panel',"Each tile opens a panel with the things you can do there. Tap Today, top left, to go back.",['active','new'],cam=(0,100,443)),
  B('home','The bar at the bottom is always there',"The bar at the bottom never moves: Today, Clients, the microphone for your assistant, Deals, and Office.",[[0,896,443,64]],cam='bottom'),
  B('office','Office holds everything behind the scenes',"Office holds everything behind the scenes: your calendar, the marketing studio, vaults, reports, your profile, and help.",['cal','mkt','vaults','reports','profile','help']),
]),
'needs':L(1,'Clear what needs you','Clear_what_needs_you',[
  B('home','Start your day with Needs you',"Start every day with the first tile, Needs you. The number is how many things are waiting.",['needs'],click='needs',shot2='needs_panel'),
  B('needs_panel','Most urgent first',"It opens to six choices. Needs your attention is the list to clear.",['att'],click='att',shot2='attention'),
  B('attention','Scored by urgency',"Everything here is scored by urgency. The most pressing item is number one.",['count',[30,300,385,135]]),
  B('attention','Each item suggests the next move',"Each item suggests the next move, like Confirm with seller. Open the file takes you straight to that deal.",['do1','open1']),
  B('attention','Sweep clears them one at a time',"Sweep walks you through them one at a time. Take all suggestions accepts every suggested move at once.",['sweep','all']),
  B('digest','Your daily digest',"Back in Needs you, Your daily digest shows what came in while you were away, and what today holds.",['away','today']),
]),
'assistant':L(1,'Ask your assistant','Ask_your_assistant',[
  B('needs_panel','Open Ask your assistant',"In Needs you, tap Ask your assistant.",['ask'],click='ask',shot2='ask'),
  B('ask','Ask in plain words',"Ask in plain words, or tap one of the starter questions. Let's ask, What should I do first today?",['q1'],click='q1',shot2='ask_answer'),
  B('ask_answer','The answer comes from your own book',"The answer comes from your own clients, deals, and calendar. Here it says to call Hannah Cole first, and why.",[[38,233,320,150]]),
  B('ask_answer','It only uses your workspace',"The assistant only uses what is in your workspace. If something isn't there, it says so.",[[30,585,385,40]]),
  B('home','Or just talk to it',"You can also talk to it. Tap the microphone in the middle of the bottom bar, from any screen.",['mic'],click='mic',shot2='mic'),
  B('mic','Say what you need',"It starts listening right away. Say something like, What do I need to do today, or, Create a task.",[[32,669,395,270]]),
]),
# ---------------- Module 2
'addclient':L(2,'Add a client','Add_a_client',[
  B('home','Open Clients',"From Today, tap the Clients tile.",['clients'],click='clients',shot2='clients_panel'),
  B('clients_panel','Tap Add client',"Tap Add client. A name and a phone number are enough to start.",['add'],click='add',shot2='add_blank'),
  B('add_filled','Name, email, phone',"Type the name, and add an email and phone if you have them.",['name','email','phone']),
  B('add_filled','Hot, warm, or cold',"Mark how warm they are, and whether they are buying, selling, or both.",['hot','buying']),
  B('add_filled','Where they came from',"Pick where they came from, like an open house, and leave the stage on Lead for someone new.",['src','stage']),
  B('add_filled','Add a note, then save',"Add a short note so you remember the conversation. Then tap Add to my book.",['note','save'],click='save',shot2='add_done'),
  B('add_done','They are in your book',"Elena is now at the top of your book, marked Hot, with her phone number ready to tap.",[[16,330,411,88]]),
]),
'card':L(2,'Work a client card','Work_a_client_card',[
  B('book','Open a client from your book',"In Your book, tap a client to open their card. We'll open Maya Ellis.",['maya'],click='maya',shot2='card'),
  B('card','Call, Text, Email',"At the top are Call, Text, and Email. One tap starts each one.",[CALL,TEXT,EMAIL],cam='top'),
  B('card','Everything for this client',"Below that is everything for this client: email, text, call, note, history, booking, and their vault.",[[18,250,407,175]]),
  B('card','Tap Note after every contact',"After you talk to someone, tap Note.",['b_note'],click='b_note',shot2='card_note'),
  B('card_note','Say what happened',"Pick what it was, a call, text, meeting, or note, and type what happened in your own words.",['kinds','box']),
  B('card_note','Set a follow up, then save',"Choose a follow up, like three days, and tap Save note.",['follow','save'],click='save',shot2='card_saved'),
  B('card_hist','It all lands in History',"The card now says Talked today, and the note is in History for next time.",[[30,425,385,80]]),
]),
'pipeline':L(2,'Your book, pipeline and import','Your_book_pipeline_and_import',[
  B('clients_panel','Your book is everyone you know',"In Clients, Your book is everyone you work with.",['book'],click='book',shot2='book'),
  B('book','Search and filter',"Search by name, email, or phone. Tap Hot, Warm, or Cold, or filter to buyers or sellers.",['search','hot','filters'],cam='top'),
  B('book','Speak a note without opening the card',"On every row, the microphone lets you speak a note, and the pencil edits the client.",['mic','edit']),
  B('pipeline','Pipeline shows every active deal',"Pipeline lists every active deal on both sides, with its stage and the next step.",[[16,110,411,170]],cam='top'),
  B('reach','Reach today',"Reach today tells you who is due for a call. When no one is due, it says so.",[[16,130,411,60]],cam='top'),
  B('import','Bring your whole book in',"Moving from another system? Import takes a spreadsheet file. The columns map themselves, and nothing uploads until you say go.",[[16,110,411,160]],cam='top'),
]),
# ---------------- Module 3
'buyer':L(3,'Start a buyer profile','Start_a_buyer_profile',[
  B('home','Open Buyers',"From Today, tap the Buyers tile.",['buyers'],click='buyers',shot2='buyers_panel'),
  B('buyers_panel','Tap Start a buyer',"Tap Start a buyer. It takes about a minute.",['start'],click='start',shot2='buyer_blank'),
  B('buyer_top','Pick the client',"Choose who it is for. Pick someone already in your book and their details fill in, or enter someone new.",['who']),
  B('buyer_top','Budget, beds, baths',"Enter their budget, and the fewest beds and baths they will accept.",['bmin','bmax','beds','baths']),
  B('buyer_bottom','Where, must-haves, dealbreakers',"Add the areas they want, their must-haves, and anything to avoid. Separate each with a comma.",['areas','must','deal']),
  B('buyer_bottom','Create buyer profile',"Tap Create buyer profile.",['create'],click='create',shot2='buyer_created'),
  B('bp','The profile tracks the whole journey',"The profile opens. The steps across the top follow your buyer from getting started all the way to closed.",[[14,130,415,115]],cam='top'),
]),
'preapp':L(3,'Log a pre-approval and track a home','Log_a_pre-approval_and_track_a_home',[
  B('buyers_list','Open the buyer',"In Active buyers, tap the buyer to open their profile.",['elena'],click='elena',shot2='bp'),
  B('bp','Tap Log pre-approval',"When the lender letter comes in, tap Log pre-approval.",['pre'],click='pre',shot2='pre_filled'),
  B('pre_filled','Amount, lender, loan type, rate',"Enter the approved amount, the lender, the loan type, and the rate.",['amt','lender','type','rate']),
  B('pre_filled','Save the pre-approval',"Tap Save the pre-approval.",['save'],click='save',shot2='pre_saved'),
  B('pre_saved','Approved to shows on the profile',"The profile now shows what they are approved to, and with which lender.",[[300,296,115,50],[16,356,200,24]]),
  B('track_filled','Track a home they like',"Found a home they like? Tap Track a home, enter the address and list price, and tap Track it.",['addr','price','go'],click='go',shot2='track_saved'),
  B('track_saved','It joins their tracked homes',"The home joins their tracked homes. Set it to Watching, Tour set, Toured, or Passed as things move.",[[18,770,407,100]]),
]),
'logtour':L(3,'Log a tour','Log_a_tour',[
  B('track_saved','After every tour, log it',"After you show a home, log it while it is fresh. On the buyer profile, tap Log tour.",[[280,384,70,32]],click=[280,384,70,32],shot2='tour_filled',cam=(0,250,443)),
  B('tour_filled','When, and which home',"Set when it happened, and which home.",['when',[31,588,381,48]]),
  B('tour_filled','How it went',"Type how it went, in your buyer's words. Loved the yard. Kitchen needs updating.",['how']),
  B('tour_filled','Log the tour',"Tap Log the tour.",['go'],click='go',shot2='tour_saved'),
  B('tour_saved','Tours done goes up',"Tours done goes up by one, so you always know how much ground you have covered together.",[[112,296,96,50]]),
  B('bp','Offer comes next',"When they are ready, Log offer sits right beside it.",['offer']),
]),
# ---------------- Module 4
'newlisting':L(4,'Create a listing','Create_a_listing',[
  B('home','Open Listings',"From Today, tap the Listings tile.",['listings'],click='listings',shot2='listings_panel'),
  B('listings_panel','Tap New listing',"Tap New listing. It takes about two minutes, and the page goes live when you save.",['new'],click='new',shot2='nl_blank'),
  B('nl_top','Start with the seller',"Start with the seller. Choose New client and type their details, or pick an existing client.",['new','existing','seller','email','phone']),
  B('nl_top','Then the property',"Then the property: street address, city, and zip.",['addr','city','zip']),
  B('nl_bottom','Beds, baths, size, year',"Add beds, baths, square feet, and the year it was built.",['beds','sqft','year'],cam=(0,180,443)),
  B('nl_bottom','List price and status',"Enter the list price. Leave the status on For sale, or choose Coming soon.",['price','status']),
  B('nl_bottom','Create listing',"Tap Create listing.",['create'],click='create',shot2='listings4'),
  B('listings4','It is in your active listings',"Your new listing now shows in your active listings, with its own page ready to share.",['card']),
]),
'page':L(4,'Photos, story and the listing page','Photos_story_and_the_listing_page',[
  B('nl_actions','Every listing has its own page',"Every listing gets its own web page, with a link you can copy. Tap Edit page to build it out.",['link','copy','edit'],click='edit',shot2='ep_photos'),
  B('ep_photos','Add photos',"Tap Add photos and choose them from your phone. The first photo becomes the hero, the one the page leads with.",['add',[40,555,363,300]]),
  B('ep_story','Give the writer three phrases',"For the story, give the writer up to three phrases about what makes this home special.",['p1',[52,460,339,96]]),
  B('ep_story','Headline and narrative',"It proposes a headline and narrative. You edit them. Nothing goes on the page until you save.",['head','narr']),
  B('ep_save','Highlights, then Save to the page',"Add up to six highlights, one per line, and tap Save to the page.",['hl','save'],click='save',shot2='ep_saved'),
  B('lp_top','This is what buyers see',"This is what buyers see: your photos, the price, the headline, and a Request a showing button.",[],cam=(0,385,443)),
  B('lp_2','Your story, and a way to reach you',"Your highlights and story follow, and buyers can share the page or ask to see the home in person.",[],cam=(0,40,443)),
]),
'runlisting':L(4,'Log a showing and change the price','Log_a_showing_and_change_the_price',[
  B('hb_detail','Open the listing',"Open a listing to see its price, days listed, showings, and offers at a glance.",['price',[20,640,403,90]]),
  B('hb_actions','Everything for this listing',"Scroll down to Everything for this listing. The stages show where it stands, and what comes next.",['owner',[30,330,385,90]]),
  B('hb_actions','Tap Log showing',"When another agent shows the home, tap Log showing.",['showing'],click='showing',shot2='hb_showing'),
  B('hb_showing','Who showed it, and what they said',"Enter when, the showing agent, and the feedback in their words.",['when','agent','fb']),
  B('hb_showing','Rate the interest, then log it',"Choose how interested the buyers were, and tap Log the showing.",['read','go'],click='go'),
  B('hb_price','Change the price',"To change the price, tap Price, enter the new number and a note for the record, and tap Change the price.",['price','new','note','go']),
  B('hb_actions','Advice built from the numbers',"Below, MyRealtyVault reads the views, saves, and showings, and gives you talking points for the seller call.",[[36,600,370,110]]),
]),
# ---------------- Module 5
'request':L(5,'Confirm a showing request','Confirm_a_showing_request',[
  B('lp_top','A buyer asks to see a home',"When a buyer taps Request a showing on a listing page, the request comes to you.",[[16,896,200,52]],cam='bottom'),
  B('needs_panel','It shows up in Needs you',"It shows up under Needs you, in Showing requests.",['req'],click='req',shot2='req'),
  B('req','The home and the time they asked for',"You see the home and the time they asked for.",['addr','card']),
  B('req','Tap Confirm',"If the time works, tap Confirm. You can also decline, or ask the seller's agent first.",['confirm','decline','ask'],click='confirm',shot2='req_done'),
  B('req_done','Confirmed, and on your calendar',"It is confirmed and on your calendar, and the buyer gets the details by email.",['msg']),
  B('cal_list','See it with everything else',"You'll find it on the calendar with the rest of your showings.",[[40,352,380,46]]),
]),
'calendar':L(5,'Use the calendar and add a task','Use_the_calendar_and_add_a_task',[
  B('show_panel','Open Showings',"The Showings tile opens your calendar panel: today, showings, deadlines, tasks, and the full calendar.",['showings','deadlines'],cam=(0,130,443)),
  B('cal_week','Month, week, day, or list',"Full calendar shows everything in one place. Switch between month, week, day, and list.",[[28,118,285,48]],cam='top'),
  B('cal_list','Filter to what you need',"Filter to deadlines, showings, appointments, or tasks.",[[28,232,385,95]]),
  B('cal_list','Tap New',"To add something, tap New.",['new'],click='new',shot2='cal_new'),
  B('cal_new','Task, appointment, or event',"Choose a task, an appointment, or an event. Deadlines come from the contract, so they are added on the listing.",['task','appt','event']),
  B('cal_task','Say what needs doing',"For a task, say what needs doing, attach a client if you like, set the due date, and tap Add task item.",['what','client','due','add']),
]),
# ---------------- Module 6
'closing':L(6,'Follow a closing','Follow_a_closing',[
  B('home','Open Closings',"The Closings tile shows how many deals are under contract. Tap it.",['closings'],click='closings',shot2='closings'),
  B('closings','Every deal under contract',"Each deal under contract is here, with its steps to closing and the closing date.",[[16,269,427,122]]),
  B('closing_detail','Open the file',"Tap a deal to open its file. The steps across the top show where it stands: under contract, inspection, appraisal, clear to close, closed.",[[14,130,420,115]],cam='top'),
  B('closing_detail','Keep the next step current',"Next always names the very next thing to do. Tap the pencil to change it.",['next']),
  B('deadlines','Deadlines count down for you',"In the calendar, Deadlines counts down every contract date: inspection, appraisal, loan approval, and closing.",['r1','r2','r3','r4']),
  B('attention','The urgent ones come to you',"And anything due soon shows up in Needs you, so a date never slips.",['count',[30,300,385,135]]),
]),
'vault':L(6,"Add a document to a client's vault",'Add_a_document_to_a_clients_vault',[
  B('home','Open Documents',"From Today, tap the Documents tile.",['documents'],click='documents',shot2='docs_panel'),
  B('docs_panel','Tap Add to the vault',"Tap Add to the vault.",['add'],click='add',shot2='vault_filled'),
  B('vault_filled','Choose the client',"Choose the client, and which deal the file belongs under.",['client','under']),
  B('vault_filled','Kind and status',"Pick the kind of document, like a disclosure, and its status, like awaiting signature.",['kind','status','title']),
  B('vault_filled','Share it, or keep it private',"Decide whether to share it with the client, or keep it private to you.",['share','private']),
  B('vault_filled','Choose the file and upload',"Choose the file, or scan paper with your camera, and tap Upload.",[[37,735,335,40],'scan','upload'],click='upload',shot2='vault_done'),
  B('vaults','It is in their vault',"The document is in the client's vault, where you can view it, download it, or share it.",[[16,124,411,292]]),
]),
# ---------------- Module 7
'form':L(7,'Create an open house sign-in form','Create_an_open_house_sign-in_form',[
  B('home','Open Marketing',"From Today, tap the Marketing tile.",['marketing'],click='marketing',shot2='mkt_panel'),
  B('mkt_panel','Tap Forms',"Tap Forms.",['forms'],click='forms',shot2='forms'),
  B('forms','Start with the moment',"Start with the moment. Open house sign-in puts every visitor into your book, tagged with the address.",[[17,277,198,130]],click=[17,277,198,130],shot2='form_pick'),
  B('form_pick','Pick the listing',"Pick the listing the open house is for.",['pick']),
  B('form_draft','Your form starts as a draft',"The form is created as a draft, under Your forms. Tap Publish when you are ready.",['state','publish'],click='publish',shot2='form_live'),
  B('form_live','Live, with a link to share',"Now it is live. Open it on a tablet by the door, email it, or copy the link.",[[18,712,405,52]]),
  B('form_draft','Sign-in stand mode',"Sign-in stand mode keeps it ready for the next visitor, and you can add your own thank-you note.",['stand','thanks']),
]),
'campaign':L(7,'Create a just listed email','Create_a_just_listed_email',[
  B('mkt_panel','Tap Emails',"In Marketing, tap Emails.",['emails'],click='emails',shot2='emails'),
  B('emails','Quick email from a template',"Tap Quick email from a template.",['quick'],click='quick',shot2='camp_moment'),
  B('camp_moment','Pick the moment',"Pick the moment: just listed, open house, price reduced, under contract, or just sold.",['jl','oh','pr']),
  B('camp_ready','Pick the design and the listing',"Choose the design, then choose the listing. Its photo, price, and details are pulled in for you.",['design',[37,535,369,62]]),
  B('camp_ready','Create the campaign',"Tap Create just listed campaign.",['create'],click='create',shot2='camp_made'),
  B('camp_made','Review it before anything sends',"The email is built in your brand, and waits for your review. Nothing sends until you tap Send.",[],cam=(0,430,443)),
  B('camp_made','Edit or Send',"Tap Edit to change the words, or Send to choose who gets it.",['edit','send']),
]),
'results':L(7,'Workflows and results','Workflows_and_results',[
  B('mkt_panel','Workflows send themselves',"Workflows are emails that send themselves, like a welcome series for every new client.",['flows'],click='flows',shot2='flows'),
  B('flows','Tap New workflow',"Tap New workflow, give it a name, and choose what starts it: someone joins a group, changes stage, or lands in your book.",['new','hint']),
  B('mkt_panel','Then check Results',"Then check Results to see whether your marketing is working.",['results'],click='results',shot2='results'),
  B('results','The last thirty days',"It shows the last thirty days: who joined your list, emails delivered, clicks, and forms filled in.",[[40,255,365,235]]),
  B('results','What to do next',"And it tells you what to do next, in plain words.",[[40,715,365,130]]),
]),
}
# ---------------- Module intros (required), overview (Start here), wrap-up
def I(m,title,beats): return dict(kind='intro',module=M[m],title=title,file=f'Module{m}_Intro',beats=beats,m=m,outro=('Up next',"Let's go step by step",'Each lesson shows one job, tap by tap.'))
FILMS.update({
'intro1':I(1,'Your day on one screen',[
  T('home','One screen runs your day',"Welcome to MyRealtyVault. This first module is about the screen you will see every morning.",['Today: what is next, and what needs you','Eight tiles, one for each part of your business','A bar at the bottom that never moves']),
  T('attention','Nothing slips',"You will learn how to clear the list of things that need you, most urgent first, so nothing slips.",['Scored by urgency','A suggested next move on every item']),
  T('ask_answer','An assistant that knows your book',"And you will meet your assistant, which answers from your own clients, deals, and calendar.",['Type a question, or just talk','Answers come only from your workspace']),
]),
'intro2':I(2,'Clients',[
  T('book','Your book is your business',"This module is about your book: every person you work with, in one place.",['Add a client in one pass','Hot, warm, or cold at a glance']),
  T('card_note','Every conversation, remembered',"You will learn to work a client card: call, text, email, and log a note after every contact.",['One tap to reach them','A follow up set before you move on']),
  T('pipeline','See every active deal',"And you will see your pipeline, find out who to reach today, and bring your whole book in from another system.",['Pipeline: both sides, by stage','Import from a spreadsheet']),
]),
'intro3':I(3,'Buyers',[
  T('bp','One profile for every buyer',"This module follows a buyer from the first conversation to an offer.",['Budget, areas, must-haves, dealbreakers','Steps from getting started to closed']),
  T('pre_saved','Know what they can buy',"You will log a pre-approval, so you always know what they are approved to, and with which lender.",['Approved amount, lender, loan type, rate']),
  T('tour_saved','Track homes and tours',"And you will track the homes they like, and log every tour while it is fresh.",['Tracked homes','Tours done, in their own words']),
]),
'intro4':I(4,'Listings',[
  T('listings4','From new listing to live page',"This module takes a listing from a blank form to a live page buyers can see.",['Two minutes to create','Live in your active listings on save']),
  T('lp_top','A page for every listing',"You will add photos and a story, and see the page your buyers see, with a Request a showing button.",['Photos, headline, highlights','A link you can copy and share']),
  T('hb_actions','Run the listing day to day',"And you will run the listing day to day: log showings and feedback, and change the price with a note for the record.",['Showings and feedback','Advice built from the numbers']),
]),
'intro5':I(5,'Showings and calendar',[
  T('req','Showings, confirmed in a tap',"This module is about your time. When a buyer asks to see a home, the request comes straight to you.",['Confirm, decline, or ask the seller’s agent','Confirmed showings land on your calendar']),
  T('cal_list','One calendar for everything',"You will use one calendar for showings, deadlines, appointments, and tasks.",['Month, week, day, or list','Filter to what you need','Add a task in seconds']),
]),
'intro6':I(6,'Closings and documents',[
  T('closing_detail','From contract to closed',"This module covers the stretch from contract to closing, where dates matter most.",['Every deal under contract in one place','Steps: inspection, appraisal, clear to close']),
  T('deadlines','Deadlines count down for you',"You will see every contract deadline counting down, so nothing is missed.",['Inspection, appraisal, loan approval, closing']),
  T('vaults','Every document in the client’s vault',"And you will add documents to a client's vault, shared with them or kept private to you.",['Upload a file or scan with your camera','Kind and status on every document']),
]),
'intro7':I(7,'Marketing',[
  T('mkt_panel','Marketing, built in',"This module is marketing. It lives in the same app as your clients and listings, so nothing is typed twice.",['Emails, workflows, forms, results']),
  T('form_live','Capture every lead',"You can create an open house sign-in form that puts every visitor into your book.",['Start with the moment','Live with a link in a minute']),
  T('camp_made','Email in your brand',"You can build a just listed email from a listing, and review it before anything sends.",['Photo, price, and details pulled in','Nothing sends until you tap Send']),
  T('results','Know what is working',"And you can set up emails that send themselves, and check your results.",['Workflows','The last thirty days, in plain words']),
]),
'overview':dict(kind='overview',module='Start here',title='MyRealtyVault for agents',sub='Every home. Every deal. One vault.',file='Agent_Overview',m=0,
  outro=('MyRealtyVault','Every home. Every deal. One vault.','Start with Module 1: your day on one screen.'),beats=[
  T('home','Your whole business, on your phone',"MyRealtyVault runs your whole real estate business from your phone. This short video shows you what is inside.",['Built for agents who work from the car','One screen. Eight tiles.'],kicker='MyRealtyVault · Agent path'),
  T('attention','It tells you what needs you',"Every morning it tells you what needs you, most urgent first, with a suggested next move on each item.",['Showing requests','Deadlines and overdue follow ups'],kicker='Your day'),
  T('card','Every client, one card',"Every client has one card: call, text, email, notes, history, and their documents.",['Your book, hot to cold','Every conversation remembered'],kicker='Clients'),
  T('bp','Buyers, from first call to closed',"Buyers get a profile that follows them from the first conversation to closing: budget, pre-approval, the homes they like, and every tour.",['Pre-approvals','Tracked homes and tours'],kicker='Buyers'),
  T('lp_top','Listings with their own page',"Each listing gets its own page, with your photos and story, and a button for buyers to request a showing.",['Live when you save','Showings and feedback in one place'],kicker='Listings'),
  T('cal_list','One calendar. No missed dates.',"Showings, contract deadlines, appointments, and tasks share one calendar, and the urgent ones come to you.",['Confirm a showing in a tap','Deadlines count down'],kicker='Showings and closings'),
  T('vaults','A vault for every client',"Documents live in each client's vault, shared with them or private to you.",['Upload or scan','Shared, signed, on file'],kicker='Documents'),
  T('camp_made','Marketing, already connected',"And marketing is built in: forms that capture leads, and emails made from your listings, in your brand.",['Open house sign-in forms','Just listed emails','Results in plain words'],kicker='Marketing'),
  T('ask_answer','And an assistant that knows your book',"When you are not sure what to do next, ask your assistant. It answers from your own business.",['Type it, or say it'],kicker='Your assistant'),
]),
'wrap':dict(kind='wrap',module='Agent path complete',title='You are ready',file='Agent_Path_WrapUp',m=8,
  outro=('Congratulations!','You have finished the Agent path','Your business is in one vault. Go run your day.'),beats=[
  T('home','Congratulations!',"Congratulations! You have finished the MyRealtyVault Agent path.",['Your day, on one screen','Clients, buyers, and listings','Showings, closings, and documents','Marketing that runs itself'],kicker='Agent path complete',confetti=True),
  T('attention','Tomorrow morning, start here',"Tomorrow morning, open Today, tap Needs you, and clear your list. Everything else follows from there.",['Open Today','Tap Needs you','Clear your list'],kicker='Your first day',confetti=True),
]),
})
