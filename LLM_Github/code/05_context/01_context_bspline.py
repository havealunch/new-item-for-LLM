import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
sys.path.append(str(Path(__file__).resolve().parents[2]))

import numpy as np
import pandas as pd
import statsmodels.api as sm
from patsy import dmatrix
from config import FIG4_SOURCE, FIG5_SOURCE, TABLES
from common import ensure_dirs

def spline_fit(df, x, y, df_spline=5, grid_n=160):
    d=df[[x,y]].dropna().copy()
    B=dmatrix(f"bs(x, df={df_spline}, degree=3, include_intercept=False)",
              {"x":d[x]}, return_type="dataframe")
    X=sm.add_constant(B,has_constant="add")
    fit=sm.OLS(d[y].to_numpy(),X).fit(cov_type="HC3")
    grid=np.linspace(d[x].min(),d[x].max(),grid_n)
    Bg=dmatrix(f"bs(x, df={df_spline}, degree=3, include_intercept=False)",
               {"x":grid}, return_type="dataframe")
    Xg=sm.add_constant(Bg,has_constant="add")
    pred=fit.get_prediction(Xg).summary_frame(alpha=0.05)
    return pd.DataFrame({"X":grid,"fit":pred["mean"],"CI_low":pred["mean_ci_lower"],"CI_high":pred["mean_ci_upper"]})

def main():
    ensure_dirs(TABLES)
    specs=[
        ("China",FIG4_SOURCE,"Panel_e_Cities","Psychological_change_Post_minus_Pre",
         ["Digital_readiness","AI_readiness","Mental_health_service","Healthcare_scarcity"]),
        ("United States",FIG5_SOURCE,"Panel_e_Counties","Psychological_change_Post_minus_Pre",
         ["DIGITAL_READINESS_FINAL","TECH_READINESS_FINAL","MENTAL_HEALTH_SERVICE_FINAL","HEALTHCARE_SCARCITY_FINAL"]),
    ]
    rows=[]
    for country,path,sheet,y,mods in specs:
        d=pd.read_excel(path,sheet_name=sheet)
        for mod in mods:
            curve=spline_fit(d,mod,y,5)
            curve["Country"]=country
            curve["Moderator"]=mod
            rows.append(curve)
    pd.concat(rows,ignore_index=True).to_csv(TABLES/"context_bspline_df5_reestimated.csv",index=False)

if __name__=="__main__":
    main()
