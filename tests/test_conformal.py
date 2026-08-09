import numpy as np
from src.conformal.split_conformal import fit_threshold, prediction_sets, empirical_coverage

def test_conformal_runs():
    p = np.array([[.8,.1,.1],[.1,.8,.1],[.1,.1,.8],[.6,.2,.2]])
    y = np.array([0,1,2,0])
    q = fit_threshold(p,y,alpha=.1)
    sets = prediction_sets(p,q)
    cov = empirical_coverage(sets,y)
    assert 0 <= q <= 1
    assert 0 <= cov <= 1
