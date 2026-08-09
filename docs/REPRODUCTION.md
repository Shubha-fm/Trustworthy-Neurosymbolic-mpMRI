# Reproduction workflow

## 1. Obtain datasets

Download BraTS 2021, UCSF-PDGM, and UPenn-GBM from their official repositories under the providers' access conditions. Do not commit raw NIfTI files to GitHub.

## 2. Build manifests

Populate:
- `data/manifests/brats2021.csv`
- `data/manifests/ucsf_pdgm.csv`
- `data/manifests/upenn_gbm.csv`

All four sequences must be available for the current architecture.

## 3. Preprocess

The manuscript preprocessing consists of:
- sequence alignment;
- resampling to 128 x 128 x 128;
- brain-mask z-score normalization;
- crop/pad to a fixed field of view;
- consistent four-sequence augmentation during training.

The included Python module gives the normalization and crop/pad primitives. Registration/resampling should use the same toolchain selected for the real experiment and should be recorded in an environment lockfile before archival.

## 4. Derived labels

Use `src/data/labels.py`.

Definitions:
- `V_lesion = V_ET + V_NCR + V_ED`
- background-dominant if `V_lesion < 1.0 ml`
- enhancement-dominant if `V_ET/(V_lesion+1e-6) >= 0.35`
  or `V_ET/(V_NCR+1e-6) >= 1.25`
- otherwise choose the largest of ET, NCR/NET, oedema;
  ties: ET > NCR/NET > oedema.

## 5. Model

Four modality-specific 3D encoders produce 512-dimensional vectors.
The concatenated 2048-dimensional representation is passed to:

`2048 -> 512 -> 128 -> 5`

with ReLU hidden activations.

## 6. Neurosymbolic regularization

Training objective:

`L = L_CE + lambda * (1 - mean_p val(phi_p))`

for seven training-time soft priors. The eighth, conformal-set-related template is post-hoc only.

## 7. Conformal prediction

Fit split-conformal scores on the calibration subset only:

`s_i = 1 - p(y_i|x_i)`

and construct:

`C(x) = {y : 1 - p(y|x) <= qhat}`

with alpha = 0.10.

## 8. Verification

The full voxel-level encoders are not encoded directly into SMT.
Generate **sound** encoder-output abstractions, then encode the fusion head exactly.

Selected operating point:
- epsilon = 0.031
- timeout = 60 s / property

UNSAT => verified over the encoded abstraction  
SAT => candidate counterexample requiring reachability review  
TIMEOUT => no verified status

## 9. TLA+

Run TLC against:
- `tla/CertFusion.tla`
- `tla/CertFusion.cfg`

Run the negative control against:
- `tla/CertFusion_Mutant.tla`
- `tla/CertFusion_Mutant.cfg`

## 10. Aggregate results

`results/reported/` contains only aggregate numbers stated in the manuscript.
It is not a substitute for subject-level logs.
