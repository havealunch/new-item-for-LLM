import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
sys.path.append(str(Path(__file__).resolve().parents[2]))

import pandas as pd
from common import twfe_single_regressor, ensure_dirs
from config import TABLES

OUTCOMES = {
    "Composite distress": "composite",
    "Public distress": "public_distress_z",
    "Latent distress": "latent_distress_z",
}

def main():
    ensure_dirs(TABLES)
    rows = []
    for country, fn in [("China","china_prepared.csv"),("United States","us_prepared.csv")]:
        df = pd.read_csv(TABLES / fn)
        for label, col in OUTCOMES.items():
            if col not in df:
                continue
            r = twfe_single_regressor(df, col)
            rows.append({"Country":country, "Outcome":label, **r})
    out = pd.DataFrame(rows)
    out.to_csv(TABLES / "main_twfe_did.csv", index=False)
    print(out.to_string(index=False))

if __name__ == "__main__":
    main()
