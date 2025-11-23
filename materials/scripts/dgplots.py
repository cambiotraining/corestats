# dgplots (rewritten with stable LOWESS smoothing)
"""
Diagnostic plotting utilities for statsmodels linear models.

This version replaces plotnine's LOESS smoothing with a robust LOWESS
implementation from statsmodels, eliminating failures caused by
plotnine's geom_smooth(stat_smooth) layer.

Plots:
  1. Residuals vs fitted (+ LOWESS)
  2. Normal Q–Q
  3. Scale–location (+ LOWESS)
  4. Cook’s distance

Output:
  Composite 2×2 PNG returned as base64 HTML for universal display.
"""

__version__ = "1.2.0"

import pandas as pd
import numpy as np
import base64
from io import BytesIO
import matplotlib.pyplot as plt
from IPython.display import HTML
import statsmodels.api as sm
from statsmodels.nonparametric.smoothers_lowess import lowess

from plotnine import (
    ggplot, aes, geom_point, geom_line, stat_qq, stat_qq_line,
    geom_segment, geom_hline, labs, theme_bw, theme, element_text
)


# ======================================================================
# Utility: render a plotnine plot safely to a numpy array
# ======================================================================
def _render_plotnine(p):
    """
    Draw a plotnine plot into a numpy array (PNG) safely.

    This function does NOT try to catch LOESS failures anymore because
    LOWESS is computed externally, not inside plotnine.
    """
    def _draw(plot):
        fig = plot.draw()
        buf = BytesIO()
        fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
        buf.seek(0)
        img = plt.imread(buf)
        buf.close()
        plt.close(fig)
        return img

    return _draw(p)


# ======================================================================
# Utility: LOWESS smoother using statsmodels
# ======================================================================
def _lowess_df(df, x, y, frac=0.75):
    """
    Compute LOWESS smoothing with parameters comparable to
    plotnine/ggplot2's LOESS defaults (span = 0.75).
    """
    smoothed = lowess(
        endog=df[y],
        exog=df[x],
        frac=frac,   # match ggplot2 default span
        it=0,        # no robustness iterations (ggplot also uses none)
        return_sorted=True
    )

    return pd.DataFrame({
        x: smoothed[:, 0],
        f"{y}_smooth": smoothed[:, 1],
    })



# ======================================================================
# Main function
# ======================================================================
def dgplots(results):
    """
    Generate a 2×2 diagnostic panel for a statsmodels regression object.
    LOWESS smoothing is provided by statsmodels.lowess and is extremely
    stable (no LOESS failures).

    Returns
    -------
    IPython.display.HTML
    """

    if not isinstance(results, sm.regression.linear_model.RegressionResultsWrapper):
        raise TypeError("Please provide a statsmodels regression fit.")

    infl = results.get_influence()

    df = pd.DataFrame({
        "residuals": results.resid,
        "predicted_values": results.fittedvalues,
        "std_resid": np.sqrt(np.abs(infl.resid_studentized_internal)),
        "cooks_d": infl.cooks_distance[0],
        "leverage": infl.hat_matrix_diag,
        "obs": np.arange(len(results.resid)),
    })

    n_obs = len(df)

    # Common theme
    diag_theme = (
        theme_bw()
        + theme(
            text=element_text(size=14),
            axis_title=element_text(size=16),
            axis_text=element_text(size=12)
        )
    )

    # ==================================================================
    # P1: Residuals vs Fitted with LOWESS
    # ==================================================================
    def build_p1():
        df_lo = _lowess_df(df, "predicted_values", "residuals")

        return (
            ggplot(df, aes("predicted_values", "residuals"))
            + geom_point(size=3)
            + geom_hline(yintercept=0, size=0.8, colour="blue")
            + geom_line(
                df_lo,
                aes("predicted_values", "residuals_smooth"),
                color="red",
                size=1.2
            )
            + labs(title="Residuals plot",
                   x="Predicted values",
                   y="Residuals")
            + diag_theme
        )

    # ==================================================================
    # P2: Normal Q–Q (no smoothing)
    # ==================================================================
    def build_p2():
        return (
            ggplot(df, aes(sample="residuals"))
            + stat_qq(size=3)
            + stat_qq_line(color="blue", size=1.2)
            + labs(title="Q–Q plot",
                   x="Theoretical quantiles",
                   y="Sample quantiles")
            + diag_theme
        )

    # ==================================================================
    # P3: Scale–Location with LOWESS
    # ==================================================================
    def build_p3():
        df_lo = _lowess_df(df, "predicted_values", "std_resid")

        return (
            ggplot(df, aes("predicted_values", "std_resid"))
            + geom_point(size=3)
            + geom_line(
                df_lo,
                aes("predicted_values", "std_resid_smooth"),
                color="red",
                size=1.2
            )
            + labs(title="Location–Scale plot",
                   x="Predicted values",
                   y=u"\u221A|standardised residuals|")
            + diag_theme
        )

    # ==================================================================
    # P4: Cook’s distance
    # ==================================================================
    def build_p4():
        return (
            ggplot(df, aes("obs", "cooks_d"))
            + geom_point(size=3)
            + geom_segment(aes(xend="obs", yend=0),
                           color="blue", size=0.8)
            + geom_hline(yintercept=0, size=0.8)
            + geom_hline(yintercept=4 / n_obs,
                         color="blue", linetype="dashed", size=0.8)
            + labs(title="Influential points",
                   x="Observation",
                   y="Cook's D")
            + diag_theme
        )

    # ==================================================================
    # Render all plots
    # ==================================================================
    imgs = [
        _render_plotnine(build_p1()),
        _render_plotnine(build_p2()),
        _render_plotnine(build_p3()),
        _render_plotnine(build_p4())
    ]

    # Composite 2×2 figure
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    for ax, img in zip(axes.flatten(), imgs):
        ax.imshow(img)
        ax.axis("off")
    plt.tight_layout()

    # Convert composite to base64 HTML
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    buf.seek(0)
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    buf.close()
    
    plt.close(fig)

    return HTML(f'<img style="max-width:100%; height:auto;" '
                f'src="data:image/png;base64,{b64}"/>')
