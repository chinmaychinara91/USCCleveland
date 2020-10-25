clc;clear all;close all;restoredefaultpath;
addpath(genpath('.'));

%% Set the input arguments
bse_exe = '/home/ajoshi/BrainSuite18a/bin/bse';
% subject ID
sub = 'M1976GB4';%'M1988H3A';

%% correct the paths
mov_img=['/big_disk/ajoshi/for_cleveland/1_29_2019/',sub,'/postMRI.nii'];
ref_img=['/big_disk/ajoshi/for_cleveland/1_29_2019/',sub,'/preMRI.nii'];

%% The following two files contain the output file names

% rigidly warped image
reg_img=['/big_disk/ajoshi/for_cleveland/1_29_2019/',sub,'/post2preMRIuscrigid.nii.gz'];

% estimated error mask indicating resection or ablation
% This is not reliable, as it is suseptible to MRI artifacts
%If the error mask is not correct, then open 'ref_img' above in BrainSuite 
% and the use mask tool from BrainSuite to get the correct mask.
err_file=['/big_disk/ajoshi/for_cleveland/1_29_2019/',sub,'/',sub,'.error.mask.nii.gz'];

%perform the registration
reg_prepost(bse_exe, mov_img,ref_img,reg_img,err_file);
