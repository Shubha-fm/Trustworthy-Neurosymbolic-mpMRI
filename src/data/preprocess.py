from pathlib import Path
import numpy as np
import nibabel as nib

def load_nifti(path):
    img = nib.load(str(path))
    return np.asarray(img.get_fdata(), dtype=np.float32), img.affine, img.header

def zscore_in_mask(volume, mask, eps=1e-6):
    vals = volume[mask > 0]
    if vals.size == 0:
        raise ValueError("Brain mask is empty.")
    mu = float(vals.mean())
    sigma = float(vals.std())
    out = volume.copy()
    out[mask > 0] = (vals - mu) / (sigma + eps)
    return out

def center_crop_or_pad(arr, target=(128,128,128)):
    out = np.zeros(target, dtype=arr.dtype)
    src_slices, dst_slices = [], []
    for s, t in zip(arr.shape, target):
        if s >= t:
            a = (s - t)//2
            src_slices.append(slice(a, a+t))
            dst_slices.append(slice(0,t))
        else:
            a = (t - s)//2
            src_slices.append(slice(0,s))
            dst_slices.append(slice(a,a+s))
    out[tuple(dst_slices)] = arr[tuple(src_slices)]
    return out
