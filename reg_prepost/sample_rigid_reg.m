clc;clear all;close all;restoredefaultpath;

% Set the input arguments
moving_filename='/big_disk/ajoshi/for_cleveland/pre_and_post_op_MRIs/M1976H8L/postMRI.nii';
gzip(moving_filename);
moving_filename='/big_disk/ajoshi/for_cleveland/pre_and_post_op_MRIs/M1976H8L/postMRI.nii.gz';
static_filename='/big_disk/ajoshi/for_cleveland/pre_and_post_op_MRIs/M1976H8L/preMRI.nii';
gzip(static_filename);
static_filename='/big_disk/ajoshi/for_cleveland/pre_and_post_op_MRIs/M1976H8L/preMRI.nii.gz';
output_filename='/big_disk/ajoshi/for_cleveland/pre_and_post_op_MRIs/M1976H8L/post2preMRIuscrigid.nii.gz';
similarity='cr';
%moving_mask='/big_disk/ajoshi/for_cleveland/pre_and_post_op_MRIs/M1997HCD/postMRI.nii';
moving_mask='/big_disk/ajoshi/for_cleveland/pre_and_post_op_MRIs/M1976H8L/postMRI.nii.gz';

usc_rigid_reg(moving_filename, static_filename, output_filename, similarity, moving_mask)

