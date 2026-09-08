from pathlib import Path
import subprocess, sys

ROOT=Path(__file__).resolve().parent
scripts=[
    "code/02_main_analysis/01_prepare_panels.py",
    "code/02_main_analysis/02_twfe_did.py",
    "code/02_main_analysis/03_event_study_pretrend.py",
    "code/02_main_analysis/04_temporal_placebo.py",
    "code/03_dimension_analysis/01_dimension_did_fdr.py",
    "code/03_dimension_analysis/02_dominant_dimension.py",
    "code/04_mechanisms/03_fdr_paths_from_source.py",
    "code/05_context/01_context_bspline.py",
    "code/05_context/02_bspline_sensitivity.py",
    "code/06_figures/figure1.py",
    "code/06_figures/figure2.py",
    "code/06_figures/figure3.py",
    "code/06_figures/figure4.py",
    "code/06_figures/figure5.py",
]
for s in scripts:
    print(f"\n>>> {s}")
    subprocess.run([sys.executable,str(ROOT/s)],check=True)
