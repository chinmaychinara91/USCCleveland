import nilearn.image as ni
from warp_utils import apply_warp
from aligner import Aligner
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

from warper import Warper
import nibabel.processing as nibp

BrainSuitePATH = "/home/ajoshi/BrainSuite23a"
ERR_THR = 80
rigid_reg = Aligner()


pre_mri_base_orig = '/deneb_disk/auto_resection/data_8_4_2023/sub-M2003N6J/sMRI/sub-M2003N6J-M2003N6J_MRI'
post_mri_base_orig ='/deneb_disk/auto_resection/data_8_4_2023/sub-M2003N6J/sMRI/sub-M2003N6J-M2003N6J_post_RS_MRI'

pre_mri_base = pre_mri_base_orig +'_1mm'
post_mri_base = post_mri_base_orig +'_1mm'

out_img = nibp.conform(nib.load(pre_mri_base_orig+'.nii.gz'))
out_img.to_filename(pre_mri_base + '.nii.gz')

out_img = nibp.conform(nib.load(post_mri_base_orig+'.nii.gz'))
out_img.to_filename(post_mri_base + '.nii.gz')



pre_mri_dir, _ = os.path.split(pre_mri_base)


mov_img_orig = post_mri_base + ".nii.gz"
if not os.path.isfile(mov_img_orig):
    mov_img_orig = post_mri_base + ".nii"


# Pre MRI pre processing


cmd = (
    os.path.join(BrainSuitePATH, "bin", "bse")
    + " -i "
    + pre_mri_base + '.nii.gz'
    + " -o "
    + pre_mri_base + '.bse.nii.gz'
    + " --prescale --auto --trim --mask "
    + pre_mri_base + '.mask.nii.gz'
)
os.system(cmd)

cmd = (
    os.path.join(BrainSuitePATH, "bin", "bfc")
    + " -i "
    + pre_mri_base + '.bse.nii.gz'
    + " -o "
    + pre_mri_base + '.bfc.nii.gz'
    + " --iterate -m "
    + pre_mri_base + '.mask.nii.gz'
)
os.system(cmd)


cmd = (
    os.path.join(BrainSuitePATH, "bin", "pvc")
    + " -i "
    + pre_mri_base + '.bfc.nii.gz'
    + " -o "
    + pre_mri_base + '.pvc.label.nii.gz'
    + " -f "
    + pre_mri_base + '.pvc.frac.nii.gz'
)
os.system(cmd)



# Post MRI pre processing


cmd = (
    os.path.join(BrainSuitePATH, "bin", "bse")
    + " -i "
    + post_mri_base + '.nii.gz'
    + " -o "
    + post_mri_base + '.bse.nii.gz'
    + " --prescale --auto --trim --mask "
    + post_mri_base + '.mask.nii.gz'
)
os.system(cmd)

cmd = (
    os.path.join(BrainSuitePATH, "bin", "bfc")
    + " -i "
    + post_mri_base + '.bse.nii.gz'
    + " -o "
    + post_mri_base + '.bfc.nii.gz'
    + " --iterate -m "
    + post_mri_base + '.mask.nii.gz'
)
os.system(cmd)


cmd = (
    os.path.join(BrainSuitePATH, "bin", "pvc")
    + " -i "
    + post_mri_base + '.bfc.nii.gz'
    + " -o "
    + post_mri_base + '.pvc.label.nii.gz'
    + " -f "
    + post_mri_base + '.pvc.frac.nii.gz'
)
os.system(cmd)




# "/deneb_disk/auto_resection/Ken_Post-op_MRI/sub-SUB"+sub+"/sMRI/sub-SUB"+sub+"-"+sub+"_MRI.nii"
mov_img = post_mri_base + ".bse.nii.gz"
# "/deneb_disk/auto_resection/Ken_Post-op_MRI/sub-SUB"+sub+"/sMRI/sub-SUB"+sub+"-"+sub+"_MRI.bse.nii.gz"
ref_img = pre_mri_base + ".bse.nii.gz"
# "/deneb_disk/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject"+sub+"/T1s.bse.nii.gz"
ref_img_mask = pre_mri_base + ".mask.nii.gz"
# "/deneb_disk/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject"+sub+"/T1s.mask.nii.gz"
ref_img_pvc_frac = pre_mri_base + ".pvc.frac.nii.gz"
# "/deneb_disk/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject"+sub+"/T1s.pvc.frac.nii.gz"
error_img = pre_mri_dir + "/error_pre_post.nii.gz"
# "/deneb_disk/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject"+sub+"/error_pre_post.nii.gz"
error_mask_img = pre_mri_dir + "/error_pre_post.mask.nii.gz"
# "/deneb_disk/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject"+sub+"/error_pre_post.mask.nii.gz"
error_init_mask_img = pre_mri_dir + "/error_pre_post.init.mask.nii.gz"
# "/deneb_disk/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject"+sub+"/error_pre_post.init.mask.nii.gz"


