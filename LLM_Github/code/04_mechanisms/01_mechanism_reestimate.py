"""
Re-estimate pathway regressions when the deposited panel contains the mechanism
indices used in the manuscript.

Because the exact historical SEM preprocessing/standardization choices must
match the archived analysis, this script is intentionally transparent about the
implemented model: region-level pre/post change-score regressions.

Figure 3 can be reproduced exactly from the deposited Figure3 source workbook
using code/06_figures/figure3.py.
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
sys.path.append(str(Path(__file__).resolve().parents[2]))

import numpy as np
import pandas as pd
import statsmodels.api as sm
from config import CHINA_PANEL, US_PANEL, TABLES, EVENT_DATE
from common import read_first_sheet, canonicalize_panel, find_col, ALIASES, ensure_dirs

MECH_ALIASES = {
    "AI companionship":["AI_Companionship_Potential_人工智能陪伴潜力","AI_Companionship_Potential"],
    "Disclosure migration":["Disclosure_Migration_Index_表达迁移指数","Disclosure_Migration_Index"],
    "Help substitution":["AI_Substitution_Risk_人工智能替代风险","AI_Substitution_Risk"],
}
EXPOSURE_ALIASES = ALIASES["exposure"]

def get_col(df, names):
    for c in names:
        if c in df: return c
    raise KeyError(names)

def z(s):
    return (s-s.mean())/s.std(ddof=0)

def region_change(df, event):
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"] if "Date" in df else pd.to_datetime(dict(year=df["Year"],month=df["Month"],day=1)))
    e = pd.Timestamp(event)
    pre = df[df.Date < e]
    post = df[df.Date >= e]
    num = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    a = pre.groupby("region")[num].mean()
    b = post.groupby("region")[num].mean()
    return (b-a).dropna(how="all")

def main():
    ensure_dirs(TABLES)
    rows=[]
    for country,path in [("China",CHINA_PANEL),("United States",US_PANEL)]:
        raw=read_first_sheet(path)
        # canonicalize region only while keeping original mechanism names
        region_col = next(c for c in ALIASES["region"] if c in raw.columns)
        raw = raw.rename(columns={region_col:"region"})
        if "Date" not in raw and {"Year","Month"}.issubset(raw.columns):
            raw["Date"]=pd.to_datetime(dict(year=raw.Year,month=raw.Month,day=1))
        ch = region_change(raw, EVENT_DATE[country])
        exp = get_col(ch, EXPOSURE_ALIASES)
        for mech,names in MECH_ALIASES.items():
            try: mc=get_col(ch,names)
            except KeyError: continue
            d=pd.DataFrame({"x":z(ch[exp]),"m":z(ch[mc])}).dropna()
            fit=sm.OLS(d.m,sm.add_constant(d.x)).fit(cov_type="HC3")
            rows.append({"Country":country,"mechanism":mech,"a_coef":fit.params["x"],"a_se":fit.bse["x"],"a_p":fit.pvalues["x"]})
    pd.DataFrame(rows).to_csv(TABLES/"mechanism_a_paths_reestimated.csv",index=False)

if __name__=="__main__":
    main()
