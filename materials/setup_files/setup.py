from plotnine import *
import pandas as pd
import numpy as np
import pingouin as pg
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
import scikit_posthocs as sp
exec(open('scripts/dgplots.py').read())
exec(open('scripts/pwr_f2_test.py').read())
theme_set(theme_bw())
