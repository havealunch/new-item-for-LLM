"""
Workflow template for normalizing authorized/public Weibo records.

No undocumented scraping endpoint is embedded here. Provide records collected
under the platform's permitted interface or archived study workflow.
"""
import pandas as pd

REQUIRED_OUTPUT_COLUMNS = [
    "post_id", "user_hash", "platform", "country", "region_id", "region_name",
    "datetime", "year", "month", "raw_text", "clean_text", "language"
]

def normalize_weibo_records(records):
    rows = []
    for r in records:
        dt = pd.to_datetime(r["datetime"])
        rows.append({
            "post_id": str(r["post_id"]),
            "user_hash": str(r.get("user_hash", "")),
            "platform": "Weibo",
            "country": "China",
            "region_id": str(r["region_id"]),
            "region_name": r.get("region_name", ""),
            "datetime": dt,
            "year": dt.year,
            "month": dt.month,
            "raw_text": r["text"],
            "clean_text": r.get("clean_text", r["text"]),
            "language": r.get("language", "zh"),
        })
    return pd.DataFrame(rows, columns=REQUIRED_OUTPUT_COLUMNS)

if __name__ == "__main__":
    raise SystemExit(
        "Template only. Connect the authorized/original Weibo data source, then "
        "pass retrieved records to normalize_weibo_records()."
    )
