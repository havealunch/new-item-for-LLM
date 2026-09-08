import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
sys.path.append(str(Path(__file__).resolve().parents[2]))

import numpy as np
import pandas as pd
from scipy import stats
from common import two_way_demean, cluster_covariance, ensure_dirs
from config import TABLES

def dynamic_twfe(df, y_col="composite", ref=-1):
    d = df[[y_col,"high","event_time","region","calendar_month"]].dropna().copy()
    event_times = sorted(int(k) for k in d["event_time"].unique() if int(k) != ref)

    Xraw = np.column_stack([
        ((d["event_time"].to_numpy() == k) & (d["high"].to_numpy() == 1)).astype(float)
        for k in event_times
    ])
    y = two_way_demean(d[y_col], d["region"], d["calendar_month"])
    X = np.column_stack([
        two_way_demean(Xraw[:,j], d["region"], d["calendar_month"])
        for j in range(Xraw.shape[1])
    ])

    keep = np.var(X, axis=0) > 1e-12
    X = X[:, keep]
    event_times = [k for k, z in zip(event_times, keep) if z]

    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    resid = y - X @ beta
    V = cluster_covariance(X, resid, d["region"])
    se = np.sqrt(np.clip(np.diag(V), 0, np.inf))

    coef = pd.DataFrame({
        "event_time":event_times,
        "beta":beta,
        "se":se,
        "ci_low":beta-1.96*se,
        "ci_high":beta+1.96*se,
    })

    return coef, V, d

def joint_test(coef, V, which):
    idx = [i for i,k in enumerate(coef.event_time) if which(int(k))]
    if not idx:
        return {"Wald":np.nan,"df":0,"p":np.nan}
    b = coef.beta.to_numpy()[idx]
    VV = V[np.ix_(idx, idx)]
    W = float(b @ np.linalg.pinv(VV) @ b)
    df = len(idx)
    p = float(stats.chi2.sf(W, df))
    return {"Wald":W, "df":df, "p":p}

def main():
    ensure_dirs(TABLES)
    summary = []
    for country, fn in [("China","china_prepared.csv"),("United States","us_prepared.csv")]:
        df = pd.read_csv(TABLES / fn)
        coef, V, d = dynamic_twfe(df, "composite", ref=-1)
        coef.insert(0, "Country", country)
        coef.to_csv(TABLES / f"event_study_{'china' if country=='China' else 'us'}.csv", index=False)

        all_pre = joint_test(coef.drop(columns="Country"), V, lambda k: k < 0 and k != -1)
        last12 = joint_test(coef.drop(columns="Country"), V, lambda k: -12 <= k < 0 and k != -1)
        summary += [
            {"Country":country, "Window":"All available pre-entry months", **all_pre},
            {"Country":country, "Window":"Last 12 pre-entry months", **last12},
        ]
    out = pd.DataFrame(summary)
    out.to_csv(TABLES / "Supplementary_Table_7_pretrend_joint_tests.csv", index=False)
    print(out.to_string(index=False))

if __name__ == "__main__":
    main()
