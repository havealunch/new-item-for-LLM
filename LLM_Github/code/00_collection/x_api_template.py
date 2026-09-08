"""
Workflow template for collecting public X posts through an authorized API.

This file deliberately does not hard-code credentials, bypass platform controls,
or claim to reproduce an undocumented historical endpoint. Supply an authorized
client and query consistent with the study's approved collection protocol.
"""
import os
import pandas as pd

REQUIRED_OUTPUT_COLUMNS = [
    "post_id", "user_hash", "platform", "country", "region_id", "region_name",
    "datetime", "year", "month", "raw_text", "clean_text", "language"
]

def normalize_x_records(records):
    rows = []
    for r in records:
        dt = pd.to_datetime(r["datetime"])
        rows.append({
            "post_id": str(r["post_id"]),
            "user_hash": str(r.get("user_hash", "")),
            "platform": "X",
            "country": "United States",
            "region_id": str(r["region_id"]),
            "region_name": r.get("region_name", ""),
            "datetime": dt,
            "year": dt.year,
            "month": dt.month,
            "raw_text": r["text"],
            "clean_text": r.get("clean_text", r["text"]),
            "language": r.get("language", "en"),
        })
    return pd.DataFrame(rows, columns=REQUIRED_OUTPUT_COLUMNS)

if __name__ == "__main__":
    raise SystemExit(
        "Template only. Connect an authorized X API/export source, then pass "
        "retrieved records to normalize_x_records()."
    )
