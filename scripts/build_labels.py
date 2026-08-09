import argparse, pandas as pd
from src.data.labels import derive_label

p = argparse.ArgumentParser()
p.add_argument("--input", required=True)
p.add_argument("--output", required=True)
args = p.parse_args()

df = pd.read_csv(args.input)
df["derived_label"] = [
    derive_label(r.V_ET, r.V_NCR, r.V_ED) for r in df.itertuples()
]
df.to_csv(args.output, index=False)
print(args.output)
