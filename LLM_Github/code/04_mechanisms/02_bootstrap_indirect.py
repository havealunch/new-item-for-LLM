import numpy as np
import pandas as pd
import statsmodels.api as sm

def bootstrap_indirect(df, exposure, mediator, outcome, n_boot=5000, seed=42):
    """
    Non-parametric bootstrap for a*b indirect effect.
    Input dataframe should contain region-level observations.
    """
    d = df[[exposure, mediator, outcome]].dropna().reset_index(drop=True)
    rng = np.random.default_rng(seed)

    def estimate(x):
        a = sm.OLS(x[mediator], sm.add_constant(x[[exposure]])).fit().params[exposure]
        b = sm.OLS(x[outcome], sm.add_constant(x[[exposure, mediator]])).fit().params[mediator]
        return float(a*b)

    point = estimate(d)
    boot = np.empty(n_boot)
    n = len(d)
    for i in range(n_boot):
        ix = rng.integers(0,n,n)
        boot[i] = estimate(d.iloc[ix])
    low, high = np.quantile(boot,[0.025,0.975])
    return {"indirect":point,"ci_low":low,"ci_high":high,"sig":bool(low>0 or high<0)}
