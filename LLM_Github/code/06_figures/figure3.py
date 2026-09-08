import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))
import pandas as pd
import matplotlib.pyplot as plt
from config import FIG3_SOURCE, FIGURES
FIGURES.mkdir(parents=True,exist_ok=True)

def main():
    cn=pd.read_excel(FIG3_SOURCE,sheet_name="Fig.3c-1China_indirect")
    us=pd.read_excel(FIG3_SOURCE,sheet_name="Fig.3c-2US_indirect")
    d=pd.concat([cn,us],ignore_index=True)
    d["label"]=d["country"].astype(str)+" | "+d["outcome"].astype(str)+" | "+d["mechanism"].astype(str)
    fig,ax=plt.subplots(figsize=(8,8))
    y=range(len(d))
    ax.errorbar(d.indirect,y,xerr=[d.indirect-d.ci_low,d.ci_high-d.indirect],fmt="o")
    ax.axvline(0,lw=.8)
    ax.set_yticks(list(y),d.label)
    ax.set_xlabel("Bootstrap indirect effect")
    fig.tight_layout()
    fig.savefig(FIGURES/"Figure3c_indirect_effects.png",dpi=300)
    plt.close(fig)

    for sheet,label in [("Fig.3dChina_sensitivity","China"),("Fig.3eUS_sensitivity","United States")]:
        z=pd.read_excel(FIG3_SOURCE,sheet_name=sheet)
        fig,ax=plt.subplots(figsize=(7,4.5))
        for outcome,g in z.groupby("outcome"):
            ax.plot(g["window"],g["beta"],marker="o",label=str(outcome).replace("\n"," "))
        ax.axhline(0,lw=.8)
        ax.set_xlabel("Window (months)")
        ax.set_ylabel("Estimate")
        ax.legend(frameon=False)
        fig.tight_layout()
        fig.savefig(FIGURES/f"Figure3_sensitivity_{label.replace(' ','_')}.png",dpi=300)
        plt.close(fig)

if __name__=="__main__":
    main()
