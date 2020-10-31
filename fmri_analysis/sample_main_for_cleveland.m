clc;clear all;close all;restoredefaultpath;

addpath(genpath('/ImagePTE1/ajoshi/code_farm/bfp/src'));

% Set the input arguments
configfile='/ImagePTE1/ajoshi/HBM_Fingerprint_Data_For_Anand/bfp_out/config_bfp_preproc.ini';

t1='/ImagePTE1/ajoshi/HBM_Fingerprint_Data_For_Anand/Single_Subject_fMRI_Data/sub-F1988I21/BrainSuite/brainsuite_files/preMRI_new.nii.gz';
%t1='/ImagePTE1/ajoshi/usc_music/sub-01/anat/T1.nii.gz';

%a=load_nii_BIG_Lab(t1o);
%a.img=33000+(a.img);
%a.img=a.img/10;
%save_untouch_nii_gz(a,t1);

fmri='/ImagePTE1/ajoshi/HBM_Fingerprint_Data_For_Anand/Single_Subject_fMRI_Data/sub-F1988I21/rfMRI/sub-F1988I21-F1988I21_rs_FMRI.nii.gz';

%fmri='/home/ajoshi/Downloads/BFP_issues/ACTL005/ACTL005.BOLD.resting.nii.gz';
studydir='/ImagePTE1/ajoshi/HBM_Fingerprint_Data_For_Anand/bfp_out';
subid='sub-F1988I21';
sessionid='rest';
TR='';
 
% Call the bfp function
%bfp(configfile, t1, fmri, studydir, subid, sessionid,TR);
gen_brainordinates('/home/ajoshi/BrainSuite19b', studydir, subid, sessionid);

%bfp.sh config.ini input/sub08001/anat/mprage_anonymized.nii.gz /big_disk/ajoshi/bfp_sample/input/sub08001/func/rest.nii.gz /big_disk/ajoshi/bfp_sample/output sub11 rest 2
