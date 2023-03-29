clc;clear all;close all;restoredefaultpath;
addpath(genpath('.'));

%add resection to label file

label_file = [ref_img(1:end-7),'.svreg.label.nii.gz'];
label_file_resection =  [ref_img(1:end-7),'.resection.label.nii.gz'];
resection_mask = '/deneb_disk/neuroimage_4944/sub-F1979I24/misc/temp/preop/resection.mask.nii.gz';

v = load_untouch_nii_gz(label_file);
m = load_untouch_nii_gz(resection_mask);
v.img(m.img>0) = 10000; % resecrion label is set to be 10000 in this case

save_untouch_nii_gz(v,label_file_resection);




