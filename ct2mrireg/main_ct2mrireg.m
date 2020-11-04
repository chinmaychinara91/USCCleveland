%% Intra-modal rigid registration example
clc; close all; clear;
restoredefaultpath;      % To remove conflicting libraries. May remove this line.

% mandatory inputs
fileDir = '/home/ajoshi/Downloads';
%ct_img = fullfile(fileDir, 'F1998H93_CT.nii'); % CT image
%mr_img = fullfile(fileDir, 'F1998H93_preMRI.bse.nii.gz'); % MR image
out_img = fullfile(fileDir, 'F1998H93_CT_bse_reg.nii'); %Output Image

mr_img = '/ImagePTE1/ajoshi/HBM_Fingerprint_Data_For_Anand/post2prenii/post2pre_10_22_2020/de_identified/231_M1979J41_2/M1979J41_preMRI.bse.nii';
ct_img = '/ImagePTE1/ajoshi/HBM_Fingerprint_Data_For_Anand/post2prenii/post2pre_10_22_2020/de_identified/231_M1979J41_2/new_data_sub-M1979J41/sMRI/sub-M1979J41-M1979J41_MRI.bse.nii.gz';%'/ImagePTE1/ajoshi/HBM_Fingerprint_Data_For_Anand/post2prenii/post2pre_10_22_2020/de_identified/231_M1979J41_2/new_data_sub-M1979J41/CT/sub-M1979J41-M1979J41_CT.nii';
out_img = '/ImagePTE1/ajoshi/HBM_Fingerprint_Data_For_Anand/post2prenii/post2pre_10_22_2020/de_identified/231_M1979J41_2/contrastmri2preMRI.nii.gz';
% Register CT (moving) to MR (fixed)
ct2mrireg(ct_img, mr_img, out_img);


