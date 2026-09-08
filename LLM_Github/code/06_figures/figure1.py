import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))
import pandas as pd
import matplotlib.pyplot as plt
from config import FIG1_SOURCE, FIGURES
FIGURES.mkdir(parents=True,exist_ok=True)

def main():
    # Event-time panel
    us=pd.read_excel(FIG1_SOURCE,sheet_name="Fig.1c_US_event")
    cn=pd.read_excel(FIG1_SOURCE,sheet_name="Fig.1c_CN_event")
    fig,ax=plt.subplots(figsize=(7,4.5))
    for d,label in [(us,"United States"),(cn,"China")]:
        ax.plot(d["event_month_plot"],d["effect"],label=label)
        ax.fill_between(d["event_month_plot"],d["CI95_low"],d["CI95_high"],alpha=.18)
    ax.axhline(0,lw=.8)
    ax.axvline(0,lw=.8,ls="--")
    ax.set_xlabel("Months relative to country-specific LLM entry")
    ax.set_ylabel("High-minus-low exposure effect")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURES/"Figure1c_event_time.png",dpi=300)
    plt.close(fig)

    d=pd.read_excel(FIG1_SOURCE,sheet_name="Fig.1d_effects")
    fig,ax=plt.subplots(figsize=(7,4.5))
    labels=[f"{o} — {c}" for o,c in zip(d.Outcome,d.Country)]
    y=range(len(d))
    ax.errorbar(d.Estimate,y,xerr=[d.Estimate-d.CI_low,d.CI_high-d.Estimate],fmt="o")
    ax.axvline(0,lw=.8)
    ax.set_yticks(list(y),labels)
    ax.set_xlabel("DID estimate")
    fig.tight_layout()
    fig.savefig(FIGURES/"Figure1d_effects.png",dpi=300)
    plt.close(fig)

if __name__=="__main__":
    main()
