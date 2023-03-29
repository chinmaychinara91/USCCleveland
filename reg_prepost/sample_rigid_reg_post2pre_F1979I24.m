clc;clear all;close all;restoredefaultpath;
addpath(genpath('.'));

%% Set the input arguments
bse_exe = '/home/ajoshi/BrainSuite21a/bin/bse';

mov_img = ['/deneb_disk/neuroimage_4944/sub-F1979I24/misc/temp/postop/post_RS_MRI.nii'];
ref_img = ['/deneb_disk/neuroimage_4944/sub-F1979I24/misc/temp/preop/MRI_1mm.nii.gz'];
%% The following two files contain the output file names

% rigidly warped image
reg_img=['/deneb_disk/neuroimage_4944/sub-F1979I24/misc/temp/preop/post2pre.nii.gz'];

% estimated error mask indicating resection or ablation
% This is not reliable, as it is suseptible to MRI artifacts
%If the error mask is not correct, then open 'ref_img' above in BrainSuite
% and the use mask tool from BrainSuite to get the correct mask.
err_file=['/deneb_disk/neuroimage_4944/sub-F1979I24/misc/temp/preop/error.nii.gz'];

%perform the registration
reg_prepost(bse_exe, mov_img,ref_img,reg_img,err_file);


