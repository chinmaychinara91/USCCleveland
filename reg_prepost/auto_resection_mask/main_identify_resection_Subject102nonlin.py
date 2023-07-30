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
from skimage.morphology import remove_small_objects


BrainSuitePATH = "/home/ajoshi/BrainSuite23a"
ERR_THR = 100

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
error_mask_img = "/deneb_disk/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject102/error_pre_post.mask.nii.gz"
error_init_mask_img = "/deneb_disk/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject102/error_pre_post.init.mask.nii.gz"


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
)
