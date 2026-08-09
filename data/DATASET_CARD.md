# Dataset card

## Real cohorts used in the manuscript

| Cohort | Role | Raw MRI files included in this ZIP? |
|---|---|---|
| BraTS 2021 | Development and five-fold internal evaluation | No |
| UCSF-PDGM | External transfer evaluation | No |
| UPenn-GBM | External transfer evaluation | No |

Raw MRI files remain with the original data providers.

## Required modalities

The current architecture expects:
- T1
- T1ce / post-contrast T1 / T1-Gd mapped to the common T1ce slot
- T2
- FLAIR
- a tumour segmentation that can be mapped to ET, NCR/NET, and oedema

## Included synthetic dataset

`data/synthetic_demo/derived_dataset.csv` contains 100 synthetic records for
testing the manuscript's derived-label construction. It contains no patient data
and must not be used as experimental evidence.

## Data leakage rule

Splits must be subject-level. No crop, patch, augmented view, or derivative of a
subject may cross training, calibration, and held-out test partitions.
