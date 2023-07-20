clc;clear all;close all;restoredefaultpath;
addpath(genpath('.'));

%% Set the input arguments
bse_exe = '/home/ajoshi/BrainSuite21a/bin/bse';

mov_img = ['/deneb_disk/neuroimage_4944/sub-F1979I24/misc/temp_nonlin/postop/post_RS_MRI.nii'];
%% The following two files contain the output file names

% rigidly warped image
rigid_reg_img=['/deneb_disk/neuroimage_4944/sub-F1979I24/misc/temp_nonlin/preop/post2pre.nii.gz'];

% estimated error mask indicating resection or ablation
% This is not reliable, as it is suseptible to MRI artifacts
%If the error mask is not correct, then open 'ref_img' above in BrainSuite
% and the use mask tool from BrainSuite to get the correct mask.
err_base=['/deneb_disk/neuroimage_4944/sub-F1979I24/misc/temp_nonlin/preop/error_nonlin'];

ref_img_msk = ['/deneb_disk/neuroimage_4944/sub-F1979I24/misc/temp_nonlin/preop/MRI_1mm.mask.nii.gz'];
ref_img = ['/deneb_disk/neuroimage_4944/sub-F1979I24/misc/temp_nonlin/preop/MRI_1mm.pvc.frac.nii.gz'];
ref_img_bse= ['/deneb_disk/neuroimage_4944/sub-F1979I24/misc/temp_nonlin/preop/MRI_1mm.bse.pvc.frac.nii.gz'];
reg_img = ['/deneb_disk/neuroimage_4944/sub-F1979I24/misc/temp_nonlin/preop/post2pre.nonlin.bse.nii.gz'];

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

