"""MyRealtyVault campus · Agent path, second batch (recorded 2026-11-13). Same format as films.py. Captures in capa/.
Adds lessons to Module 2 (Clients) and Module 3 (Buyers), and a new Module 8 (Your office)."""
PATH='Agent path'; CAP='capa'; PREFIX=''
M={2:'Module 2 · Clients',3:'Module 3 · Buyers',8:'Module 8 · Your office'}
def L(m,title,file,beats,**k): return dict(module=M[m],title=title,file='Lesson_'+file,beats=beats,m=m,**k)
def T(shot,cap,vo,pts=(),**k): return dict(talk=True,shot=shot,cap=cap,vo=vo,pts=list(pts),**k)
def B(shot,cap,vo,hl=(),**k): return dict(shot=shot,cap=cap,vo=vo,hl=list(hl),**k)
FILMS={
'a_msg':L(2,'Email or text a client','Email_or_text_a_client',[
  B('mail0','Tap Email on the card',"On a client's card, tap Email. You can write it yourself, or describe the goal and let the assistant draft it.",['chip','write','ai']),
  B('mail0','Write it myself',"Let's tap Write it myself.",['write'],click='write',shot2='mail1'),
  B('mail1','Subject and message',"Add a subject, and type your message in your own words.",['subj','body']),
  B('mail1','Send and log',"Send and log sends the email and records it in the client's history in one tap.",['send']),
  B('text1','Texts work the same way',"Tap Text to write a text message. It counts the characters as you type.",['body']),
  B('text1','Send it from your own phone',"Copy it, or tap Open in Messages to send it from your own phone, then tap Log as sent.",[[32,540,345,42]]),
  B('text1','Consent comes first',"To send texts through MyRealtyVault, first tick the box that confirms the client has agreed to receive them.",[[32,590,175,40],[32,638,372,62]]),
]),
'a_suggest':L(3,'Suggest a home to your buyer','Suggest_a_home_to_your_buyer',[
  B('bp','Matches sit on the buyer profile',"On a buyer's profile, Matches is where you line up homes for them.",['matches','start','mls','suggest']),
  B('bp','Tap Suggest a home',"To add a home you already have in mind, tap Suggest a home.",['suggest'],click='suggest',shot2='suggest'),
  B('suggest','Address and price',"Enter the address and the list price, and paste the listing link if you have one.",['addr','price','link']),
  B('suggest','Add to matches',"Tap Add to matches.",['add'],click='add',shot2='suggest_done'),
  B('suggest_done','Your pick, not sent yet',"The home is in Matches, marked as your pick, and not sent yet. Track it or drop it from here.",[[16,695,411,70]]),
  B('suggest_done','Send the list to your buyer',"When the list is ready, tap Send home to buyer.",[[150,472,175,46]],cam=(0,430,443)),
  B('bp','A daily digest keeps them warm',"Their saved search is watched for you, and your buyer can get a daily email of new matches.",['watch']),
]),
'a_offer':L(3,'Draft an offer','Draft_an_offer',[
  B('bp','Tap Log offer',"When your buyer is ready, open their profile and tap Log offer.",['offer'],click='offer',shot2='offer1'),
  B('offer1','Which home, and how much',"Choose the home, then enter the offer amount, the financing, the down payment, and the proposed closing date.",['home','amt','fin','down','close']),
  B('offer2','Earnest money and contingencies',"Add the earnest money, when the offer expires, and tick the contingencies: inspection, financing, appraisal.",['earnest','expires',[31,300,381,70]]),
  B('offer2','Save the draft offer',"Add anything notable, and tap Save the draft offer.",['note','save'],click='save',shot2='offer3'),
  B('offer3','Drafted, not sent',"The offer is saved as a draft. Offers made goes up, and the home shows Offer drafted, not sent.",[[40,872,190,30]]),
  B('offer5','Tap Send the offer',"When you are ready, tap Send the offer.",['offers','send'],click='send',shot2='offer4'),
  B('offer4','The letter carries your terms',"Enter the listing agent, and MyRealtyVault writes the letter with the terms exactly as you entered them. Nothing is sent until you send it.",[],cam='bottom'),
]),
'a_reports':L(8,'Read your reports','Read_your_reports',[
  B('reports','Three reports',"In Office, Reports has three views: your week, your commission, and your year.",['week','comm','year'],cam='top'),
  B('week','The habits that close deals',"Your week counts calls made, appointments set, and opportunities created, for this week, this month, or ninety days.",['tabs','calls','appts','opps']),
  B('comm','Commission, earned and projected',"Commission shows what you have earned on closed deals, and what is projected on deals under contract.",[[40,185,300,70]]),
  B('comm','Tap a deal to add its numbers',"A deal needs its numbers before it counts. Tap the deal.",['deal'],click='deal',shot2='comm2'),
  B('comm2','Price and percent, or a flat amount',"Enter the contract price and your percent, or a flat dollar amount, and tap Save.",['price','pct','flat','save'],click='save',shot2='comm3'),
  B('comm3','Your projected commission updates',"Your projected commission updates right away.",[[176,185,165,62]]),
]),
'a_card':L(8,'Set up your card','Set_up_your_card',[
  B('profile','Open Your card',"In Office, open Profile, look and logo, then tap Your card.",['card'],click='card',shot2='card0'),
  B('card0','Your name signs your letters',"Enter your agency name, and your own name. Your name signs your letters and emails.",['agency','name']),
  B('card0','Public email, phone, website',"Add the public email, phone, and website you want clients to see.",['email','phone','web']),
  B('card1','Social links go on every email',"Your social links appear at the bottom of every marketing email.",['social']),
  B('card1','Text message tone',"Text message tone tells the assistant how you sound, so drafted texts match your voice.",['tone']),
  B('card1','Add your logo and save',"Upload your logo, and tap Save profile.",['logo','save']),
]),
'a_look':L(8,'Choose your look','Choose_your_look',[
  B('profile','Open Look and logo',"In Profile, tap Look and logo.",['look'],click='look',shot2='look'),
  B('look','White or dark',"Choose white or dark. This is set for each device, so your phone and your computer can differ.",['white','dark']),
  B('look','One accent color',"Pick one accent color. Your clients' vaults use the same accent.",['blue','green','gold','violet']),
  B('look','Your brokerage logo',"Upload your brokerage logo, and choose what sits behind your home screen: your logo, a photo, or plain.",['logo',[37,795,369,60]],cam='bottom'),
  B('look','You see it live',"You see every change live. Let's try dark.",['dark'],click='dark',shot2='look_dark'),
  B('home_dark','Save to keep it',"Here is the home screen in dark. Tap Save profile to keep your choices.",[],cam='top'),
]),
'a_connect':L(8,'Put your showings on your own calendar','Put_your_showings_on_your_own_calendar',[
  B('profile','Open Connections',"In Profile, tap Connections.",['conn'],click='conn',shot2='conn'),
  B('conn','One link for your calendar',"Connect your calendar gives you one link. Subscribe once, and your showings, deadlines, and appointments appear on your own calendar.",['head','link']),
  B('conn','Copy link',"Tap Copy link.",['copy'],click='copy'),
  B('conn','Outlook, Google, or Apple',"Then follow the steps for Outlook, Google, or Apple. New items can take a few hours to show up.",[[37,400,369,120]]),
  B('weekly0','A weekly summary by email',"Also in Profile, Weekly summary sends you a recap of your week: new clients, showings, offers, and page views.",['head']),
  B('weekly','Pick the morning',"Pick the morning you want it, or leave it off.",['pick']),
]),
'a_bench':L(8,'Build your bench','Build_your_bench',[
  B('profile','Open Assistant and partners',"In Profile, tap Assistant and partners.",['asst'],click='asst',shot2='bench0'),
  B('bench0','Your bench',"Your bench is the lender, title company, and inspector you send clients to. Your clients see them on their team.",['bench',[37,345,369,60]]),
  B('bench0','Pick a role',"Pick a role, like Lender.",[[37,430,330,90]]),
  B('bench1','Name, company, phone, email',"Enter their name, company, phone, and email.",['name','co','phone','email']),
  B('bench1','Add to the bench',"Tap Add to the bench.",['add'],click='add',shot2='bench2'),
  B('bench2','They are on your bench',"They are on your bench, ready for every client you serve.",[[37,410,372,112]]),
  B('bench0','Your assistant’s voice',"On the same screen you can choose the voice your assistant speaks with. Tap Hear it to listen.",['voice','hear'],cam='top'),
]),
'a_help':L(8,'Get help and send feedback','Get_help_and_send_feedback',[
  B('help','Help is in Office',"In Office, tap Help. Ask how to do anything, or whether MyRealtyVault can do something.",[[50,605,340,90]],cam=(0,580,443)),
  B('help','Ask in your own words',"Type your question, or tap a starter. Let's ask how to add a new client.",['q1'],click='q1',shot2='help2'),
  B('help2','Step by step answers',"You get the steps, written for the screen you are using.",[],cam=(0,600,443)),
  B('help','Ideas and bugs go to the team',"Have a feature idea, or found a bug? Tap the button and tell us. It goes straight to the MyRealtyVault team.",[[283,774,112,27],[62,807,82,27]],cam='bottom'),
  B('help','Need a person?',"And if you need a person, tap Talk to the MRV team.",[[120,893,230,26]],cam='bottom'),
]),
'intro8':dict(kind='intro',module=M[8],title='Your office',file='Module8_Intro',m=8,outro=('Up next',"Let's go step by step",'Each lesson shows one job, tap by tap.'),beats=[
  T('reports','Know your numbers',"This last module is about the office behind your business. You will read your reports: your week, your commission, and your year.",['Calls, appointments, opportunities','Earned and projected commission']),
  T('look','Make it yours',"You will set up your card, and choose your look: white or dark, one accent color, and your logo.",['Your card signs every email','Your clients’ vaults match your look']),
  T('bench2','Connect and get help',"And you will put your showings on your own calendar, build your bench of partners, and learn where to get help.",['One calendar link','Lender, title, inspector','Help and feedback, built in']),
]),
}
