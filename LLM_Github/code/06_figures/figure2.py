import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))
import pandas as pd
import matplotlib.pyplot as plt
from config import FIG2_SOURCE, FIGURES
FIGURES.mkdir(parents=True,exist_ok=True)

def main():
    d=pd.read_excel(FIG2_SOURCE,sheet_name="Fig2a_DID")
    outcomes=list(dict.fromkeys(d.Outcome))
    fig,ax=plt.subplots(figsize=(7,5))
    offsets={"China":-.13,"United States":.13}
    for country,g in d.groupby("Country"):
        yy=[outcomes.index(o)+offsets[country] for o in g.Outcome]
        ax.errorbar(g.Estimate,yy,xerr=[g.Estimate-g.CI_low,g.CI_high-g.Estimate],
                    fmt="o",label=country)
    ax.axvline(0,lw=.8)
    ax.set_yticks(range(len(outcomes)),outcomes)
    ax.set_xlabel("DID estimate")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURES/"Figure2a_dimension_DID.png",dpi=300)
    plt.close(fig)

    s=pd.read_excel(FIG2_SOURCE,sheet_name="Fig2d-eDominant_dimension_share")
    fig,ax=plt.subplots(figsize=(7,4.5))
    pivot=s.pivot(index="Dominant_Decline_Dimension_主导下降维度",columns="Country_国家",values="Share_地区占比")
    pivot.plot(kind="bar",ax=ax)
    ax.set_ylabel("Share of regions")
    ax.set_xlabel("")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURES/"Figure2_dominant_dimension_share.png",dpi=300)
    plt.close(fig)

if __name__=="__main__":
    main()
