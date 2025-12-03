# Corrected and simplified version of pwr_f2_test
# Matches R's pwr.f2.test()

from numpy import ceil
from scipy.stats import f, ncf
from scipy.optimize import brenth

def _power_f2(u, v, f2, sig_level):
    """
    Internal function returning power for given parameters.
    Mirrors R's pwr.f2.test().
    """
    # Critical F value
    Fcrit = f.isf(sig_level, u, v)

    # Noncentrality parameter
    ncp = f2 * (u + v + 1)

    # Power = 1 - CDF of noncentral F at the critical value
    return 1 - ncf.cdf(Fcrit, u, v, ncp)


def pwr_f2_test(u=None, v=None, f2=None, sig_level=None, power=None):
    """
    One of u, v, f2, sig_level, power must be None.
    Computes the missing value.

    Arguments:
        u : numerator degrees of freedom
        v : denominator degrees of freedom
        f2 : Cohen's f^2
        sig_level : significance level (alpha)
        power : test power
    """

    # Ensure exactly one parameter is missing
    params = [u, v, f2, sig_level, power]
    if sum(p is None for p in params) != 1:
        raise ValueError("Exactly one parameter must be None.")

    # Solve for missing parameter if necessary
    if power is None:
        power = _power_f2(u, v, f2, sig_level)

    elif f2 is None:
        def fn(f2_candidate):
            return _power_f2(u, v, f2_candidate, sig_level) - power
        f2 = brenth(fn, 1e-9, 1e3)

    elif u is None:
        def fn(u_candidate):
            return _power_f2(u_candidate, v, f2, sig_level) - power
        u = brenth(fn, 1+1e-9, 200)

    elif v is None:
        def fn(v_candidate):
            return _power_f2(u, v_candidate, f2, sig_level) - power
        v = brenth(fn, 1+1e-9, 1e6)

    elif sig_level is None:
        def fn(sig_candidate):
            return _power_f2(u, v, f2, sig_candidate) - power
        sig_level = brenth(fn, 1e-10, 0.5)

    # Report results exactly like your previous function
    print("Power analysis results:")
    print(f" u is: {u}")
    print(f" v is: {v}")
    print(f" f2 is: {f2}")
    print(f" sig_level is: {sig_level}")
    print(f" power is: {power}")
    print(f" num_obs is: {int(ceil(u)) + int(ceil(v)) + 1}")
