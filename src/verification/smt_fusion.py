from dataclasses import dataclass
from enum import Enum
import time
import numpy as np
import z3

class Verdict(str, Enum):
    VERIFIED = "VERIFIED"
    VIOLATED = "VIOLATED"
    FALSE_ALARM = "FALSE_ALARM"
    TIMEOUT = "TIMEOUT"

@dataclass
class VerificationResult:
    verdict: Verdict
    seconds: float
    model: dict | None = None

def _relu(solver, x, name):
    y = z3.Real(name)
    solver.add(y == z3.If(x >= 0, x, 0))
    return y

def encode_mlp(weights, biases, lower, upper, timeout_s=60):
    """
    Exact SMT encoding of a ReLU MLP given input bounds.
    weights/biases: list of numpy arrays, last layer linear.
    """
    s = z3.Solver()
    s.set(timeout=int(timeout_s * 1000))
    x = [z3.Real(f"z_{i}") for i in range(len(lower))]
    for i, (lo, hi) in enumerate(zip(lower, upper)):
        s.add(x[i] >= float(lo), x[i] <= float(hi))

    h = x
    for li, (W, b) in enumerate(zip(weights, biases)):
        nxt = []
        last = li == len(weights)-1
        for j in range(W.shape[0]):
            a = z3.Real(f"a_{li}_{j}")
            expr = sum(float(W[j,k])*h[k] for k in range(W.shape[1])) + float(b[j])
            s.add(a == expr)
            nxt.append(a if last else _relu(s, a, f"h_{li}_{j}"))
        h = nxt
    return s, x, h

def verify_implication(solver, antecedent, consequent, timeout_s=60):
    """
    Verify A -> B by checking satisfiability of A & !B.
    """
    solver.push()
    solver.add(antecedent, z3.Not(consequent))
    t0 = time.time()
    r = solver.check()
    elapsed = time.time() - t0

    if r == z3.unsat:
        verdict = Verdict.VERIFIED
        model = None
    elif r == z3.sat:
        verdict = Verdict.VIOLATED
        model = {str(d): str(solver.model()[d]) for d in solver.model().decls()}
    else:
        verdict = Verdict.TIMEOUT
        model = None
    solver.pop()
    return VerificationResult(verdict, elapsed, model)
