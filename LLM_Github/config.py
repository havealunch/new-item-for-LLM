from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
OUTPUTS = ROOT / "outputs"
TABLES = OUTPUTS / "tables"
FIGURES = OUTPUTS / "figures"

CHINA_PANEL = DATA / "China_panel.xlsx"
US_PANEL = DATA / "US_panel.xlsx"

FIG1_SOURCE = DATA / "Figure1_source.xlsx"
FIG2_SOURCE = DATA / "Figure2_source.xlsx"
FIG3_SOURCE = DATA / "Figure3_source.xlsx"
FIG4_SOURCE = DATA / "Figure4_China_source.xlsx"
FIG5_SOURCE = DATA / "Figure5_US_source.xlsx"

EVENT_DATE = {
    "China": "2023-03-01",
    "United States": "2022-11-01",
}
