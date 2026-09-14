
## Scope

This repository contains two kinds of code:

1. **Analysis code** that re-estimates the main statistical analyses from the deposited monthly China and U.S. panels:
   - panel preparation and within-country standardization;
   - country-specific TWFE-DID;
   - dynamic event-time models;
   - joint pre-trend Wald tests;
   - temporal placebo tests;
   - dimension-specific DID estimates;
   - Benjamini-Hochberg FDR correction;
   - formal China–United States coefficient contrasts;
   - regional pre/post dominant-dimension summaries;
   - contextual B-spline models and sensitivity checks.

2. **Figure-reproduction code** that reads the deposited Figure 1–5 source-data workbooks and rebuilds the principal statistical panels.


## Expected data files

Place the following files in `data/`:

- `China_panel.xlsx`
- `US_panel.xlsx`
- `Figure1_source.xlsx`
- `Figure2_source.xlsx`
- `Figure3_source.xlsx`
- `Figure4_China_source.xlsx`
- `Figure5_US_source.xlsx`

The scripts accept the bilingual column names used in the deposited workbooks.

### Main monthly panel requirements

China:
- city code
- year
- month
- monthly LLM exposure
- everyday stress
- loneliness
- anxiety
- depressive symptoms
- severe mental distress
- public distress
- latent distress

United States:
- county FIPS
- year
- month
- the same psychological and exposure fields

## Country-specific event dates

- United States: November 2022
- China: March 2023

High exposure is defined within each country as pre-entry mean regional LLM exposure at or above the country-specific median.

## Main model

For each country:

`Y_it = region FE + calendar-month FE + beta*(High_i × Post_t) + error_it`

Standard errors are clustered at the region level.

## Reproduction workflow

From the repository root:

```bash
python code/02_main_analysis/01_prepare_panels.py
python code/02_main_analysis/02_twfe_did.py
python code/02_main_analysis/03_event_study_pretrend.py
python code/02_main_analysis/04_temporal_placebo.py
python code/03_dimension_analysis/01_dimension_did_fdr.py
python code/03_dimension_analysis/02_dominant_dimension.py
python code/05_context/01_context_bspline.py
python code/05_context/02_bspline_sensitivity.py
python code/06_figures/figure1.py
python code/06_figures/figure2.py
python code/06_figures/figure3.py
python code/06_figures/figure4.py
python code/06_figures/figure5.py
```

Or:

```bash
python run_all.py
```

## Important distinction: Figure 1c and formal pre-trend test

Figure 1c in the deposited source-data workbook contains monthly high-minus-low exposure contrasts and therefore retains a non-zero estimate at event month 0.

The **formal joint pre-trend test** is estimated separately using a canonical dynamic TWFE specification with event month `k = -1` omitted for regression identification. The event date itself remains `k = 0`.

## Placebo design

Pseudo-entry dates are shifted 6, 12 and 18 months earlier than the true country-specific entry date. Placebo estimation uses only observations preceding the true entry date, preventing contamination by the actual LLM diffusion period.

## Contextual heterogeneity

The main contextual models use cubic B-splines with df = 5 and HC3 heteroskedasticity-robust confidence intervals. Sensitivity analyses use df = 4, df = 6 and df = 5 after trimming observations below the 2.5th and above the 97.5th percentile of the moderator.

## Data availability

Data supporting the analyses are available via Figshare:
https://doi.org/10.6084/m9.figshare.33465139

## Software

Python 3.10+ is recommended.

Install dependencies:

```bash
pip install -r requirements.txt
```


