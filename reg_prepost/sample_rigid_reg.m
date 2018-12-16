clc;clear all;close all;restoredefaultpath;
addpath(genpath('.'));
% Set the input arguments
bse_exe = '/home/ajoshi/BrainSuite18a/bin/bse';

sub = 'M1997HCD';

mov_img=['/big_disk/ajoshi/for_cleveland/pre_and_post_op_MRIs/',sub,'/postMRI.nii'];
ref_img=['/big_disk/ajoshi/for_cleveland/pre_and_post_op_MRIs/',sub,'/preMRI.nii'];
reg_img=['/big_disk/ajoshi/for_cleveland/pre_and_post_op_MRIs/',sub,'/post2preMRIuscrigid.nii.gz'];
err_file=['/big_disk/ajoshi/for_cleveland/pre_and_post_op_MRIs/',sub,'/Error.mask.nii.gz'];

reg_prepost(bse_exe, mov_img,ref_img,reg_img,err_file);
