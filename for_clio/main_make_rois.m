% Before running the script, open brainstorm, create subject, then import MRI. click on MNI registration
% select mri and export to matlab
% after that there should be 'mri' structure in the matlab window. Then you
% can run the script below.
clc
clear
addpath(genpath('/home/ajoshi/coding_ground/brainstorm3'))
addpath(genpath('/home/ajoshi/coding_ground/svreg/3rdParty'))


NUMROIS=1000;

exclude_rois=[800,900,720,721,740,760,700,701];
%Give subject name
name='M2005GBC';

%%
%CREATE PATHS FOR DATA

%Create path for channel/mris file (that's is provided by CLEVELAND)
brain_msk = '/deneb_disk/M2005GBC/CORSUREX_DATA/M2005GBC.mask.nii.gz';
channel_file = '/deneb_disk/M2005GBC/channels_and_mris.mat';
input_mri_name='/deneb_disk/M2005GBC/M2005GBC.nii.gz';
svreg_labels='/deneb_disk/M2005GBC/SVREG_DATA/M2005GBC.svreg.label.nii.gz';
%%
%Radius spheres created to reperesent contacts of electrodes
Radius=2;

output_name='rois.nii.gz';

create_rois_electrodes(name,channel_file,input_mri_name,Radius,output_name)

vmsk = load_untouch_nii(output_name);
msk = load_untouch_nii(brain_msk);
msk.img=double(msk.img);
vlab = load_untouch_nii(svreg_labels);

vlab.img(vlab.img>=2000)=0;
labs = mod(vlab.img,1000);

%labs(labs>600)=0;
% remove exluded rois such as brainstem, cerebellum, ventricles
labs(ismember(labs,exclude_rois))=0;

msk.img(vmsk.img>0 | labs ==0)=0;


ind = find(msk.img(:)>0);

sz = size(msk.img);
[X, Y, Z] = meshgrid(1:sz(1), 1:sz(2), 1:sz(3));

tic
lab = kmeans([X(ind),Y(ind),Z(ind)],NUMROIS);
toc

msk.img(ind) = lab+1000; % newly generated labels
msk.img(vmsk.img>0)=vmsk.img(vmsk.img>0); % electrode labels
msk.hdr.dime.datatype=8; msk.hdr.bitpix=32;
save_untouch_nii(msk,'rois.nii.gz');













%%
%Load CHANNEL/mris data

