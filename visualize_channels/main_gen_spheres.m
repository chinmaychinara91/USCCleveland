clc;clear all;close all;restoredefaultpath;
addpath(genpath('/ImagePTE1/ajoshi/code_farm/svreg/src'));
addpath(genpath('/ImagePTE1/ajoshi/code_farm/svreg/3rdParty'));



load('/ImagePTE1/ajoshi/HBM_Fingerprint_Data_For_Anand/Andrew_Pre-op_MRI_and_EZ_Map/Subject116/ChnInfo.mat');
v= load_untouch_nii_gz('/ImagePTE1/ajoshi/HBM_Fingerprint_Data_For_Anand/Andrew_Pre-op_MRI_and_EZ_Map/Subject116/T1s.nii.gz');
res = v.hdr.dime.pixdim(2:4);


h1 = icoSphereMesh(); std_sph.vertices=[h1.x*res(1),h1.y*res(2),h1.z*res(3)]; std_sph.faces=h1.face; clear h1;
std_sph.faces=[std_sph.faces(:,2),std_sph.faces(:,1),std_sph.faces(:,3)];

clo=hsv(15);

fstLtr='C';eleNum=1;

for j=1:length(chnLoc)
    
    if ~strcmp(chnName{j}(1),fstLtr)
        eleNum=eleNum+1;
        fstLtr=chnName{j}(1);
    end
        
    
    c = chnVoxIdx(j,:);
    h{j}.vertices = 1*std_sph.vertices+c.*res;
    h{j}.vcolor = repmat(clo(eleNum,:),size(std_sph.vertices,1),1);
    h{j}.faces = std_sph.faces;
    
%    h{j} = mysphere_tri(c,1,[1,0,0]);
    j
    
end

s=combine_surf(h);


figure;
patch('faces',s.faces,'vertices',s.vertices,'facevertexcdata',s.vcolor,'edgecolor','none','facecolor','flat');
axis equal;axis off;camlight;material dull;

writedfs('/ImagePTE1/ajoshi/HBM_Fingerprint_Data_For_Anand/Andrew_Pre-op_MRI_and_EZ_Map/Subject116/contacts_spheres.dfs',s);

