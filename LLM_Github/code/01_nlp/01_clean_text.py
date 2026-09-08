import re
import pandas as pd

URL = re.compile(r"https?://\S+|www\.\S+")
SPACE = re.compile(r"\s+")

def clean_text(text):
    text = "" if pd.isna(text) else str(text)
    text = URL.sub(" ", text)
    text = re.sub(r"[@#]\S+", " ", text)
    text = SPACE.sub(" ", text).strip()
    return text

def clean_file(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    if "raw_text" not in df:
        raise KeyError("raw_text is required")
    df["clean_text"] = df["raw_text"].map(clean_text)
    df.to_csv(output_csv, index=False)

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("input_csv")
    ap.add_argument("output_csv")
    args = ap.parse_args()
    clean_file(args.input_csv, args.output_csv)
