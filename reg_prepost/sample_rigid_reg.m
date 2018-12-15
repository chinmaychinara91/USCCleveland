clc;clear all;close all;restoredefaultpath;
addpath(genpath('.'));
% Set the input arguments
bse_exe = '/home/ajoshi/BrainSuite18a/bin/bse';

moving_filename='/big_disk/ajoshi/for_cleveland/pre_and_post_op_MRIs/M1976H8L/postMRI.nii';
gzip(moving_filename);
moving_filename='/big_disk/ajoshi/for_cleveland/pre_and_post_op_MRIs/M1976H8L/postMRI.nii.gz';
moving_filename_bse='/big_disk/ajoshi/for_cleveland/pre_and_post_op_MRIs/M1976H8L/postMRI.bse.nii.gz';
moving_filename_mask='/big_disk/ajoshi/for_cleveland/pre_and_post_op_MRIs/M1976H8L/postMRI.mask.nii.gz';



static_filename='/big_disk/ajoshi/for_cleveland/pre_and_post_op_MRIs/M1976H8L/preMRI.nii';
gzip(static_filename);
static_filename='/big_disk/ajoshi/for_cleveland/pre_and_post_op_MRIs/M1976H8L/preMRI.nii.gz';
static_filename_bse='/big_disk/ajoshi/for_cleveland/pre_and_post_op_MRIs/M1976H8L/preMRI.bse.nii.gz';
static_filename_mask='/big_disk/ajoshi/for_cleveland/pre_and_post_op_MRIs/M1976H8L/preMRI.mask.nii.gz';

output_filename='/big_disk/ajoshi/for_cleveland/pre_and_post_op_MRIs/M1976H8L/post2preMRIuscrigid.nii.gz';

similarity='cr';
%moving_mask='/big_disk/ajoshi/for_cleveland/pre_and_post_op_MRIs/M1997HCD/postMRI.nii';
moving_mask=moving_filename;%'/big_disk/ajoshi/for_cleveland/pre_and_post_op_MRIs/M1976H8L/postMRI.mask.nii.gz';
err_file='/big_disk/ajoshi/for_cleveland/pre_and_post_op_MRIs/M1976H8L/Error.nii.gz';


%system(sprintf('%s -i %s -o %s --mask %s --auto --trim',bse_exe, static_filename, static_filename_bse, static_filename_mask));
%system(sprintf('%s -i %s -o %s --mask %s --auto --trim',bse_exe, moving_filename, moving_filename_bse, moving_filename_mask));

usc_rigid_reg(moving_filename, static_filename, output_filename, similarity, moving_mask)


vref = load_untouch_nii_gz(static_filename);
vwrp = load_untouch_nii_gz(output_filename);
msk = load_untouch_nii_gz(static_filename_bse);
vwrp.img=(255.0/max(double(vwrp.img(msk.img(:)>0))))*double(vwrp.img);
vref.img=(255.0/max(double(vref.img(msk.img(:)>0))))*double(vref.img);

vwrp.img = sqrt((double(vref.img) - double(vwrp.img)).^2);
vwrp.img = vwrp.img.*(msk.img>0);

vwrp.img=smooth3(vwrp.img,'gaussian',[7,7,7],1);
%vwrp.img=imfill(255*(vwrp.img>30),6,'holes');
vwrp.img=bwareaopen(255.0*(vwrp.img>30),50,18);

SE = strel('cube',3);
vwrp.img=imerode(vwrp.img,SE);
vwrp.img=bwareaopen(255.0*(vwrp.img>0),150,18);
vwrp.img=imdilate(vwrp.img,SE);

save_untouch_nii_gz(vwrp, err_file,64);




