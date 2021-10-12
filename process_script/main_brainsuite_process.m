clc;clear all;close all;

configfile = '/ImagePTE1/ajoshi/code_farm/USCCleveland/data/config_brainsuite.ini';
t1file = '/ImagePTE1/ajoshi/code_farm/USCCleveland/data/t1list.txt';

filetext = fileread(t1file);
t1subs = splitlines(filetext);

for j = 1:length(t1subs)
    
    
    [pth,subbasename,ext] = fileparts(t1subs{j});
    if strcmp(subbasename(end-2:end),'nii')
        subbasename = fullfile(pth,subbasename(1:end-4));
    else
        subbasename = fullfile(pth,subbasename);
    end
    
    brainsuite_process_subject(configfile,subbasename);

end
