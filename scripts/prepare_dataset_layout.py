import argparse
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("--root", required=True)
args = p.parse_args()

base = Path(args.root)
for cohort in ["BraTS2021", "UCSF-PDGM", "UPenn-GBM"]:
    for sub in ["raw", "processed", "manifests", "logs"]:
        (base / cohort / sub).mkdir(parents=True, exist_ok=True)

print("Created:", base)
print("Keep raw MRI archives outside the Git repository.")
