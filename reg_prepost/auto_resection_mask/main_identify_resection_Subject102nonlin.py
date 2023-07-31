import nilearn.image as ni
from warp_utils import apply_warp
from aligner import Aligner
from warper import Warper
from monai.transforms import (
    LoadImage,
    Resize,
    EnsureChannelFirst,
    ScaleIntensityRangePercentiles,
)
import nibabel as nib
import os
import os.path
import numpy as np
from scipy.ndimage import gaussian_filter
from skimage.morphology import remove_small_objects, opening


BrainSuitePATH = "/home/ajoshi/BrainSuite23a"
ERR_THR = 80

nonlin_reg = Warper()


mov_img_orig = (
    "/deneb_disk/auto_resection/Ken_Post-op_MRI/sub-SUB102/sMRI/sub-SUB102-102_MRI.nii"
)
mov_img = "/deneb_disk/auto_resection/Ken_Post-op_MRI/sub-SUB102/sMRI/sub-SUB102-102_MRI.bse.nii.gz"
ref_img = (
    "/deneb_disk/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject102/T1s.bse.nii.gz"
)
ref_img_mask = (
    "/deneb_disk/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject102/T1s.mask.nii.gz"
)
ref_img_bfc = (
    "/deneb_disk/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject102/T1s.bfc.nii.gz"
)
ref_img_pvc_frac = "/deneb_disk/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject102/T1s.pvc.frac.nii.gz"
error_img = "/deneb_disk/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject102/error_pre_post.nii.gz"
error_mask_img = "/deneb_disk/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject102/error_pre_post.nonlin.mask.nii.gz"
error_init_mask_img = "/deneb_disk/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject102/error_pre_post.nonlin.init.mask.nii.gz"

error_mask_img_rigid = "/deneb_disk/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject102/error_pre_post.init.mask.nii.gz"
target_msk_file = "/deneb_disk/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject102/target.mask.nii.gz"

# rigidly warped image
rigid_reg_img = (
    "/deneb_disk/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject102/post2pre.nii.gz"
)
nonlin_reg_img_pvc_frac = "/deneb_disk/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject102/post2pre.nonlin.warped.pvc.frac.nii.gz"
rigid_reg_img_mask = "/deneb_disk/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject102/post2pre.mask.nii.gz"
rigid_reg_img_bfc = "/deneb_disk/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject102/post2pre.bfc.nii.gz"
rigid_reg_img_pvc_label = "/deneb_disk/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject102/post2pre.pvc.label.nii.gz"
rigid_reg_img_pvc_frac = "/deneb_disk/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject102/post2pre.pvc.frac.nii.gz"
jac_file = (
    "/deneb_disk/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject102/jacobian.nii.gz"
)


ddf = "/deneb_disk/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject102/ddf_nonlin.nii.gz"


tar_msk, target_mask_meta = LoadImage()(error_mask_img_rigid)
tar_msk = gaussian_filter(tar_msk, sigma=1)
tar_msk = np.float32(tar_msk < 1)

nib.save(
    nib.Nifti1Image(255 * (tar_msk), target_mask_meta["affine"]),
    target_msk_file,
)


nonlin_reg.nonlinear_reg(
    target_file=ref_img_pvc_frac,
    moving_file=rigid_reg_img_pvc_frac,
    output_file=nonlin_reg_img_pvc_frac,
    ddf_file=ddf,
    reg_penalty=3,
    nn_input_size=64,
    lr=1e-3,
    max_epochs=1000,
    loss="mse",
    jacobian_determinant_file=jac_file,
    target_mask=target_msk_file,
)


# Load the images and normalize their intensities
vref, _ = LoadImage()(ref_img_pvc_frac)
vwrp, _ = LoadImage()(nonlin_reg_img_pvc_frac)
msk, _ = LoadImage()(ref_img_mask)

vwrp = (255.0 / np.max(vwrp[msk > 0])) * vwrp
vref = (255.0 / np.max(vref[msk > 0])) * vref


# compute the error and smooth the error
vwrp = np.sqrt((vref - vwrp) ** 2)
# vwrp = gaussian_filter(vwrp, sigma=1)

nib.save(nib.Nifti1Image(vwrp, nonlin_reg.target.affine), error_img)
vwrp = vwrp * (msk > 0)

error_mask = opening(vwrp > ERR_THR)
nib.save(
    nib.Nifti1Image(255 * np.uint8(error_mask), nonlin_reg.target.affine),
    error_init_mask_img,
)

resection_mask = remove_small_objects(error_mask)
nib.save(
    nib.Nifti1Image(255 * np.uint8(resection_mask), nonlin_reg.target.affine),
    error_mask_img,
)
