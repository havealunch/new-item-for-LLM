from __future__ import annotations
import numpy as np
import pandas as pd
from scipy import stats
from pathlib import Path

# Column aliases found in the deposited bilingual workbooks.
ALIASES = {
    "region": [
        "region_id", "Region_ID", "City_Code_城市代码", "City_Code", "FIPS",
        "FIPS_County_Code", "Region_ID_地区代码"
    ],
    "region_name": [
        "region_name", "Region_Name", "City_Name_城市名称", "City_Name",
        "COUNTY_NAME", "County_Name", "Region_Name_地区名称"
    ],
    "year": ["Year", "year"],
    "month": ["Month", "month"],
    "date": ["Date", "date", "datetime"],
    "exposure": [
        "LLM_Exposure_Index_大语言模型暴露强度", "LLM_Exposure_Index",
        "LLM exposure", "LLM_exposure", "exposure"
    ],
    "stress": [
        "Everyday_Stress_Index_日常压力指数", "Everyday_Stress_Index",
        "Everyday Stress Index", "stress_score"
    ],
    "loneliness": [
        "Loneliness_Index_孤独感指数", "Loneliness_Index",
        "Loneliness Index", "loneliness_score"
    ],
    "anxiety": [
        "Anxiety_Index_焦虑表达指数", "Anxiety_Index",
        "Anxiety Index", "anxiety_score"
    ],
    "depression": [
        "Depressive_Symptom_Index_抑郁表达指数",
        "Depressive_Symptom_Index", "Depressive Symptom Index",
        "depression_score"
    ],
    "severe": [
        "Severe_Mental_Distress_Index_严重心理危机指数",
        "Severe_Mental_Distress_Index", "Severe Mental Distress Index",
        "severe_distress_score"
    ],
    "public_distress": [
        "Public_Distress_公开心理困扰表达", "Public_Distress",
        "public_distress_score"
    ],
    "latent_distress": [
        "Latent_Distress_潜在心理困扰", "Latent_Distress",
        "latent_distress_score"
    ],
}

OUTCOME_KEYS = ["stress", "loneliness", "anxiety", "depression", "severe"]

def find_col(df: pd.DataFrame, key: str, required: bool = True):
    for c in ALIASES.get(key, [key]):
        if c in df.columns:
            return c
    if required:
        raise KeyError(f"Required field '{key}' not found. Available columns: {list(df.columns)[:30]}")
    return None

def read_first_sheet(path: Path) -> pd.DataFrame:
    xl = pd.ExcelFile(path)
    return pd.read_excel(path, sheet_name=xl.sheet_names[0])

def canonicalize_panel(df: pd.DataFrame) -> pd.DataFrame:
    rename = {}
    for k in ["region", "region_name", "year", "month", "date", "exposure",
              "stress", "loneliness", "anxiety", "depression", "severe",
              "public_distress", "latent_distress"]:
        c = find_col(df, k, required=(k not in ["region_name", "date", "public_distress", "latent_distress"]))
        if c is not None:
            rename[c] = k
    out = df.rename(columns=rename).copy()

    if "month" not in out.columns:
        raise ValueError("Monthly analysis requires an explicit Month field. Annual data cannot reproduce the DID/event-study.")
    if "date" not in out.columns:
        out["date"] = pd.to_datetime(dict(year=out["year"], month=out["month"], day=1))
    else:
        out["date"] = pd.to_datetime(out["date"])

    out["region"] = out["region"].astype(str)
    for c in ["year", "month", "exposure"] + OUTCOME_KEYS:
        out[c] = pd.to_numeric(out[c], errors="coerce")
    for c in ["public_distress", "latent_distress"]:
        if c in out:
            out[c] = pd.to_numeric(out[c], errors="coerce")
    return out

