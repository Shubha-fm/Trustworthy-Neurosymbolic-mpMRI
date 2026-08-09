from pathlib import Path
import csv, random
from src.data.labels import derive_label

out_vol = Path("data/synthetic_demo/volumes.csv")
out_lbl = Path("data/synthetic_demo/derived_dataset.csv")
out_vol.parent.mkdir(parents=True, exist_ok=True)
random.seed(42)

rows = []
for i in range(100):
    if i < 15:
        v_et, v_ncr, v_ed = 0.05, 0.10, 0.20
    elif i < 35:
        v_et = random.uniform(8, 24)
        v_ncr = random.uniform(0.5, 8)
        v_ed = random.uniform(2, 15)
    else:
        v_et = random.uniform(0, 20)
        v_ncr = random.uniform(0, 25)
        v_ed = random.uniform(0, 35)
    label = derive_label(v_et, v_ncr, v_ed)
    rows.append([f"SYN_{i:03d}", round(v_et,3), round(v_ncr,3), round(v_ed,3), label])

with out_vol.open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["subject_id","V_ET","V_NCR","V_ED"])
    for r in rows:
        w.writerow(r[:4])

with out_lbl.open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["subject_id","V_ET","V_NCR","V_ED","derived_label"])
    w.writerows(rows)

print(out_vol)
print(out_lbl)
