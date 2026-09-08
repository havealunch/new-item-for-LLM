import pandas as pd

SCORE_COLS = [
    "loneliness_score", "stress_score", "anxiety_score",
    "depression_score", "severe_distress_score",
    "public_distress_score", "latent_distress_score"
]

def aggregate_monthly(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    required = ["region_id", "region_name", "year", "month"] + SCORE_COLS
    missing = [c for c in required if c not in df]
    if missing:
        raise KeyError(f"Missing fields: {missing}")

    out = (
        df.groupby(["country", "region_id", "region_name", "year", "month"], as_index=False)
          .agg(**{c: (c, "mean") for c in SCORE_COLS},
               Social_Media_Post_Count=("post_id", "count"))
    )
    out.to_csv(output_csv, index=False)

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("input_csv")
    ap.add_argument("output_csv")
    args = ap.parse_args()
    aggregate_monthly(args.input_csv, args.output_csv)
