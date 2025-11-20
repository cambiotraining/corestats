"""
Diagnostic plotting utilities for statsmodels linear models.

This module provides a robust implementation of regression diagnostic
plots using plotnine and a Matplotlib composite. LOESS smoothing is
used when possible, but if plotnine's LOESS fails due to singularities
(very common with categorical predictors or few unique fitted values),
the affected plot is automatically rebuilt using method='lm'. Titles,
themes, axis labels, and all styling are preserved because each plot is
regenerated from scratch rather than mutated.

The composite figure is encoded as base64 PNG and returned as an HTML
object, ensuring correct rendering in Jupyter, Quarto, RStudio via
reticulate, VSCode, and terminal-based `quarto render`, without
requiring GUI backends or file I/O.
"""

__version__ = "1.1.0"


# ======================================================================
# Rendering with LOESS → LM fallback (clean rebuild architecture)
# ======================================================================

def _render_plotnine(p, build_func):
    """
    Render a plotnine plot safely into a numpy array.

    Parameters
    ----------
    p : plotnine.ggplot
        The initial LOESS-based plot to attempt rendering.

    build_func : callable
        A function that rebuilds the same plot with method="lm" when
        LOESS fails. Signature must be build_func(method="loess"|"lm").

    Returns
    -------
    numpy.ndarray
        Image of the rendered plot.
    """
    import matplotlib.pyplot as plt
    from io import BytesIO

    def try_draw(plot):
        """Internal helper that draws a plotnine plot to a PNG array."""
        fig = plot.draw()
        buf = BytesIO()
        fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
        buf.seek(0)
        img = plt.imread(buf)
        buf.close()
        plt.close(fig)
        return img

    # Attempt LOESS version
    try:
        return try_draw(p)

    except Exception:
        print("⚠ LOESS failed — rebuilding plot with linear smoothing (method='lm').")
        p_lm = build_func(method="lm")
        return try_draw(p_lm)



# ======================================================================
# Main dgplots() function
# ======================================================================

def dgplots(results):
    """
    Generate a 2×2 panel of diagnostic plots for a statsmodels regression fit.

    Plots produced:
      1. Residuals vs fitted values (+ smoother)
      2. Normal Q–Q plot
      3. Scale–location plot (+ smoother)
      4. Cook’s distance

    Smoothing:
      - LOESS used by default.
      - If LOESS fails (singularities), affected plots are fully rebuilt
        using method='lm' to preserve titles and themes.

    Returns
    -------
    IPython.display.HTML
        HTML object containing a responsive composite PNG.

    Examples
    --------
    >>> import statsmodels.formula.api as smf
    >>> from dgplots import dgplots
    >>> model = smf.ols("y ~ x1 + x2", data=df).fit()
    >>> dgplots(model)
    """
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from io import BytesIO
    import base64
    from IPython.display import HTML
    import statsmodels.api as sm
    from plotnine import (
        ggplot, aes, geom_point, geom_smooth, stat_qq, stat_qq_line,
        geom_segment, geom_hline, labs, theme_bw, theme, element_text
    )

    # ------------------------------------------------------------------
    # Validate input
    # ------------------------------------------------------------------
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

    # ------------------------------------------------------------------
    # Common formatting theme
    # ------------------------------------------------------------------
    diag_theme = (
        theme_bw()
        + theme(
            text=element_text(size=14),
            axis_title=element_text(size=16),
            axis_text=element_text(size=12)
        )
    )

    # ==================================================================
    # Plot builder functions
    # ==================================================================

    def build_p1(method="loess"):
        smoother = geom_smooth(method=method, se=False, colour="red", size=1.2)
        return (
            ggplot(df, aes("predicted_values", "residuals"))
            + geom_point(size=3)
            + smoother
            + labs(title="Residuals plot", x="Predicted values", y="Residuals")
            + diag_theme
        )

    def build_p2(method="loess"):
        # Q-Q plot does not use smoothing
        return (
            ggplot(df, aes(sample="residuals"))
            + stat_qq(size=3)
            + stat_qq_line(colour="blue", size=1.2)
            + labs(title="Q–Q plot", x="Theoretical quantiles", y="Sample quantiles")
            + diag_theme
        )

    def build_p3(method="loess"):
        smoother = geom_smooth(method=method, se=False, colour="red", size=1.2)
        return (
            ggplot(df, aes("predicted_values", "std_resid"))
            + geom_point(size=3)
            + smoother
            + labs(
                title="Location–Scale plot",
                x="Predicted values",
                y=u"\u221A" + "|standardised residuals|"
            )
            + diag_theme
        )

    def build_p4(method="loess"):
        # Cook's D plot has no smoothing
        return (
            ggplot(df, aes("obs", "cooks_d"))
            + geom_point(size=3)
            + geom_segment(aes(xend="obs", yend=0), colour="blue", size=0.8)
            + geom_hline(yintercept=0, size=0.8)
            + geom_hline(yintercept=4 / n_obs, colour="blue",
                          linetype="dashed", size=0.8)
            + labs(title="Influential points", x="Observation", y="Cook's D")
            + diag_theme
        )

    # ==================================================================
    # Render each panel with LOESS→LM fallback
    # ==================================================================

    imgs = [
        _render_plotnine(build_p1(), build_p1),
        _render_plotnine(build_p2(), build_p2),
        _render_plotnine(build_p3(), build_p3),
        _render_plotnine(build_p4(), build_p4)
    ]

    # ==================================================================
    # Composite 2×2 figure
    # ==================================================================
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    for ax, img in zip(axes.flatten(), imgs):
        ax.imshow(img)
        ax.axis("off")
    plt.tight_layout()

    # Convert to base64
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    buf.seek(0)
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    buf.close()
    plt.close(fig)

    # Return responsive HTML
    return HTML(f'<img style="max-width:100%; height:auto;" '
                f'src="data:image/png;base64,{b64}"/>')
