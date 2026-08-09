from sklearn.metrics import accuracy_score, f1_score, cohen_kappa_score
import numpy as np

def expected_calibration_error(probs, y, bins=15):
    probs = np.asarray(probs)
    y = np.asarray(y)
    conf = probs.max(axis=1)
    pred = probs.argmax(axis=1)
    edges = np.linspace(0,1,bins+1)
    ece = 0.0
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (conf > lo) & (conf <= hi)
        if m.any():
            ece += m.mean() * abs((pred[m] == y[m]).mean() - conf[m].mean())
    return float(ece)

def classification_metrics(probs, y):
    pred = np.asarray(probs).argmax(axis=1)
    y = np.asarray(y)
    return {
        "accuracy": accuracy_score(y, pred),
        "macro_f1": f1_score(y, pred, average="macro"),
        "weighted_f1": f1_score(y, pred, average="weighted"),
        "kappa": cohen_kappa_score(y, pred),
        "ece": expected_calibration_error(probs, y),
    }
