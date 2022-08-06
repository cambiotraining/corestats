import pandas as pd
from plotnine import *
import statsmodels.formula.api as smf
import patchworklib as pw
from plotnine.data import *
from typing import Type
import statsmodels

def dgplots(results: Type[statsmodels.regression.linear_model.RegressionResultsWrapper]) -> None:
    if isinstance(results, statsmodels.regression.linear_model.RegressionResultsWrapper) is False:
        raise TypeError("I need a model fit")
    else:
        residuals = results.resid.rename("residuals")
        fitted_values = results.fittedvalues.rename("fitted_values")
        std_resid = pd.Series(results.resid_pearson).rename("std_resid")
        influence = results.get_influence()
        cooks_d = pd.Series(influence.cooks_distance[0]).rename("cooks_d")
        leverage = pd.Series(influence.hat_matrix_diag).rename("leverage")
        obs = pd.Series(range(len(residuals))).rename("obs")
        n_obs = len(obs.index)
        
        # combine Series into DataFrame
        model_values = residuals.to_frame().join(fitted_values).join(std_resid).join(cooks_d).join(leverage).join(obs)
        # add the total number of observations
        model_values["n_obs"] = n_obs
        
        p1 = (
        ggplot(model_values, aes(x = "fitted_values", y = "residuals"))
        + geom_point()
        + geom_smooth(se = False, colour = "red")
        )

        p2 = (
        ggplot(model_values, aes(sample = "residuals"))
        + stat_qq()
        + stat_qq_line(colour = "blue")
        )

        p3 = (
        ggplot(model_values, aes(x = "fitted_values", y = "std_resid"))
        + geom_point()
        + geom_smooth(se = False, colour = "red")
        )

        p4 = (
        ggplot(model_values, aes(x = "obs", y = "cooks_d"))
        + geom_point()
        + geom_segment(aes(xend = "obs", yend = 0), colour = "blue")
        + geom_hline(aes(yintercept = 0))
        + geom_hline(aes(yintercept = 4/n_obs), colour = "blue", linetype = "dashed")
        )

        p1 = pw.load_ggplot(p1, figsize=(3,2))
        p2 = pw.load_ggplot(p2, figsize=(3,2))
        p3 = pw.load_ggplot(p3, figsize=(3,2))
        p4 = pw.load_ggplot(p4, figsize=(3,2))

        dplots = (p1 | p2) / (p3 | p4)
        return dplots
