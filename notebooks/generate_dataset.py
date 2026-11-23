"""Generates the SYNTHETIC (hypothetical) support-ticket dataset for NovaCart (fictional company).
All records are artificial. Seeded for reproducibility."""
import numpy as np, pandas as pd
rng = np.random.default_rng(2026)
N = 400
cats = {
 "Delivery Delay":      (0.24,"Logistics",[.05,.25,.50,.20],.60),
 "Refund / Return":     (0.18,"Billing",  [.03,.22,.55,.20],.45),
 "Payment Failure":     (0.14,"Billing",  [.20,.45,.30,.05],.55),
 "Damaged / Wrong Item":(0.12,"Logistics",[.05,.30,.50,.15],.65),
 "Account / Login":     (0.12,"Tech Support",[.10,.30,.40,.20],.35),
 "Product Inquiry":     (0.12,"General Support",[.00,.05,.35,.60],.10),
 "Complaint / Escalation":(0.08,"Senior Support",[.30,.45,.20,.05],.85),
}
names=list(cats); shares=np.array([cats[c][0] for c in names]); shares/=shares.sum()
texts = {
 "Delivery Delay":["My order {o} was due 5 days ago and tracking has not updated. Where is it?","Package still not delivered after 8 days. I need it urgently for a gift.","Courier marked order {o} as delivered but I never received anything."],
 "Refund / Return":["I returned order {o} two weeks ago and have not received my refund.","How do I return a product that does not fit? The return link is not working.","Refund was issued for less than the amount I paid on order {o}."],
 "Payment Failure":["Money was deducted from my account but order {o} shows payment failed.","Payment keeps failing at checkout with my UPI app.","I was charged twice for order {o}. Please reverse one payment."],
 "Damaged / Wrong Item":["The item in order {o} arrived broken. Photos attached.","I received a different colour than what I ordered.","Parcel was open and a product is missing from order {o}."],
 "Account / Login":["I cannot log in, the OTP never arrives.","Please update the mobile number on my account.","My account was locked after several password attempts."],
 "Product Inquiry":["Is this product available in size M and when will it restock?","Does the blender come with a warranty and what does it cover?","Can you tell me if this item is suitable for sensitive skin?"],
 "Complaint / Escalation":["This is the third time I am contacting you about order {o}. No one has solved it. I want a manager.","Terrible service. I will post a review and dispute the charge if this is not fixed today.","Nobody has replied to me for three days. Escalate this immediately."],
}
channels=["Email","Web Form","Chat","Social Media"]; ch_p=[.35,.30,.22,.13]
segments=["New","Regular","Premium"]; seg_p=[.30,.55,.15]
sla={"Urgent":2,"High":6,"Medium":12,"Low":24}
hw=np.array([1,1,1,1,1,2,3,5,8,10,10,9,8,8,8,8,7,6,5,4,3,2,2,1],float); hw/=hw.sum()
start=pd.Timestamp("2026-09-01")
rows=[]
for i in range(N):
    c=rng.choice(names,p=shares); share,team,pp,negp=cats[c]
    pr=rng.choice(["Urgent","High","Medium","Low"],p=pp)
    ch=rng.choice(channels,p=ch_p); seg=rng.choice(segments,p=seg_p)
    day=int(rng.integers(0,56)); hour=int(rng.choice(range(24),p=hw))
    created=start+pd.Timedelta(days=day,hours=hour,minutes=int(rng.integers(0,60)))
    r=rng.random()
    sent="Negative" if r<negp else ("Neutral" if r<negp+(1-negp)*.6 else "Positive")
    if sent=="Positive" and c not in ("Product Inquiry","Account / Login"): sent="Neutral"
    mis_p={"Delivery Delay":.12,"Refund / Return":.22,"Payment Failure":.18,"Damaged / Wrong Item":.25,"Account / Login":.10,"Product Inquiry":.08,"Complaint / Escalation":.30}[c]
    if ch=="Social Media": mis_p+=.10
    misrouted=bool(rng.random()<mis_p)
    load = 1.0 + (0.5 if hour in (9,10,11) else 0) + (0.4 if created.dayofweek==0 else 0)
    base={"Urgent":1.2,"High":3.2,"Medium":6.5,"Low":13.0}[pr]*load
    frt=float(rng.lognormal(np.log(base),0.55))
    if ch=="Social Media": frt*=1.3
    reassign=int(rng.integers(1,3)) if misrouted else 0
    frt+=sum(rng.uniform(1.5,4.0,size=reassign)) if reassign else 0
    res=frt+float(rng.lognormal(np.log({"Urgent":10,"High":18,"Medium":30,"Low":40}[pr]),0.5))
    breached=bool(frt>sla[pr])
    score=4.6-0.9*min(frt/sla[pr],3)/1.5-(0.7 if misrouted else 0)-(0.3 if sent=="Negative" else 0)+rng.normal(0,.5)
    csat=int(np.clip(round(score),1,5)) if rng.random()<0.68 else np.nan
    text=str(rng.choice(texts[c])).format(o=f"NC{rng.integers(100000,999999)}")
    assigned=team if not misrouted else str(rng.choice([t for t in ["Logistics","Billing","Tech Support","General Support","Senior Support"] if t!=team]))
    rows.append(dict(created_at=created,channel=ch,customer_segment=seg,category=c,priority=pr,sentiment=sent,
        correct_team=team,assigned_team=assigned,misrouted=misrouted,reassignments=reassign,
        sla_target_hrs=sla[pr],first_response_hrs=round(frt,2),resolution_hrs=round(res,2),sla_breached=breached,csat=csat,ticket_text=text))
df=pd.DataFrame(rows).sort_values("created_at").reset_index(drop=True)
df.insert(0,"ticket_id",[f"TK-{1001+i}" for i in range(len(df))])
df["created_at"]=df["created_at"].dt.strftime("%Y-%m-%d %H:%M")
df.to_csv("data/synthetic_support_tickets.csv",index=False)
print(df.shape)
print(df.head(3).T)
