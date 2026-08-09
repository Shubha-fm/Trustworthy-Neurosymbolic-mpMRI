# Dataset access

The raw clinical MRI archives are intentionally **not re-uploaded into this GitHub repository**.

## BraTS 2021

- Synapse challenge archive:
  https://www.synapse.org/Synapse:syn25829067
- TCIA BraTS 2021 analysis-result page:
  https://www.cancerimagingarchive.net/analysis-result/rsna-asnr-miccai-brats-2021/

The original BraTS 2021 Synapse challenge page is archived. Obtain the data only
through an authorized current BraTS/TCIA source and follow the applicable terms.

## UCSF-PDGM

Official TCIA collection:

https://www.cancerimagingarchive.net/collection/ucsf-pdgm/

Dataset DOI:

https://doi.org/10.7937/tcia.bdgf-8v37

## UPenn-GBM

Official TCIA collection:

https://www.cancerimagingarchive.net/collection/upenn-gbm/

## Local setup

After downloading each dataset from its provider:

```bash
python scripts/prepare_dataset_layout.py --root /path/to/local/datasets
```

Populate the manifests in `data/manifests/` and validate them:

```bash
python scripts/validate_manifests.py --manifest data/manifests/brats2021.csv
python scripts/validate_manifests.py --manifest data/manifests/ucsf_pdgm.csv
python scripts/validate_manifests.py --manifest data/manifests/upenn_gbm.csv
```

Use `--check-files` when the manifest paths have been populated.
