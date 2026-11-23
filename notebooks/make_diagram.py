import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
f,ax=plt.subplots(figsize=(9,3.9)); ax.set_xlim(0,18); ax.set_ylim(0,8); ax.axis("off")
def box(x,y,w,h,t,c="#DDEBF7",ec="#1F4E79"):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.05",fc=c,ec=ec,lw=1.2)); ax.text(x+w/2,y+h/2,t,ha="center",va="center",fontsize=7.5)
def arr(x1,y1,x2,y2,t=None):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="-|>",mutation_scale=10,color="#444",lw=1))
    if t: ax.text((x1+x2)/2,(y1+y2)/2+.35,t,fontsize=6.5,ha="center")
AI="#FCE4D6"; AIE="#C55A11"
box(.2,3.2,2.6,1.6,"Customer ticket\n(email / web form /\nchat / social)")
box(3.6,3.2,2.6,1.6,"Google Sheet\n'Inbox' (new row)")
box(7.0,3.2,2.6,1.6,"AI Step 1 (P1)\nClassify category,\npriority, sentiment,\nteam, confidence",AI,AIE)
box(10.4,3.2,2.2,1.6,"Router:\nconfidence >= 0.6\nand not escalation?",c="#FFF2CC",ec="#BF9000")
box(13.4,5.3,2.8,1.6,"AI Step 2 (P2)\nDraft reply\n(human approves)",AI,AIE)
box(13.4,0.6,2.8,1.6,"Human review alert\nto Senior Support",c="#E2EFDA",ec="#548235")
box(16.4,5.3,1.5,1.6,"Triage_Output\nsheet + email",c="#E2EFDA",ec="#548235")
box(7.0,0.2,3.6,1.3,"Weekly: AI Step 3 (P3)\nmanager summary + analytics",AI,AIE)
arr(2.8,4,3.6,4);arr(6.2,4,7.0,4);arr(9.6,4,10.4,4)
arr(12.6,4.5,13.4,6,"Yes");arr(12.6,3.5,13.4,1.7,"No");arr(16.2,6.1,16.4,6.1)
ax.set_title("Figure 1: AI-enabled ticket triage process (orange = AI step)",fontsize=9)
plt.tight_layout(); plt.savefig("docs/process_diagram.png",dpi=200)
