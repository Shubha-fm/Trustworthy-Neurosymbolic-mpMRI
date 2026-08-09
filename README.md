# Trustworthy Neurosymbolic Fusion for Multi-Parametric Brain MRI

Reproducibility-oriented code package for the manuscript:

**Trustworthy Neurosymbolic Fusion for Multi-Parametric Brain MRI with Formal Verification and Calibrated Uncertainty**

## Important data note

This repository **does not redistribute raw MRI scans or protected dataset files**.  
The study uses public research datasets whose access is governed by their original providers:

- BraTS 2021
- UCSF-PDGM
- UPenn-GBM

Place locally downloaded data under the paths described in `data/README.md`, then create subject manifests using the provided templates/scripts.


## Dataset acquisition

Dataset source and setup files are included in:

- `data/DATASET_ACCESS.md`
- `data/DATASET_CARD.md`
- `data/dataset_access_catalog.csv`
- `data/manifests/`

A 100-row synthetic dataset is included at
`data/synthetic_demo/derived_dataset.csv` for testing the label pipeline.

The raw BraTS 2021, UCSF-PDGM, and UPenn-GBM MRI archives are **not**
re-uploaded because they must remain under the original providers' access
and redistribution terms.


## What is included

- derived five-class label construction;
- four-sequence subject manifest format;
- preprocessing pipeline scaffold;
- four-branch 3D encoder + fusion-head implementation;
- imaging-informed symbolic-prior regularisation hooks;
- training/evaluation pipeline;
- split conformal prediction;
- latent-bound representation and SMT/Z3 fusion-head verification;
- verification-aware repair scaffold;
- TLA+ release-workflow specification and TLC configuration;
- reported aggregate results from the manuscript;
- tests using synthetic data only.

## Derived task

The five experimental imaging categories are:

1. background-dominant / negligible lesion;
2. NCR/NET;
3. oedema;
4. enhancing tumour;
5. enhancement-dominant.

The enhancement-dominant operating point is:

- `r_ET >= 0.35` OR
- `rho_ET >= 1.25`

with negligible lesion threshold `V_min = 1.0 ml`.

These are **experimental benchmark rules, not clinical thresholds**.

## Environment

Python 3.10+ is recommended.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Optional external tools:

- Z3 (installed through `z3-solver`)
- TLC / TLA+ tools for checking `tla/CertFusion.tla`

## Quick synthetic smoke test

```bash
python scripts/make_synthetic_demo.py
python scripts/build_labels.py \
  --input data/synthetic_demo/volumes.csv \
  --output data/synthetic_demo/labels.csv

pytest -q
```

## Real-data workflow

1. Obtain each dataset from its official repository under its applicable terms.
2. Build a manifest with paths to T1, T1ce/T1-Gd, T2, FLAIR, and tumour masks.
3. Run preprocessing.
4. Construct derived labels from compartment masks.
5. Train the multimodal model.
6. Fit conformal calibration using the calibration subset only.
7. Generate latent bounds for the selected perturbation radius.
8. Verify selected fusion-head properties with Z3.
9. Run TLC on the release-workflow model.
10. Aggregate prediction, calibration, verification, and runtime metrics.

Example commands are documented in `docs/REPRODUCTION.md`.

## Reproducibility boundary

This ZIP contains a faithful implementation scaffold of the method described in the manuscript plus the manuscript-reported aggregate results. It does **not** contain the original MRI data, trained weights, private experiment logs, or any unprovided subject-level predictions. Those artifacts must be generated from legitimately obtained datasets.

## Citation

If this repository is archived for the paper, replace the placeholder citation below with the final article/DOI.

```text
Chakraborty S, Karmakar R. Trustworthy Neurosymbolic Fusion for
Multi-Parametric Brain MRI with Formal Verification and Calibrated Uncertainty.
Artificial Intelligence in Medicine. (submitted)
```
