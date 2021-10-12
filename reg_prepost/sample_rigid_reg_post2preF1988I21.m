clc;clear all;close all;restoredefaultpath;
addpath(genpath('.'));

%% Set the input arguments
bse_exe = '/home/ajoshi/BrainSuite19b/bin/bse';

mov_img = '/ImagePTE1/ajoshi/HBM_Fingerprint_Data_For_Anand/post2prenii/post2pre_10_22_2020/de_identified/F1988I21/sub-F1988I21-F1988I21_postRS_MRI.nii.gz';
ref_img = '/ImagePTE1/ajoshi/HBM_Fingerprint_Data_For_Anand/post2prenii/post2pre_10_22_2020/de_identified/F1988I21/sub-F1988I21_T1w.nii.gz';
%% The following two files contain the output file names

% rigidly warped image
reg_img='/ImagePTE1/ajoshi/HBM_Fingerprint_Data_For_Anand/post2prenii/post2pre_10_22_2020/de_identified/F1988I21/post2pre.nii.gz';

% estimated error mask indicating resection or ablation
% This is not reliable, as it is suseptible to MRI artifacts
%If the error mask is not correct, then open 'ref_img' above in BrainSuite 
% and the use mask tool from BrainSuite to get the correct mask.
err_file='/ImagePTE1/ajoshi/HBM_Fingerprint_Data_For_Anand/post2prenii/post2pre_10_22_2020/de_identified/F1988I21/error.nii.gz';

%perform the registration
reg_prepost(bse_exe, mov_img,ref_img,reg_img,err_file);
