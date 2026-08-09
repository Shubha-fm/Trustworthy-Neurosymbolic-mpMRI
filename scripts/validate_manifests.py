import argparse
from pathlib import Path
import pandas as pd

REQUIRED = ["subject_id","t1","t1ce","t2","flair","segmentation","cohort","split"]

p = argparse.ArgumentParser()
p.add_argument("--manifest", required=True)
p.add_argument("--check-files", action="store_true")
args = p.parse_args()

df = pd.read_csv(args.manifest)
missing = [c for c in REQUIRED if c not in df.columns]
if missing:
    raise SystemExit(f"Missing required columns: {missing}")

if df["subject_id"].duplicated().any():
    raise SystemExit("Duplicate subject IDs detected.")

if args.check_files:
    failures = []
    for row in df.itertuples():
        for col in ["t1","t1ce","t2","flair","segmentation"]:
            value = getattr(row, col)
            if pd.isna(value) or not Path(str(value)).exists():
                failures.append((row.subject_id, col, value))
    if failures:
        for item in failures[:50]:
            print("Missing:", item)
        raise SystemExit(f"{len(failures)} unresolved file paths.")

print(f"Manifest OK: {len(df)} rows")
