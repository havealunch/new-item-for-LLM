import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))
import pandas as pd
import matplotlib.pyplot as plt
from config import FIG5_SOURCE, FIGURES
FIGURES.mkdir(parents=True,exist_ok=True)

def main():
    d=pd.read_excel(FIG5_SOURCE,sheet_name="Panels_a-d_Curves")
    for panel,g in d.groupby("Panel"):
        fig,ax=plt.subplots(figsize=(5.5,4.3))
        ax.plot(g.X,g.Smooth_fit)
        ax.fill_between(g.X,g.CI_low,g.CI_high,alpha=.18)
        ax.axhline(0,lw=.8)
        ax.set_xlabel(str(panel))
        ax.set_ylabel("Post − Pre composite distress")
        fig.tight_layout()
        safe=str(panel).replace("/","_")
        fig.savefig(FIGURES/f"Figure5_{safe}.png",dpi=300)
        plt.close(fig)

    e=pd.read_excel(FIG5_SOURCE,sheet_name="Panel_e_Counties")
    fig,ax=plt.subplots(figsize=(6,5))
    sc=ax.scatter(e.DIGITAL_READINESS_FINAL,e.HEALTHCARE_SCARCITY_FINAL,
                  c=e.Psychological_change_Post_minus_Pre,s=8)
    ax.set_xlabel("Digital readiness")
    ax.set_ylabel("Healthcare scarcity")
    fig.colorbar(sc,ax=ax,label="Post − Pre distress")
    fig.tight_layout()
    fig.savefig(FIGURES/"Figure5e_US_context_joint.png",dpi=300)
    plt.close(fig)

if __name__=="__main__":
    main()
