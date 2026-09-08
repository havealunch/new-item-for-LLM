import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
sys.path.append(str(Path(__file__).resolve().parents[2]))

import pandas as pd
from common import bh_fdr, ensure_dirs
from config import FIG3_SOURCE, TABLES

def main():
    ensure_dirs(TABLES)
    xl = pd.ExcelFile(FIG3_SOURCE)
    pieces=[]
    for s in ["Fig.3a-1China_a_paths","Fig.3a-2China_b_paths","Fig.3b-1US_a_paths","Fig.3b-2US_b_paths"]:
        if s not in xl.sheet_names: continue
        d=pd.read_excel(FIG3_SOURCE,sheet_name=s)
        pcol = "a_p" if "a_p" in d else "b_p"
        kind = "a" if pcol=="a_p" else "b"
        z=d.copy()
        z["path_type"]=kind
        z["p_value"]=z[pcol]
        pieces.append(z)
    out=pd.concat(pieces,ignore_index=True,sort=False)
    out["q_BH_24_paths"]=bh_fdr(out["p_value"])
    out.to_csv(TABLES/"Supplementary_Table_5_SEM_path_FDR.csv",index=False)

if __name__=="__main__":
    main()
