-- MRV film set (TEST ONLY — never prod). Fictional tenant "Harbor & Oak Realty" staged for marketing capture.
-- Applied to TEST 11/10/26 by Claude via the Supabase connector. Idempotent on fixed f115… ids.
-- The demo login (filmset.agent@jshinnovations.com, auth user f1150000-…-0001) was created directly in auth.users;
-- its password is NOT stored here — reset it in the Supabase dashboard if a session needs it.
-- Cast (all fictional): agent Ava Marshall; clients Maya Ellis, Grace Whitfield, Tom Ortiz, Priya Raman, Caleb Brooks,
-- Hannah Cole, Marcus Hale; requesters Daniel Reyes, Laura Kim, Ben Carter. Homes: 1420 Live Oak Ct, 88 Heron Bend Dr,
-- 2117 Magnolia Ridge Way, 517 Saddlebrook Ln (Ocala, FL — fictional addresses).
-- Before each take: reset the showing request so "Confirm" is live on camera:
update showings set status='requested', scheduled_at=date_trunc('day',now())+interval '1 day 16 hours'
 where id='f1150000-0000-0000-0005-000000000001';
-- Dates are relative to now(); re-run the showing/deadline block below before a new shoot so "this week" stays true:
update showings set scheduled_at = date_trunc('day',now())+interval '1 day 20 hours' where id='f1150000-0000-0000-0005-000000000002';
update showings set scheduled_at = date_trunc('day',now())+interval '2 days 17 hours' where id='f1150000-0000-0000-0005-000000000004';
update showings set scheduled_at = date_trunc('day',now())+interval '3 days 20 hours' where id='f1150000-0000-0000-0005-000000000003';

-- ============================== FULL SEED (as applied 11/10/26) ==============================
do $$
declare T uuid := 'a2222222-2222-2222-2222-222222222222';
        A uuid := (select id from tenant_members where email='filmset.agent@jshinnovations.com' and tenant_id='a2222222-2222-2222-2222-222222222222');
begin
insert into people (id, full_name, email, phone, vault_status) values
 ('f1150000-0000-0000-0001-000000000001','Maya Ellis','maya.ellis@example.com','(352) 555-0111','active'),
 ('f1150000-0000-0000-0001-000000000002','Grace Whitfield','grace.whitfield@example.com','(352) 555-0112','active'),
 ('f1150000-0000-0000-0001-000000000003','Tom Ortiz','tom.ortiz@example.com','(352) 555-0113','active'),
 ('f1150000-0000-0000-0001-000000000004','Priya Raman','priya.raman@example.com','(352) 555-0114','active'),
 ('f1150000-0000-0000-0001-000000000005','Caleb Brooks','caleb.brooks@example.com','(352) 555-0115','active'),
 ('f1150000-0000-0000-0001-000000000006','Hannah Cole','hannah.cole@example.com','(352) 555-0116','active'),
 ('f1150000-0000-0000-0001-000000000007','Marcus Hale','marcus.hale@example.com','(352) 555-0117','active')
on conflict (id) do nothing;
insert into properties (id,address_line,city,state,zip,beds,baths,sqft,lot_acres,year_built,description) values
 ('f1150000-0000-0000-0002-000000000001','1420 Live Oak Court','Ocala','FL','34471',4,3,2640,0.38,2019,'Bright split plan under a canopy of live oaks.'),
 ('f1150000-0000-0000-0002-000000000002','88 Heron Bend Drive','Ocala','FL','34482',3,2,1980,0.25,2014,'Lake views and a screened lanai.'),
 ('f1150000-0000-0000-0002-000000000003','2117 Magnolia Ridge Way','Ocala','FL','34476',5,4,3410,1.10,2021,'Farmhouse modern on an acre with a 3-car garage.'),
 ('f1150000-0000-0000-0002-000000000004','517 Saddlebrook Lane','Ocala','FL','34480',3,2,1820,0.30,2008,'Under contract.')
on conflict (id) do nothing;
insert into transactions (id,tenant_id,agent_id,side,stage,headline,next_step,next_step_due,opened_at,contract_price,commission_pct) values
 ('f1150000-0000-0000-0003-000000000001',T,A,'sell','listed','1420 Live Oak Court','Send weekly seller update',current_date+1,now()-interval '12 days',null,0.03),
 ('f1150000-0000-0000-0003-000000000002',T,A,'sell','showings','88 Heron Bend Drive','Review showing feedback with Priya',current_date+2,now()-interval '20 days',null,0.03),
 ('f1150000-0000-0000-0003-000000000003',T,A,'sell','listed','2117 Magnolia Ridge Way','Open house Saturday 1–3',current_date+4,now()-interval '5 days',null,0.03),
 ('f1150000-0000-0000-0003-000000000004',T,A,'buy','touring','Maya Ellis — 3BR near Paddock Park','Tour 88 Heron Bend tomorrow',current_date+1,now()-interval '9 days',null,0.03),
 ('f1150000-0000-0000-0003-000000000005',T,A,'buy','under_contract','Grace Whitfield — 517 Saddlebrook Lane','Inspection Thursday 10am',current_date+2,now()-interval '30 days',389000,0.03),
 ('f1150000-0000-0000-0003-000000000006',T,A,'buy','searching','Caleb Brooks — first home','Send three new matches',current_date+1,now()-interval '3 days',null,0.03),
 ('f1150000-0000-0000-0003-000000000007',T,A,'buy','lead','Hannah Cole — relocating from Atlanta','Intro call',current_date,now()-interval '1 day',null,0.03)
