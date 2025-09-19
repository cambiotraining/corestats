from typing import Type
import os
from datetime import datetime
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from plotnine import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def dgplots(results: Type[sm.regression.linear_model.RegressionResultsWrapper]) -> plt.Figure:
    if not isinstance(results, sm.regression.linear_model.RegressionResultsWrapper):
        raise TypeError("Please provide a model fit.")

    residuals = results.resid.rename("residuals")
    predicted_values = results.fittedvalues.rename("predicted_values")
    std_resid = pd.Series(np.sqrt(np.abs(results.get_influence().resid_studentized_internal))).rename("std_resid")
    influence = results.get_influence()
    cooks_d = pd.Series(influence.cooks_distance[0]).rename("cooks_d")
    leverage = pd.Series(influence.hat_matrix_diag).rename("leverage")
    obs = pd.Series(range(len(residuals))).rename("obs")
    n_obs = len(obs)

    # Combine Series into DataFrame
    model_values = (
        residuals.to_frame()
        .join(predicted_values)
        .join(std_resid)
        .join(cooks_d)
        .join(leverage)
        .join(obs)
    )
    model_values["n_obs"] = n_obs

    # Define plots
    p1 = (
        ggplot(model_values, aes(x="predicted_values", y="residuals"))
        + geom_point()
        + geom_smooth(se=False, colour="red")
        + labs(title="Residuals plot")
        + xlab("predicted values")
        + ylab("residuals")
        + theme_bw()
    )

    p2 = (
        ggplot(model_values, aes(sample="residuals"))
        + stat_qq()
        + stat_qq_line(colour="blue")
        + labs(title="Q-Q plot")
        + xlab("theoretical quantiles")
        + ylab("sample quantiles")
        + theme_bw()
    )

    p3 = (
        ggplot(model_values, aes(x="predicted_values", y="std_resid"))
        + geom_point()
        + geom_smooth(se=False, colour="red")
        + labs(title="Location-Scale plot")
        + xlab("predicted values")
        + ylab(u"\u221A" + "|standardised residuals|")
        + theme_bw()
    )

    p4 = (
        ggplot(model_values, aes(x="obs", y="cooks_d"))
        + geom_point()
        + geom_segment(aes(xend="obs", yend=0), colour="blue")
        + geom_hline(aes(yintercept=0))
        + geom_hline(aes(yintercept=4/n_obs), colour="blue", linetype="dashed")
        + labs(title="Influential points")
        + xlab("observation")
        + ylab("cook's d")
        + theme_bw()
    )

    # Save each plot to a temporary PNG
    output_dir = "images/dgplots"
    os.makedirs(output_dir, exist_ok=True)
    date = datetime.now().strftime("%Y_%m_%d-%I-%M-%S_%p")

    p1_path = os.path.join(output_dir, f"{date}_p1.png")
    p2_path = os.path.join(output_dir, f"{date}_p2.png")
    p3_path = os.path.join(output_dir, f"{date}_p3.png")
    p4_path = os.path.join(output_dir, f"{date}_p4.png")

    p1.save(p1_path, dpi=150, width=4, height=3, units="in")
    p2.save(p2_path, dpi=150, width=4, height=3, units="in")
    p3.save(p3_path, dpi=150, width=4, height=3, units="in")
    p4.save(p4_path, dpi=150, width=4, height=3, units="in")

    # Load images
    img1 = mpimg.imread(p1_path)
    img2 = mpimg.imread(p2_path)
    img3 = mpimg.imread(p3_path)
    img4 = mpimg.imread(p4_path)

    # Create 2x2 figure
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    ax_flat = axes.flatten()
    images = [img1, img2, img3, img4]

    for ax, img in zip(ax_flat, images):
        ax.imshow(img)
        ax.axis("off")  # Hide axes

    plt.tight_layout()

    return fig
