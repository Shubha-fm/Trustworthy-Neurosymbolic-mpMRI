# Dataset layout

Raw imaging data are intentionally not included.

Create one CSV manifest per cohort with columns:

`subject_id,t1,t1ce,t2,flair,segmentation,cohort,split`

For UPenn-GBM, the post-contrast T1-Gd path should be placed in the `t1ce` column so the model receives a common post-contrast slot.

Example:

```csv
subject_id,t1,t1ce,t2,flair,segmentation,cohort,split
BraTS_00001,/data/.../t1.nii.gz,/data/.../t1ce.nii.gz,/data/.../t2.nii.gz,/data/.../flair.nii.gz,/data/.../seg.nii.gz,BraTS2021,train
```

The label-construction code expects compartment volumes (ml) for:
- enhancing tumour (`V_ET`);
- NCR/NET (`V_NCR`);
- oedema (`V_ED`).

If using voxel masks directly, compute the volume using voxel spacing before calling `src/data/labels.py`.
