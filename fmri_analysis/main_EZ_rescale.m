clear all;close all;clc;
restoredefaultpath;
addpath(genpath('/ImagePTE1/ajoshi/code_farm/svreg/src'));
addpath(genpath('/ImagePTE1/ajoshi/code_farm/svreg/3rdParty'));

EZ='/ImagePTE1/ajoshi/HBM_Fingerprint_Data_For_Anand/Analysis_Results/F1988I21/EZs.nii.gz';
v=load_nii_BIG_Lab(EZ)

v.img = v.img - min(v.img(:));

save_untouch_nii(v,'/ImagePTE1/ajoshi/HBM_Fingerprint_Data_For_Anand/Analysis_Results/F1988I21/EZs_positive.nii.gz');