on conflict (id) do nothing;
insert into transaction_participants (transaction_id,person_id,role)
select ('f1150000-0000-0000-0003-00000000000'||i)::uuid, ('f1150000-0000-0000-0001-00000000000'||p)::uuid, 'primary'
from (values (1,3),(2,4),(3,7),(4,1),(5,2),(6,5),(7,6)) v(i,p) on conflict do nothing;
insert into contacts (tenant_id,person_id,owner_id,display_name,email,phone,stage,temperature,lead_source,source,intent,last_touch_at)
select T, p.id, A, p.full_name, p.email, p.phone, s.stage, s.temp, 'referral','portal', s.intent, now()-interval '1 day'
from people p join (values
 ('f1150000-0000-0000-0001-000000000001'::uuid,'active','hot','buying'), ('f1150000-0000-0000-0001-000000000002'::uuid,'active','hot','buying'),
 ('f1150000-0000-0000-0001-000000000003'::uuid,'active','warm','selling'), ('f1150000-0000-0000-0001-000000000004'::uuid,'active','hot','selling'),
 ('f1150000-0000-0000-0001-000000000005'::uuid,'active','warm','buying'), ('f1150000-0000-0000-0001-000000000006'::uuid,'lead','warm','buying'),
 ('f1150000-0000-0000-0001-000000000007'::uuid,'active','warm','selling')) s(pid,stage,temp,intent) on s.pid=p.id
on conflict (tenant_id, person_id) do nothing;
insert into listings (id,tenant_id,transaction_id,property_id,mls_number,status,list_price,original_price,listed_on,photo_count,views_7d,saves_count,showings_count,agent_id,commission_rate) values
 ('f1150000-0000-0000-0004-000000000001',T,'f1150000-0000-0000-0003-000000000001','f1150000-0000-0000-0002-000000000001','OM700142','active',489000,489000,current_date-12,36,214,31,6,A,0.03),
 ('f1150000-0000-0000-0004-000000000002',T,'f1150000-0000-0000-0003-000000000002','f1150000-0000-0000-0002-000000000002','OM700188','active',412500,425000,current_date-20,28,166,22,9,A,0.03),
 ('f1150000-0000-0000-0004-000000000003',T,'f1150000-0000-0000-0003-000000000003','f1150000-0000-0000-0002-000000000003','OM700231','active',725000,725000,current_date-5,48,301,44,3,A,0.03)
on conflict (id) do nothing;
insert into showings (id,tenant_id,transaction_id,listing_id,scheduled_at,duration_minutes,status,requester_name,requester_phone,requester_email,requester_sms_ok) values
 ('f1150000-0000-0000-0005-000000000001',T,'f1150000-0000-0000-0003-000000000002','f1150000-0000-0000-0004-000000000002',date_trunc('day',now())+interval '1 day 16 hours',30,'requested','Daniel Reyes','(352) 555-0171','daniel.reyes@example.com',true),
 ('f1150000-0000-0000-0005-000000000002',T,'f1150000-0000-0000-0003-000000000001','f1150000-0000-0000-0004-000000000001',date_trunc('day',now())+interval '1 day 20 hours',30,'confirmed','Maya Ellis','(352) 555-0111','maya.ellis@example.com',true),
 ('f1150000-0000-0000-0005-000000000003',T,'f1150000-0000-0000-0003-000000000003','f1150000-0000-0000-0004-000000000003',date_trunc('day',now())+interval '3 days 20 hours',45,'confirmed','Laura Kim','(352) 555-0172','laura.kim@example.com',true),
 ('f1150000-0000-0000-0005-000000000004',T,'f1150000-0000-0000-0003-000000000002','f1150000-0000-0000-0004-000000000002',date_trunc('day',now())+interval '2 days 17 hours',30,'confirmed','Ben Carter','(352) 555-0173','ben.carter@example.com',true)
on conflict (id) do nothing;
if not exists (select 1 from transaction_deadlines where transaction_id='f1150000-0000-0000-0003-000000000005') then
 insert into transaction_deadlines (tenant_id,transaction_id,kind,label,due_on,status,source) values
  (T,'f1150000-0000-0000-0003-000000000005','effective','Effective date',current_date-9,'done','manual'),
  (T,'f1150000-0000-0000-0003-000000000005','deposit','Escrow deposit',current_date-6,'done','manual'),
  (T,'f1150000-0000-0000-0003-000000000005','inspection','Inspection period ends',current_date+2,'pending','manual'),
  (T,'f1150000-0000-0000-0003-000000000005','appraisal','Appraisal',current_date+8,'pending','manual'),
  (T,'f1150000-0000-0000-0003-000000000005','financing','Loan approval',current_date+15,'pending','manual'),
  (T,'f1150000-0000-0000-0003-000000000005','closing','Closing',current_date+24,'pending','manual');
end if;
update preapprovals set rate_lock_expires = current_date+40 where tenant_id=T;
end $$;