# rigidly warped image
rigid_reg_img = pre_mri_dir + "/post2pre.nii.gz"
# "/deneb_disk/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject"+sub+"/post2pre.nii.gz"
rigid_reg_img_bse = pre_mri_dir + "/post2pre.bse.nii.gz"
# "/deneb_disk/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject"+sub+"/post2pre.bse.nii.gz"
rigid_reg_img_mask = pre_mri_dir + "/post2pre.mask.nii.gz"
# "/deneb_disk/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject"+sub+"/post2pre.mask.nii.gz"
rigid_reg_img_bfc = pre_mri_dir + "/post2pre.bfc.nii.gz"
# "/deneb_disk/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject"+sub+"/post2pre.bfc.nii.gz"
rigid_reg_img_pvc_label = pre_mri_dir + "/post2pre.pvc.label.nii.gz"
# "/deneb_disk/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject"+sub+"/post2pre.pvc.label.nii.gz"
rigid_reg_img_pvc_frac = pre_mri_dir + "/post2pre.pvc.frac.nii.gz"
# "/deneb_disk/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject"+sub+"/post2pre.pvc.frac.nii.gz"

ddf = pre_mri_dir + "/ddf.nii.gz"
# "/deneb_disk/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject"+sub+"/ddf.nii.gz"


rigid_reg.affine_reg(
    fixed_file=ref_img,
    moving_file=mov_img,
    output_file=rigid_reg_img_bse,
    ddf_file=ddf,
    loss="cc",
    nn_input_size=64,
    lr=1e-6,
    max_epochs=1500,
    device="cuda",
)


moving, moving_meta = LoadImage()(mov_img_orig)
moving = EnsureChannelFirst()(moving)

target, _ = LoadImage()(ref_img)
target = EnsureChannelFirst()(target)


image_movedo = apply_warp(rigid_reg.ddf[None,], moving[None,], target[None,])

nib.save(
    nib.Nifti1Image(image_movedo[0, 0].detach().cpu().numpy(), rigid_reg.target.affine),
    rigid_reg_img,
)


cmd = (
    os.path.join(BrainSuitePATH, "bin", "bse")
    + " -i "
    + rigid_reg_img
    + " -o "
    + rigid_reg_img_bse
    + " --prescale --auto --trim --mask "
    + rigid_reg_img_mask
)
os.system(cmd)

cmd = (
    os.path.join(BrainSuitePATH, "bin", "bfc")
    + " -i "
    + rigid_reg_img_bse
    + " -o "
    + rigid_reg_img_bfc
    + " --iterate -m "
    + rigid_reg_img_mask
)
os.system(cmd)


cmd = (
    os.path.join(BrainSuitePATH, "bin", "pvc")
    + " -i "
    + rigid_reg_img_bfc
    + " -o "
    + rigid_reg_img_pvc_label
    + " -f "
    + rigid_reg_img_pvc_frac
)
os.system(cmd)


# Load the images and normalize their intensities
vref, _ = LoadImage()(ref_img_pvc_frac)
vwrp, _ = LoadImage()(rigid_reg_img_pvc_frac)
msk, _ = LoadImage()(ref_img_mask)

vwrp = (255.0 / np.max(vwrp[msk > 0])) * vwrp
vref = (255.0 / np.max(vref[msk > 0])) * vref


# compute the error and smooth the error
vwrp = np.sqrt((vref - vwrp) ** 2)
vwrp = vwrp * (msk > 0)
vwrp = gaussian_filter(vwrp, sigma=1)

nib.save(nib.Nifti1Image(vwrp, rigid_reg.target.affine), error_img)

error_mask = opening(vwrp > ERR_THR)
nib.save(
    nib.Nifti1Image(255 * np.uint8(error_mask), rigid_reg.target.affine),
    error_init_mask_img,
)


resection_mask = remove_small_objects(error_mask)
nib.save(
    nib.Nifti1Image(255 * np.uint8(resection_mask), rigid_reg.target.affine),
    error_mask_img,
)


# boblin code
nonlin_reg = Warper()

ref_img_bfc = pre_mri_base + ".bfc.nii.gz"
"""(
    "/deneb_disk/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject"
    + sub
    + "/T1s.bfc.nii.gz"
)
"""
error_img = pre_mri_dir + "/error_pre_post.nonlin.nii.gz"

error_init_mask_img = pre_mri_dir + "/error_pre_post.nonlin.init.mask.nii.gz"

error_mask_img_nonlin = pre_mri_dir + "/error_pre_post.nonlin.mask.nii.gz"


error_mask_img_rigid = pre_mri_dir + "/error_pre_post.init.mask.nii.gz"

target_msk_file = pre_mri_dir + "/target.mask.nii.gz"

# rigidly warped image

nonlin_reg_img_pvc_frac = pre_mri_dir + "/post2pre.nonlin.warped.pvc.frac.nii.gz"

jac_file = pre_mri_dir + "/jacobian.nii.gz"


ddf = pre_mri_dir + "/ddf_nonlin.nii.gz"


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
    error_mask_img_nonlin,
)
