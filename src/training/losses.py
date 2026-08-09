import torch.nn.functional as F
from .priors import prior_satisfaction

def neurosymbolic_loss(logits, targets, predicates, lam=0.1):
    ce = F.cross_entropy(logits, targets)
    probs = logits.softmax(dim=1)
    sat = prior_satisfaction(predicates, probs)
    return ce + lam*(1.0 - sat), {"ce": float(ce.detach()), "rule_sat": float(sat.detach())}
