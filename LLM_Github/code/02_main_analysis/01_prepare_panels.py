import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
sys.path.append(str(Path(__file__).resolve().parents[2]))

import pandas as pd
from common import read_first_sheet, prepare_country_panel, ensure_dirs
from config import CHINA_PANEL, US_PANEL, EVENT_DATE, TABLES

def main():
    ensure_dirs(TABLES)
    for country, path in [("China", CHINA_PANEL), ("United States", US_PANEL)]:
        df = read_first_sheet(path)
        panel, cutoff = prepare_country_panel(df, EVENT_DATE[country])
        name = "china_prepared.csv" if country == "China" else "us_prepared.csv"
        panel.to_csv(TABLES / name, index=False)
        print(country, "N=", len(panel), "regions=", panel.region.nunique(), "cutoff=", cutoff)

if __name__ == "__main__":
    main()
