clc;clear all;close all;restoredefaultpath;
%addpath(genpath('/big_disk/ajoshi/coding_ground/bfp/supp_data'))
%addpath(genpath('/ImagePTE1/ajoshi/code_farm/svreg/dev'));

%addpath(genpath('/ImagePTE1/ajoshi/code_farm/svreg/src'));
%addpath(genpath('/ImagePTE1/ajoshi/code_farm/svreg/3rdParty'));

addpath(genpath('/ImagePTE1/ajoshi/code_farm/bfp/src'));
% Set the input arguments
configfile='/big_disk/ajoshi/for_cleveland/bfpout/config_bfp_preproc_2020.ini';

subname={'study12098','study12028','study11258','study12525','study12554','study13072','0019003','0019001','0019006','0019005','0019004','0019002'};

for jj=1:length(subname)
    t1=sprintf('/big_disk/ajoshi/for_cleveland/fmri_data/%s_MRI.nii.gz',subname{jj});
    fmri=sprintf('/big_disk/ajoshi/for_cleveland/fmri_data/%s_fMRI.nii.gz',subname{jj});
    
    studydir='/big_disk/ajoshi/for_cleveland/bfpout';
    subid=subname{jj};
    sessionid='rest';
    
    % Call the bfp function
    bfp(configfile, t1, fmri, studydir, subid, sessionid, '');
 %   gen_brainordinates('/home/ajoshi/BrainSuite19b', studydir, subid, sessionid);
 
end
