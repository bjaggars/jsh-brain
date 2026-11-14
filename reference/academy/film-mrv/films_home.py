"""MyRealtyVault campus · Homeowner path. Same format as films.py (see there). Captures in caph/.
Filmed as the film-set homeowner Jordan Avery on TEST, with no agent attached (the agentless homeowner)."""
PATH='Homeowner path'; CAP='caph'; PREFIX='Home_'
M=['','Module 1 · Your vault','Module 2 · Buying a home','Module 3 · Your documents','Module 4 · Selling and owning','Module 5 · Help, and your agent']
def L(m,title,file,beats,**k): return dict(module=M[m],title=title,file='Lesson_'+file,beats=beats,m=m,outro=('Your turn','Now try it in your vault','Then take the quick check to complete the lesson.'),**k)
def T(shot,cap,vo,pts=(),**k): return dict(talk=True,shot=shot,cap=cap,vo=vo,pts=list(pts),**k)
def B(shot,cap,vo,hl=(),**k): return dict(shot=shot,cap=cap,vo=vo,hl=list(hl),**k)
FILMS={
'h_tour':L(1,'Find your way around your vault','Find_your_way_around_your_vault',[
  B('home','This is your vault',"This is your vault. It keeps your homes, your search, and your documents in one place, and it is yours for life.",['title'],cam='top'),
  B('home','Pick your focus',"Tell it what you are doing right now: buying, selling, or looking after the home you own. The page changes to match.",['focus','selling','myhome']),
  B('home','Your next step',"At the top is your next step, in plain words. Tap Do it, or Later if now is not the time.",['hero','doit','later']),
  B('home','Your checklist keeps count',"Your checklist shows how far along you are. Every step can wait, and you can do them in any order.",['check','open']),
  B('home2','Every tool is one tap away',"Scroll down for your tools: home search, documents, calculators, and more.",['search','docs','afford','mort'],cam=((0,0,443),(0,300,443))),
  B('home3','Help when you want it',"Further down: Ask MRV, your checklist, your calendar, and a place to add your agent.",['askmrv','check','cal','agent'],cam=((0,250,443),(0,500,443))),
  B('home','Ask MRV follows you everywhere',"And the Ask MRV button stays in the corner of every screen.",['ask'],cam='bottom'),
]),
'h_check':L(1,'Use your checklist','Use_your_checklist',[
  B('home','Open your checklist',"From your vault, tap Open my checklist.",['open'],click='open',shot2='check'),
  B('check','Buying, selling, or owning',"There is a checklist for buying, one for selling, and one for owning. Each is split into stages.",['tabs','own','stage']),
  B('check','Each step says why it matters',"Each step says what to do and why. Open takes you straight to the right tool.",['s1','open']),
  B('check','Done, Later, or Skip',"When you finish a step, tap Done. Tap Later to come back to it, or Skip if it doesn't apply to you.",['done','later','skip']),
  B('check','Mark a step done',"Let's mark Check your credit as done.",['done2'],click='done2',shot2='check_done'),
  B('check_done','The count goes up',"The step is crossed off and your count goes up. Tap Undo if you change your mind.",['count',[30,636,385,170]]),
  B('check2','Six stages, start to keys',"Keep going through the stages: search, choose a home, make an offer, under contract, and closing.",[[16,630,411,300]]),
]),
'h_afford':L(2,'Work out what you can afford','Work_out_what_you_can_afford',[
  B('home','Start with your next step',"Buying starts with a number. On your next step, tap Do it.",['doit'],click='doit',shot2='afford'),
  B('afford','Income, debts, and savings',"Enter your household income for the year, your monthly debt payments, and the cash you have for a down payment.",['income','debt','cash']),
  B('afford','A price you will be comfortable with',"It gives you a price and a monthly payment that keep your housing costs comfortable, not just the most a lender would approve.",[[33,650,377,125]]),
  B('home2','Then check the true monthly cost',"Next, open the Mortgage calculator.",['mort'],click='mort',shot2='mort'),
  B('mort','Price, down payment, rate',"Enter a home price. Adjust the down payment, the rate, and the loan length if you need to.",['price',[33,415,377,210]]),
  B('mort2','What you would pay each month',"It adds property tax and insurance, and shows what you would really pay each month.",[],cam='bottom'),
]),
'h_search':L(2,'Search for homes and save the ones you like','Search_and_save_homes',[
  B('home2','Open Home search',"From your vault, tap Home search.",['search'],click='search',shot2='search'),
  B('search','Say what you are looking for',"Enter your price range, beds and baths, where you want to live, and your must-haves.",['low','high','beds','baths','where','must'],cam=((0,330,443),(0,540,443))),
  B('search2','Pick a site and start',"Pick Zillow, Realtor dot com, or Redfin, and tap Start my search. The site opens with your filters already set.",['zillow','realtor','redfin','start']),
  B('search3','Save a home with its link',"When you find a home you like, copy its link, come back, and paste it here.",['link','find']),
  B('saved','Your saved homes',"Every home you save lands here, with its price and details.",['card1','card2'],cam=((0,60,443),(0,480,443))),
  B('rate','Rate it and add a note',"Rate each one: love it, like, maybe, or not for me. Add a note about what you liked and what bothered you.",['note']),
  B('rate_done','Your notes stay with the home',"Your rating and your note stay with the home. If you work with an agent, they will see exactly what you love, and why.",[[16,366,411,395]]),
]),
'h_hood':L(2,'Check a neighborhood','Check_a_neighborhood',[
  B('hood','Check any address',"Before you fall for a house, check the address. Type it in and tap Check it.",['addr','go'],click='go',shot2='hood2'),
  B('hood2','Flood risk and insurance',"You get the flood zone, and what that means for insurance.",[],cam=(0,530,443)),
  B('hood3','Public schools nearby',"You see the public schools nearby, and how far away each one is.",[[16,305,411,325]]),
  B('hood3','How buying works in your state',"And you get plain facts about buying in your state, and questions to ask before you make an offer.",[],cam='bottom'),
  B('hood2','Save it with your take',"Rate the home or add a note, and it is saved with the rest of your homes.",[[16,350,411,180]],cam=(0,300,443)),
]),
'h_docs':L(3,'Keep your documents in your vault','Keep_your_documents_in_your_vault',[
  B('home2','Open Documents',"From your vault, tap Documents.",['docs'],click='docs',shot2='docs'),
  B('docs','Folders keep it tidy',"Your documents are sorted into folders, like income and bank statements. You can add your own folder too.",['all','income','bank','newf']),
  B('docs','Tap Add a document',"To add one, tap Add a document.",['add'],click='add',shot2='doc_add'),
  B('doc_add','Take a photo or choose a file',"Take a photo of the paper, or choose a file from your phone.",['photo','choose']),
  B('doc_add','Name it and pick a folder',"Say what it is, and pick the folder it belongs in.",['what','folder']),
  B('doc_add','Save to my vault',"Tap Save to my vault. It is private to you until you choose to share it.",['save'],click='save',shot2='doc_saved'),
  B('doc_saved','It is in your vault',"The document is in its folder, marked Private. From here you can move it, share it, or delete it.",[[228,342,199,134],[16,850,411,100]],cam=((0,330,443),(0,677,443))),
]),
'h_lender':L(3,'Send documents to anyone who needs them','Send_documents_to_anyone_who_needs_them',[
  B('sd_docs','Find the document and tap Share',"Your lender, your title company, your insurance agent. Sooner or later, someone needs one of your documents. In Documents, find it and tap Share.",['row','share'],click='share',shot2='sd_menu'),
  B('sd_menu','Choose who it is for',"Choose who it is for: your agent, your lender or bank, the title company, your insurance agent, or someone else.",['agent','lender','title','ins','other']),
  B('sd_menu','Tap the title company',"This policy is for the closing, so tap With the title company.",['title'],click='title',shot2='sd_sheet'),
  B('sd_sheet','Say who gets it',"Enter their name and their email.",['name','email']),
  B('sd_sheet','Choose how long the link lasts',"Choose how long the link lasts. You can stop it sooner, at any time.",['days','until']),
  B('sd_sheet','Send secure link',"Add a note if you like, then tap Send secure link.",['note','send'],click='send',shot2='sd_after'),
  B('sd_after','Your document never leaves your vault',"Your document is not emailed as an attachment. It stays in your vault, and they get a secure link to it.",['row']),
  B('sd_menu2','See who has it, and stop it',"Tap Share again to see who has a link and whether they have opened it. Tap Stop, and the link stops working right away.",['has','who','state','stop']),
]),
'h_sell':L(4,'Thinking of selling','Thinking_of_selling',[
  B('home','Switch your focus to Selling',"If you are thinking of selling, tap Selling at the top of your vault.",['selling'],click='selling',shot2='sell'),
  B('sell','A selling plan, step by step',"Your vault switches to selling, with its own next step and its own checklist.",['hero','next','check']),
  B('sell2','Know your number before you list',"The selling tools start with what your home is worth, and a free price opinion from a local agent.",['worth','opinion'],cam='top'),
  B('sell2','What will I walk away with?',"Tap What will I walk away with.",['walk'],click='walk',shot2='walk'),
  B('walk','Price, commission, payoff',"Enter the sale price, the commission, and what you still owe on your mortgage.",['price','comm','payoff']),
  B('walk','What you keep',"It takes off commission, title costs, and your payoff, and shows what you walk away with.",[[33,570,377,150]]),
  B('sell2','Offers, repairs, disclosures',"You can also compare offers side by side, get your home ready, and see what your state requires you to disclose.",['offers','ready','disc']),
]),
'h_own':L(4,'Your home and its records','Your_home_and_its_records',[
  B('home','Switch your focus to My home',"Already own your home? Tap My home at the top of your vault.",['myhome'],click='myhome',shot2='own'),
  B('own','Start by adding your home',"Your first step is to add your home. Tap Do it.",['next','doit'],click='doit',shot2='myhome1'),
  B('myhome1','Address, date, and price',"Enter the address, when you bought it, and what you paid. Then tap Save.",['addr','city','date','paid','save'],cam=((0,330,443),(0,540,443))),
  B('myhome2','Your home is on file',"Your home is on file. Keep its closing papers, insurance, warranties, and tax bills together in Documents.",[[16,328,411,70]]),
  B('own2','Taxes, insurance, maintenance',"Your home's tools cover property taxes and homestead, insurance and warranties, and home maintenance.",['tax','ins','maint']),
  B('tax','Property taxes in plain words',"Property taxes explains exemptions you may be missing, how much your bill can rise, and when it is due.",[],cam=(0,330,443)),
  B('maint','A simple care schedule',"Home maintenance gives you a simple schedule: every few months, every season, and every year.",[],cam=(0,330,443)),
]),
'h_ask':L(5,'Ask MRV','Ask_MRV',[
  B('home','Tap Ask MRV',"Ask MRV is your virtual agent. Tap the button in the corner of any screen.",['ask'],click='ask',shot2='ask'),
  B('ask','Ask anything',"Ask anything about buying, selling, or owning. Type your own question, or tap one of the starters.",['q1','q2'],cam='top'),
  B('ask','It knows your search and your homes',"Let's ask which saved home it would go with, and why.",['q2'],click='q2',shot2='ask2'),
  B('ask2','An answer about your homes',"The answer is about your homes. It used the rating and the note you saved, and it tells you what it would do, and why.",[],cam=(0,130,443)),
  B('ask2','And what to do next',"Then it suggests your next steps.",[],cam=(0,330,443)),
  B('ask','Stuck? Tell the team',"The buttons at the bottom show you how to do something, report a problem, or reach the MyRealtyVault team.",['how','team',[110,783,300,36]]),
]),
'h_cal':L(5,'Keep your dates on My calendar','Keep_your_dates_on_My_calendar',[
  B('home3','Open My calendar',"From your vault, tap My calendar.",['cal'],click='cal',shot2='cal'),
  B('cal','Tap Add to my calendar',"To add your own plans, tap Add to my calendar.",['add'],click='add',shot2='cal1'),
  B('cal1','What, when, and where',"Choose what it is, like a home tour. Add a title, the day, the time, and the address.",['kind','what','date','time','addr'],cam=((0,330,443),(0,500,443))),
  B('cal1','Save',"Tap Save.",['save'],click='save',shot2='cal2'),
  B('cal2','It is on your calendar',"It is on your calendar. When your agent books a showing, or a deadline is set, it lands here too.",[[16,430,411,90]]),
  B('cal','On your phone too',"Tap Add to my phone's calendar to see everything alongside the rest of your life.",['phone']),
]),
'h_agent':L(5,'Add your agent','Add_your_agent',[
  B('home3','Open Add your agent',"Working with an agent? From your vault, tap Add your agent.",['agent'],click='agent',shot2='agent'),
  B('agent','Their name, email, and phone',"Enter their name, email, and phone.",['name','email','phone']),
  B('agent','You choose what they see',"You choose what they see: your saved homes and notes, your search, and the documents you mark as shared.",['c1','c2','c3']),
  B('agent','Tap Add my agent',"Tap Add my agent. If they are on MyRealtyVault, they get your request right away. If not, they are invited, free.",['note','add']),
  B('rate_done','They see what you love, and why',"From then on, your agent sees the homes you rated and the notes you wrote, so they know what you are looking for.",[[16,366,411,395]]),
]),
}
def I(m,title,beats): return dict(kind='intro',module=M[m],title=title,file=f'Module{m}_Intro',beats=beats,m=m,outro=('Up next',"Let's go step by step",'Each lesson shows one job, tap by tap.'))
FILMS.update({
'h_intro1':I(1,'Your vault',[
  T('home','One place for your home life',"Welcome to MyRealtyVault. Your vault keeps every home, every search, and every document in one place, for life.",['Buying, selling, or owning','Free, with or without an agent']),
  T('check','A checklist that never rushes you',"In this module you will find your way around, and learn to use the checklist that walks you through each step.",['Do steps in any order','Done, Later, or Skip']),
]),
'h_intro2':I(2,'Buying a home',[
  T('afford','Know your number first',"This module is about buying. You start by working out what you can comfortably afford.",['A comfortable price, not the lender’s maximum','The true monthly cost']),
  T('rate_done','Search, save, decide',"Then you search for homes, save the ones you like, and rate them with your own notes.",['Search on the sites you already use','Love it, like, maybe, not for me']),
  T('hood3','Check before you fall for it',"And you check any address for flood risk, schools, and what to ask.",['Flood zone and insurance','Public schools nearby']),
]),
'h_intro3':I(3,'Your documents',[
  T('doc_saved','Private until you share',"This module is about your documents. Pay stubs, statements, contracts: they stay private until you choose to share.",['Snap a photo or choose a file','Folders keep it tidy']),
  T('sd_menu','Send them to anyone, securely',"You will send anyone who needs them, your lender, your title company, or your insurance agent, exactly the documents they ask for, in one secure link that expires.",['Lender, title, insurance, your agent','See when it is opened','Stop a link any time']),
]),
'h_intro4':I(4,'Selling and owning',[
  T('walk','Selling: know what you keep',"This module covers selling, and looking after the home you own. If you sell, you will see what you walk away with.",['Price, commission, payoff','Compare offers side by side']),
  T('myhome2','Owning: your home’s records',"If you own, you will add your home and keep its records together.",['Closing papers, insurance, warranties','Property taxes and homestead','A simple maintenance schedule']),
]),
'h_intro5':I(5,'Help, and your agent',[
  T('ask2','A virtual agent in your pocket',"The last module is about help. Ask MRV knows your search and your homes, and tells you what it would do.",['Ask anything, any time']),
  T('agent','Bring your agent in when you are ready',"And when you work with an agent, you choose exactly what they see.",['Your saved homes and notes','Your search','Only the documents you mark shared']),
  T('cal2','Every date in one place',"You will also keep your tours and deadlines on one calendar.",['Your plans, and your agent’s showings']),
]),
'h_overview':dict(kind='overview',module='Start here',title='MyRealtyVault for homeowners',sub='Your homes, your search, your documents. One vault, for life.',file='Overview',m=0,
  outro=('MyRealtyVault','Every home. Every deal. One vault.','Start with Module 1: your vault.'),beats=[
  T('home','Your vault, for life',"MyRealtyVault is your vault for everything about your home. Buying, selling, or owning, it is free to use, with or without an agent.",['Buying','Selling','Owning'],kicker='MyRealtyVault · Homeowner path'),
  T('check','It walks you through each step',"A checklist walks you through each step in plain words. Nothing is rushed, and you can skip what doesn't apply.",['Know your next step','Do them in any order'],kicker='Your checklist'),
  T('afford','Know your number',"If you are buying, start by knowing what you can comfortably afford, and what a home really costs each month.",['What can I afford?','Mortgage calculator'],kicker='Buying'),
  T('rate_done','Save the homes you love',"Search on the sites you already use, save the homes you like, and rate them with your own notes.",['Rate and add notes','Check any neighborhood'],kicker='Buying'),
  T('sd_menu','Send documents to anyone who needs them',"When someone needs your documents, send them straight from your vault. Your lender, your title company, your insurance company, your agent, or anyone else.",['Lender, title, insurance, your agent','Only the documents you choose'],kicker='Documents'),
  T('sd_menu2','A secure space for your documents',"Your vault is a secure space. Your documents are never emailed around as attachments. They stay in your vault, and each person gets a view-only link that expires, and that you can turn off at any time.",['Never sent as email attachments','View-only links that expire','Turn a link off any time'],kicker='Security'),
  T('walk','Selling or owning',"If you are selling, see what you would walk away with. If you own, keep your home's records, taxes, and upkeep in one place.",['What will I walk away with?','Your home and its records'],kicker='Selling and owning'),
  T('ask2','Help whenever you want it',"And whenever you have a question, ask MRV. It knows your search and your homes.",['Your virtual agent','Add your own agent any time'],kicker='Help'),
]),
'h_wrap':dict(kind='wrap',module='Homeowner path complete',title='Your vault is ready',file='Path_WrapUp',m=6,
  outro=('Congratulations!','You have finished the Homeowner path','Your vault is yours for life. Open it whenever you need it.'),beats=[
  T('home','Congratulations!',"Congratulations! You have finished the MyRealtyVault Homeowner path.",['Your vault and your checklist','Buying with a clear number','Documents, sent securely','Selling and owning'],kicker='Homeowner path complete',confetti=True),
  T('check_done','Your next step is waiting',"Open your vault, look at your next step, and tap Do it. Your vault will be here for every home that follows.",['Open your vault','Tap Do it'],kicker='What to do now',confetti=True),
]),
})
