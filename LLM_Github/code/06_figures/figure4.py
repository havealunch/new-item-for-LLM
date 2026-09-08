import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))
import pandas as pd
import matplotlib.pyplot as plt
from config import FIG4_SOURCE, FIGURES
FIGURES.mkdir(parents=True,exist_ok=True)

def main():
    d=pd.read_excel(FIG4_SOURCE,sheet_name="Panels_a-d_Curves")
    for panel,g in d.groupby("Panel"):
        fig,ax=plt.subplots(figsize=(5.5,4.3))
        ax.plot(g.X,g.Spline_fit)
        ax.fill_between(g.X,g.CI_low,g.CI_high,alpha=.18)
        ax.axhline(0,lw=.8)
        ax.set_xlabel(g.Moderator.iloc[0])
        ax.set_ylabel("Post − Pre composite distress")
        fig.tight_layout()
        fig.savefig(FIGURES/f"Figure4{panel}_China_context.png",dpi=300)
        plt.close(fig)

    e=pd.read_excel(FIG4_SOURCE,sheet_name="Panel_e_Cities")
    fig,ax=plt.subplots(figsize=(6,5))
    sc=ax.scatter(e.Digital_readiness,e.Healthcare_scarcity,
                  c=e.Psychological_change_Post_minus_Pre,s=20)
    ax.set_xlabel("Digital readiness")
    ax.set_ylabel("Healthcare scarcity")
    fig.colorbar(sc,ax=ax,label="Post − Pre distress")
    fig.tight_layout()
    fig.savefig(FIGURES/"Figure4e_China_context_joint.png",dpi=300)
    plt.close(fig)

if __name__=="__main__":
    main()
