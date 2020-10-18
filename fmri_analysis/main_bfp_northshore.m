clc;clear all;close all;restoredefaultpath;
addpath(genpath('/ImagePTE1/ajoshi/code_farm/bfp/src'));

% Set the input arguments
configfile='/big_disk/ajoshi/for_cleveland/bfpout/config_bfp_preproc.ini';

subname={'0019002','0019004','0019005','0019006','0019001','0019003'};

for jj=1:length(subname)
    t1=sprintf('/big_disk/ajoshi/for_cleveland/NorthShoreStudy/NorthShoreLIJ/LiteNIFTI/%s/session_1/mprage_1/defaced_mprage.nii.gz',subname{jj});
    fmri=sprintf('/big_disk/ajoshi/for_cleveland/NorthShoreStudy/NorthShoreLIJ/LiteNIFTI/%s/session_1/rest_1/rest.nii.gz',subname{jj});
    
    studydir='/big_disk/ajoshi/for_cleveland/bfpout';
    subid=subname{jj};
    sessionid='rest';
    
    % Call the bfp function
    bfp(configfile, t1, fmri, studydir, subid, sessionid, '');
    
end
