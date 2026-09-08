import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
sys.path.append(str(Path(__file__).resolve().parents[2]))

import pandas as pd
from common import twfe_single_regressor, ensure_dirs
from config import TABLES, EVENT_DATE

SHIFTS = [6, 12, 18]

def placebo_one(df, true_event, months):
    true_event = pd.Timestamp(true_event)
    fake_event = true_event - pd.DateOffset(months=months)

    # Exclude all observations at or after the true event to prevent contamination.
    d = df.loc[pd.to_datetime(df["date"]) < true_event].copy()
    d["post_fake"] = (pd.to_datetime(d["date"]) >= fake_event).astype(int)
    d["did_fake"] = d["high"] * d["post_fake"]
    r = twfe_single_regressor(d, "composite", x_col="did_fake")
    return fake_event, r

def main():
    ensure_dirs(TABLES)
    rows = []
    for country, fn in [("China","china_prepared.csv"),("United States","us_prepared.csv")]:
        df = pd.read_csv(TABLES / fn)
        for m in SHIFTS:
            fake, r = placebo_one(df, EVENT_DATE[country], m)
            rows.append({
                "Country":country,
                "Pseudo-entry shift":f"-{m} months",
                "Pseudo-entry date":fake.strftime("%Y-%m"),
                **r,
            })
    out = pd.DataFrame(rows)
    out.to_csv(TABLES / "Supplementary_Table_8_temporal_placebo.csv", index=False)
    print(out.to_string(index=False))

if __name__ == "__main__":
    main()
