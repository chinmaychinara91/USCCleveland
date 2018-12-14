%% Intra-modal rigid registration example
clc; close all; clear;
restoredefaultpath;      % To remove conflicting libraries. May remove this line.

% mandatory inputs
fileDir = '/home/ajoshi/Downloads';
ct_img = fullfile(fileDir, 'F1998H93_CT.nii'); % CT image
mr_img = fullfile(fileDir, 'F1998H93_preMRI.bse.nii.gz'); % MR image
out_img = fullfile(fileDir, 'F1998H93_CT_bse_reg.nii'); %Output Image

% Register CT (moving) to MR (fixed)
ct2mrireg(ct_img, mr_img, out_img);


