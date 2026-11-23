import pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt, json
df=pd.read_csv("data/synthetic_support_tickets.csv",parse_dates=["created_at"])
df["week"]=df.created_at.dt.to_period("W").apply(lambda p:p.start_time)
plt.rcParams.update({"font.size":9,"axes.spines.top":False,"axes.spines.right":False})
C="#1F4E79"; A="#C55A11"
out={}
out["n"]=len(df)
out["breach_rate"]=df.sla_breached.mean()
out["misroute_rate"]=df.misrouted.mean()
out["mean_frt"]=df.first_response_hrs.mean(); out["median_frt"]=df.first_response_hrs.median()
out["mean_res"]=df.resolution_hrs.mean()
out["csat_mean"]=df.csat.mean(); out["csat_n"]=int(df.csat.notna().sum())
cat=df.groupby("category").agg(tickets=("ticket_id","count"),breach=("sla_breached","mean"),misroute=("misrouted","mean"),frt=("first_response_hrs","mean"),csat=("csat","mean")).sort_values("tickets",ascending=False)
pri=df.groupby("priority").agg(tickets=("ticket_id","count"),breach=("sla_breached","mean"),frt=("first_response_hrs","mean"),sla=("sla_target_hrs","first")).loc[["Urgent","High","Medium","Low"]]
ch=df.groupby("channel").agg(tickets=("ticket_id","count"),breach=("sla_breached","mean"),frt=("first_response_hrs","mean"),mis=("misrouted","mean"))
mis=df.groupby("misrouted").agg(frt=("first_response_hrs","mean"),res=("resolution_hrs","mean"),csat=("csat","mean"),breach=("sla_breached","mean"))
df["hour"]=df.created_at.dt.hour
hr=df.groupby("hour").size()
df["frt_band"]=pd.cut(df.first_response_hrs/df.sla_target_hrs,[0,.5,1,2,100],labels=["<50% of SLA","50-100%","1-2x SLA",">2x SLA"])
band=df.groupby("frt_band",observed=True).csat.agg(["mean","count"])
sent=df.groupby("sentiment").agg(tickets=("ticket_id","count"),breach=("sla_breached","mean"),csat=("csat","mean"))
print(cat.round(3));print(pri.round(3));print(ch.round(3));print(mis.round(3));print(band.round(2));print(sent.round(2))
print({k:round(float(v),3) for k,v in out.items()})
cat.round(3).to_csv("results/by_category.csv");pri.round(3).to_csv("results/by_priority.csv");ch.round(3).to_csv("results/by_channel.csv")
# charts
f,ax=plt.subplots(figsize=(6,3.2)); cat.tickets.sort_values().plot.barh(ax=ax,color=C); ax.set_xlabel("Tickets"); ax.set_title("Ticket volume by category (n=400, synthetic)"); plt.tight_layout(); plt.savefig("results/charts/c1_volume_by_category.png",dpi=200); plt.close()
f,ax=plt.subplots(figsize=(6,3.2)); (pri.breach*100).plot.bar(ax=ax,color=A,rot=0); ax.set_ylabel("% breaching SLA"); ax.set_xlabel("");ax.set_title("SLA breach rate by priority (synthetic)")
for i,v in enumerate(pri.breach*100): ax.text(i,v+1,f"{v:.0f}%",ha="center")
plt.tight_layout(); plt.savefig("results/charts/c2_breach_by_priority.png",dpi=200); plt.close()
f,ax=plt.subplots(figsize=(6,3.2)); (cat.misroute*100).sort_values().plot.barh(ax=ax,color=C); ax.set_xlabel("% tickets routed to wrong team"); ax.set_ylabel("");ax.set_title("Manual misrouting rate by category (synthetic)"); plt.tight_layout(); plt.savefig("results/charts/c3_misroute_by_category.png",dpi=200); plt.close()
f,ax=plt.subplots(figsize=(6,3.2)); band["mean"].plot.bar(ax=ax,color=C,rot=0); ax.set_ylim(1,5); ax.set_ylabel("Average CSAT (1-5)"); ax.set_xlabel("First response time relative to SLA target"); ax.set_title("Slower responses, lower satisfaction (synthetic)")
for i,v in enumerate(band["mean"]): ax.text(i,v+.05,f"{v:.2f}",ha="center")
plt.tight_layout(); plt.savefig("results/charts/c4_csat_vs_response.png",dpi=200); plt.close()
wk=df.groupby("week").agg(n=("ticket_id","count"),b=("sla_breached","mean"))
f,ax=plt.subplots(figsize=(6,3.2)); ax.bar(range(len(wk)),wk.n,color=C); ax.set_ylabel("Tickets per week"); ax2=ax.twinx(); ax2.plot(range(len(wk)),wk.b*100,color=A,marker="o"); ax2.set_ylabel("SLA breach %",color=A); ax2.spines["right"].set_visible(True); ax.set_xticks(range(len(wk))); ax.set_xticklabels([f"W{i+1}" for i in range(len(wk))]); ax.set_title("Weekly volume and SLA breach rate (synthetic)"); plt.tight_layout(); plt.savefig("results/charts/c5_weekly.png",dpi=200); plt.close()
# Scenario model (ASSUMPTION-BASED, hypothetical - not measured)
VOL=5000; COST=300  # assumed monthly tickets and INR cost per agent-hour
scen={"Conservative":(0.30,0.20,2),"Moderate":(0.50,0.35,4),"Optimistic":(0.70,0.50,6)}
rows=[]
for k,(mr,br,mins) in scen.items():
    new_mis=out["misroute_rate"]*(1-mr); new_breach=out["breach_rate"]*(1-br)
    h_mis=VOL*(out["misroute_rate"]-new_mis)*0.5   # assume 0.5 agent-hr wasted per misrouted ticket
    h_triage=VOL*mins/60                            # assumed minutes saved per ticket (classify + draft)
    tot=h_mis+h_triage
    rows.append(dict(scenario=k,assumed_misroute_cut_pct=int(mr*100),assumed_breach_cut_pct=int(br*100),assumed_min_saved_per_ticket=mins,
      misroute_after_pct=round(new_mis*100,1),breach_after_pct=round(new_breach*100,1),hours_saved_month=round(tot),inr_saved_month=round(tot*COST)))
sc=pd.DataFrame(rows); print(sc.to_string()); sc.to_csv("results/scenario_model.csv",index=False)
json.dump({k:float(v) for k,v in out.items()},open("results/headline_metrics.json","w"))
