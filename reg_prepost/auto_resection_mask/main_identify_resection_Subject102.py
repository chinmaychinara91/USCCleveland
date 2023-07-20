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

rigid_reg = Aligner()


mov_img_orig = "/ImagePTE1/ajoshi/HBM_Fingerprint_Data_For_Anand/auto_resection/Ken_Post-op_MRI/sub-SUB102/sMRI/sub-SUB102-102_MRI.nii"
mov_img = "/ImagePTE1/ajoshi/HBM_Fingerprint_Data_For_Anand/auto_resection/Ken_Post-op_MRI/sub-SUB102/sMRI/sub-SUB102-102_MRI.bse.nii.gz"
ref_img = "/ImagePTE1/ajoshi/HBM_Fingerprint_Data_For_Anand/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject102/T1s.bse.nii.gz"

# rigidly warped image
rigid_reg_img = "/ImagePTE1/ajoshi/HBM_Fingerprint_Data_For_Anand/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject102/post2pre.nii.gz"
rigid_reg_img_bse = "/ImagePTE1/ajoshi/HBM_Fingerprint_Data_For_Anand/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject102/post2pre.bse.nii.gz"

ddf = "/ImagePTE1/ajoshi/HBM_Fingerprint_Data_For_Anand/auto_resection/Andrew_Pre-op_MRI_and_EZ_Map/Subject102/ddf.nii.gz"


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






% Load the images and normalize their intensities
vref = load_untouch_nii_gz(ref_img);
vwrp = load_untouch_nii_gz(reg_img);
msk = load_untouch_nii_gz(ref_img_msk);
vwrp.img=(255.0/max(double(vwrp.img(msk.img(:)>0))))*double(vwrp.img);
vref.img=(255.0/max(double(vref.img(msk.img(:)>0))))*double(vref.img);

% compute the error and smooth the error
vwrp.img = sqrt((double(vref.img) - double(vwrp.img)).^2);
vwrp.img = vwrp.img.*(msk.img>0);
vwrp.img=smooth3(vwrp.img,'gaussian',[7,7,7],1);

save_untouch_nii_gz(vwrp, [err_base,'.nii.gz'], 16);

% Try to estimate the error mask using morphological operations
vwrp.img=bwareaopen(255.0*(vwrp.img>128),50,18);

SE = strel('cube',3);
vwrp.img=imerode(vwrp.img,SE);
vwrp.img=bwareaopen(255.0*(vwrp.img>0),150,18);
vwrp.img=imdilate(vwrp.img,SE);
vwrp.img=cast(vwrp.img,'uint8')*255;
save_untouch_nii_gz(vwrp, [err_base,'.mask.nii.gz'], 2);

