import math
from scipy.stats import norm


def bs_euroCall_fwdInput(forward, strike, maturity, vol, interestRate):
    volSqrtT = vol * math.sqrt(maturity)
    if volSqrtT <= 0:
        volSqrtT = 0.0001
    logMoneyness = math.log(forward/strike)
    d1 = (logMoneyness + vol*vol * maturity/2)/volSqrtT
    d2 = d1 - volSqrtT
    nd1 = norm.cdf(d1)
    nd2 = norm.cdf(d2)
    price = (forward*nd1 - strike * nd2) * math.exp(-interestRate * maturity)
    print(price)

bs_euroCall_fwdInput(1931.32, 1950, 0.542, 0.2081, 0)

def bs_euroPut_fwdInput(forward, strike, maturity, vol, interestRate):
    volSqrtT = vol * math.sqrt(maturity)
    if volSqrtT <= 0:
        volSqrtT = 0.0001
    logMoneyness = math.log(forward/strike)
    d1 = (logMoneyness + vol*vol * maturity/2)/volSqrtT
    d2 = d1 - volSqrtT
    nd1 = norm.cdf(-d1)
    nd2 = norm.cdf(-d2)
    price = (-forward * nd1 + strike * nd2) * math.exp(-interestRate * maturity)
    print(price)

bs_euroPut_fwdInput(1950, 1931, 0.542, 0.2081, 0)