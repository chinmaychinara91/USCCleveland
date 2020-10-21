clc;clear all;close all;restoredefaultpath;
addpath(genpath('/ImagePTE1/ajoshi/code_farm/bfp/src'));

% Set the input arguments
configfile='/ImagePTE1/ajoshi/HBM_Fingerprint_Data_For_Anand/bfp_out/config_bfp_preproc.ini';

    t1='/ImagePTE1/ajoshi/HBM_Fingerprint_Data_For_Anand/Single_Subject_fMRI_Data/sub-F1988I21/BrainSuite/brainsuite_files/preMRI_new.nii.gz';
    fmri='/ImagePTE1/ajoshi/HBM_Fingerprint_Data_For_Anand/Single_Subject_fMRI_Data/sub-F1988I21/rfMRI/F1988I21_rs_FMRI.nii.gz';
    
    studydir='/ImagePTE1/ajoshi/HBM_Fingerprint_Data_For_Anand/bfp_out';
    subid='sub-F1988I21';
    sessionid='rest';
    
    % Call the bfp function
    bfp(configfile, t1, fmri, studydir, subid, sessionid, '');
