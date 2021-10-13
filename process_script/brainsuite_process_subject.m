% authors: Anand A. Joshi (ajoshi@usc.edu)
% University of Southern California

function brainsuite_process_subject(configfile,subbasename)

if nargin ~=2
    disp('Incorrect number of input arguments (2 required)');
    error('exiting');
end
disp('Starting Processing');

p=inputParser;

addRequired(p,'configfile',@ischar);
addRequired(p,'subbasename',@ischar);
parse(p,configfile,subbasename);


%% Read configuration file and set environment variables
%%
fprintf('# Starting Run\n');
if ~exist(configfile,'file')
    error('Config file: %s \n: File does not exist\n',configfile);
end

fprintf('## Reading config file\n');
config=ini2struct(configfile);
fprintf(' done\n');
%% Setting up the environment
%%
setenv('BrainSuiteDir',config.BrainSuitePath);

BrainSuitePath=config.BrainSuitePath;

bst_exe=fullfile(BrainSuitePath,'bin','cortical_extraction.sh');
svreg_exe=fullfile(BrainSuitePath,'svreg','bin','svreg.sh');
svreg_resample_exe=fullfile(BrainSuitePath,'svreg','bin','svreg_resample.sh');

USCBrainbasename=fullfile(BrainSuitePath,'svreg','USCBrain','USCBrain');

[pth,sub,ext]=fileparts(subbasename);
subbasename_r = fullfile(pth,'MRI_1mm');

cmd=[svreg_resample_exe,' ',subbasename,'.nii.gz ', subbasename_r,'.nii.gz'];
unix(cmd);

subbasename = subbasename_r;
cmd=[bst_exe,' ',subbasename];
unix(cmd);

cmd=[svreg_exe,' ',subbasename,' ',USCBrainbasename];
unix(cmd);



fprintf('All done!\n\n');