def standardize_within_country(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for c in OUTCOME_KEYS:
        mu = out[c].mean()
        sd = out[c].std(ddof=0)
        out[c + "_z"] = (out[c] - mu) / sd
    out["composite"] = out[[c + "_z" for c in OUTCOME_KEYS]].mean(axis=1)
    for c in ["public_distress", "latent_distress"]:
        if c in out:
            sd = out[c].std(ddof=0)
            out[c + "_z"] = (out[c] - out[c].mean()) / sd
    return out

def prepare_country_panel(df: pd.DataFrame, event_date: str):
    out = canonicalize_panel(df)
    out = standardize_within_country(out)
    event = pd.Timestamp(event_date)

    pre = out.loc[out["date"] < event]
    region_pre = pre.groupby("region")["exposure"].mean()
    cutoff = float(region_pre.median())
    high_map = (region_pre >= cutoff).astype(int)

    out["high"] = out["region"].map(high_map)
    out["post"] = (out["date"] >= event).astype(int)
    out["did"] = out["high"] * out["post"]
    out["calendar_month"] = out["date"].dt.to_period("M").astype(str)

    event_period = event.to_period("M")
    p = out["date"].dt.to_period("M")
    out["event_time"] = (p.dt.year - event_period.year) * 12 + (p.dt.month - event_period.month)
    return out.dropna(subset=["high"]), cutoff

def two_way_demean(v, groups_a, groups_b):
    s = pd.Series(np.asarray(v, dtype=float))
    ga = pd.Series(groups_a).reset_index(drop=True)
    gb = pd.Series(groups_b).reset_index(drop=True)
    return (s - s.groupby(ga).transform("mean")
              - s.groupby(gb).transform("mean")
              + s.mean()).to_numpy()

def twfe_single_regressor(df, y_col, x_col="did", cluster_col="region"):
    d = df[[y_col, x_col, "region", "calendar_month", cluster_col]].dropna().copy()
    y = two_way_demean(d[y_col], d["region"], d["calendar_month"])
    x = two_way_demean(d[x_col], d["region"], d["calendar_month"])
    xx = float(np.dot(x, x))
    if xx <= 0:
        raise ValueError("No within variation in the DID regressor.")
    beta = float(np.dot(x, y) / xx)
    resid = y - beta * x

    clusters = d[cluster_col].astype(str).to_numpy()
    unique = np.unique(clusters)
    meat = 0.0
    for g in unique:
        ix = clusters == g
        meat += float(np.dot(x[ix], resid[ix])) ** 2

    n = len(d)
    G = len(unique)
    k = 1
    correction = (G / (G - 1)) * ((n - 1) / (n - k)) if G > 1 else 1.0
    var = correction * meat / (xx ** 2)
    se = float(np.sqrt(var))
    z = beta / se
    p = float(2 * stats.norm.sf(abs(z)))
    return {
        "beta": beta, "se": se,
        "ci_low": beta - 1.96 * se,
        "ci_high": beta + 1.96 * se,
        "p": p, "N": n, "regions": G,
    }

def cluster_covariance(X, resid, clusters):
    X = np.asarray(X, float)
    resid = np.asarray(resid, float)
    clusters = np.asarray(clusters).astype(str)
    XtX_inv = np.linalg.pinv(X.T @ X)
    meat = np.zeros((X.shape[1], X.shape[1]))
    uniq = np.unique(clusters)
    for g in uniq:
        ix = clusters == g
        score = X[ix].T @ resid[ix]
        meat += np.outer(score, score)
    n, k = X.shape
    G = len(uniq)
    correction = (G/(G-1))*((n-1)/(n-k)) if (G > 1 and n > k) else 1.0
    return correction * XtX_inv @ meat @ XtX_inv

def bh_fdr(pvalues):
    p = np.asarray(pvalues, float)
    n = len(p)
    order = np.argsort(p)
    ranked = p[order]
    q = ranked * n / np.arange(1, n + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    q = np.clip(q, 0, 1)
    out = np.empty_like(q)
    out[order] = q
    return out

def ensure_dirs(*paths):
    for p in paths:
        Path(p).mkdir(parents=True, exist_ok=True)
