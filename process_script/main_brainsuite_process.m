clc;clear all;close all;
addpath(genpath('/ImagePTE1/ajoshi/code_farm/bfp/src'));

configfile = '/ImagePTE1/ajoshi/code_farm/USCCleveland/data/config_brainsuite.ini';
t1file = '/ImagePTE1/ajoshi/code_farm/USCCleveland/data/t1list.txt';

filetext = fileread(t1file);
t1subs = splitlines(filetext);

for j = 1:length(t1subs)
    
    
    tempdir = tempname;
    mkdir(tempdir);
    [orig_pth,subbasename,ext] = fileparts(t1subs{j});
    
    newt1file = fullfile(tempdir,[subbasename,ext]);
    
    copyfile(t1subs{j}, newt1file)
    [pth,subbasename,ext] = fileparts(newt1file);

    
    if strcmp(subbasename(end-2:end),'nii')
        subbasename = fullfile(pth,subbasename(1:end-4));
    else
        subbasename = fullfile(pth,subbasename);
    end
    
    
    if SVReg_done_check(subbasename)
        fprintf('BrainSuite processing is already done for %s',subbasename);
        continue;
    end
    
    brainsuite_process_subject(configfile,subbasename);
    
    copyfile(tempdir,orig_pth);
    rmdir(tempdir, 's');

end
