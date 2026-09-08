import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
sys.path.append(str(Path(__file__).resolve().parents[2]))

import numpy as np
import pandas as pd
from scipy import stats
from common import twfe_single_regressor, bh_fdr, ensure_dirs
from config import TABLES

OUTCOMES = [
    ("Everyday stress","stress_z"),
    ("Loneliness","loneliness_z"),
    ("Anxiety","anxiety_z"),
    ("Depressive symptoms","depression_z"),
    ("Severe mental distress","severe_z"),
]

def main():
    ensure_dirs(TABLES)
    rows = []
    for country, fn in [("China","china_prepared.csv"),("United States","us_prepared.csv")]:
        df = pd.read_csv(TABLES / fn)
        for label, col in OUTCOMES:
            r = twfe_single_regressor(df, col)
            rows.append({"Country":country,"Outcome":label,**r})
    did = pd.DataFrame(rows)
    did["q_BH_10_tests"] = bh_fdr(did["p"])
    did.to_csv(TABLES / "Supplementary_Table_4_dimension_DID_FDR.csv", index=False)

    contrasts = []
    for label, _ in OUTCOMES:
        c = did[(did.Country=="China") & (did.Outcome==label)].iloc[0]
        u = did[(did.Country=="United States") & (did.Outcome==label)].iloc[0]
        diff = c.beta - u.beta
        se = float(np.sqrt(c.se**2 + u.se**2))
        z = diff/se
        p = float(2*stats.norm.sf(abs(z)))
        contrasts.append({
            "Outcome":label, "China_minus_US":diff, "SE":se,
            "CI_low":diff-1.96*se, "CI_high":diff+1.96*se, "p":p
        })
    con = pd.DataFrame(contrasts)
    con["q_BH_5_tests"] = bh_fdr(con["p"])
    con.to_csv(TABLES / "Supplementary_Table_3_cross_country_contrasts.csv", index=False)
    print(did.to_string(index=False))
    print(con.to_string(index=False))

if __name__ == "__main__":
    main()
