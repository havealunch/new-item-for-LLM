import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
sys.path.append(str(Path(__file__).resolve().parents[2]))

import pandas as pd
from config import TABLES, EVENT_DATE
from common import ensure_dirs

OUTCOMES = {
    "Loneliness":"loneliness_z",
    "Everyday stress":"stress_z",
    "Anxiety":"anxiety_z",
    "Depressive symptoms":"depression_z",
    "Severe mental distress":"severe_z",
}

WINDOWS = {
    "China": {
        "pre": ("2022-03-01","2023-02-28"),
        "post":("2023-09-01","2024-08-31"),
    },
    "United States": {
        "pre": ("2021-11-01","2022-10-31"),
        "post":("2023-05-01","2024-04-30"),
    }
}

def country_summary(country, df):
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    w = WINDOWS[country]
    rows = []
    for region, g in df.groupby("region"):
        rec = {"Country":country,"region":region}
        changes = {}
        for label, col in OUTCOMES.items():
            pre = g[g.date.between(*map(pd.Timestamp,w["pre"]))][col].mean()
            post = g[g.date.between(*map(pd.Timestamp,w["post"]))][col].mean()
            change = post-pre
            rec[label+"_change"] = change
            changes[label] = change
        rec["Dominant_decline_dimension"] = min(changes, key=changes.get)
        rec["Dominant_decline_value"] = changes[rec["Dominant_decline_dimension"]]
        rows.append(rec)
    return pd.DataFrame(rows)

def main():
    ensure_dirs(TABLES)
    all_rows = []
    for country, fn in [("China","china_prepared.csv"),("United States","us_prepared.csv")]:
        df = pd.read_csv(TABLES/fn)
        all_rows.append(country_summary(country,df))
    out = pd.concat(all_rows, ignore_index=True)
    out.to_csv(TABLES/"dominant_dimension_by_region.csv", index=False)
    share = (out.groupby(["Country","Dominant_decline_dimension"]).size()
              .rename("Count").reset_index())
    share["Share"] = share["Count"] / share.groupby("Country")["Count"].transform("sum")
    share.to_csv(TABLES/"dominant_dimension_share.csv", index=False)
    print(share.to_string(index=False))

if __name__ == "__main__":
    main()
