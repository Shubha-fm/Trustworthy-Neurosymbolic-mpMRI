import numpy as np

def fit_threshold(probs, y, alpha=0.10):
    """
    Split conformal threshold using scores s_i = 1 - p(y_i | x_i).
    """
    probs = np.asarray(probs, dtype=float)
    y = np.asarray(y, dtype=int)
    n = len(y)
    scores = 1.0 - probs[np.arange(n), y]
    q_level = min(1.0, np.ceil((n + 1) * (1 - alpha)) / n)
    return float(np.quantile(scores, q_level, method="higher"))

def prediction_sets(probs, qhat):
    probs = np.asarray(probs, dtype=float)
    return [np.flatnonzero(1.0 - row <= qhat).tolist() for row in probs]

def empirical_coverage(sets, y):
    y = np.asarray(y, dtype=int)
    return float(np.mean([int(t in s) for t, s in zip(y, sets)]))
