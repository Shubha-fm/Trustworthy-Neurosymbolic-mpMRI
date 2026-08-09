import pandas as pd

df = pd.read_csv("results/reported/solver_log.csv")
for _, r in df.iterrows():
    assert r["UNSAT"] + r["SAT"] + r["Timeout"] == r["Queries"]
    assert r["False_alarms"] + r["Genuine_violations"] == r["SAT"]
print("Reported solver-log arithmetic is internally consistent.")
