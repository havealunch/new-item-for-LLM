import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
sys.path.append(str(Path(__file__).resolve().parents[2]))

import pandas as pd
from config import FIG4_SOURCE, FIG5_SOURCE, TABLES
from common import ensure_dirs
from importlib.util import spec_from_file_location, module_from_spec

# Reuse spline_fit without requiring a package install.
p = Path(__file__).with_name("01_context_bspline.py")
spec=spec_from_file_location("ctx",p)
ctx=module_from_spec(spec); spec.loader.exec_module(ctx)

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
            for dfs in [4,5,6]:
                curve=ctx.spline_fit(d,mod,y,dfs)
                curve["Country"]=country; curve["Moderator"]=mod
                curve["Specification"]=f"df={dfs}"
                rows.append(curve)
            lo,hi=d[mod].quantile([0.025,0.975])
            trim=d[d[mod].between(lo,hi)]
            curve=ctx.spline_fit(trim,mod,y,5)
            curve["Country"]=country; curve["Moderator"]=mod
            curve["Specification"]="df=5; trim 2.5-97.5%"
            rows.append(curve)
    pd.concat(rows,ignore_index=True).to_csv(TABLES/"Supplementary_Table_6_bspline_sensitivity_curves.csv",index=False)

if __name__=="__main__":
    main()
