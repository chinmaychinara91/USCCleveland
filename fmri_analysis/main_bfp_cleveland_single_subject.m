clc;clear all;close all;restoredefaultpath;
addpath(genpath('/ImagePTE1/ajoshi/code_farm/bfp/src'));

% Set the input arguments
configfile='/big_disk/ajoshi/for_cleveland/bfpout/config_bfp_preproc.ini';

%t1='/ImagePTE1/ajoshi/HBM_Fingerprint_Data_For_Anand/Single_Subject_fMRI_Data/sub-F1988I21/BrainSuite/brainsuite_files/preMRI_new.nii.gz';
%fmri='/ImagePTE1/ajoshi/HBM_Fingerprint_Data_For_Anand/Single_Subject_fMRI_Data/sub-F1988I21/rfMRI/F1988I21_rs_FMRI.nii.gz';

t1 = '/home/ajoshi/Downloads/sub-F1979I24/BrainSuite/brainsuite_files/preMRI_new.nii.gz';
fmri = '/home/ajoshi/Downloads/sub-F1979I24/rfMRI/sub-F1979I24-F1979I24_fMRI.nii';
studydir='/big_disk/ajoshi/for_cleveland/bfpout';
subid='sub-F1979I24';
sessionid='rest';

% Call the bfp function
%bfp(configfile, t1, fmri, studydir, subid, sessionid, '');
gen_brainordinates('/home/ajoshi/BrainSuite19b', studydir, subid, sessionid);


