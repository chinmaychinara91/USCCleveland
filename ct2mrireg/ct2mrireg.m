
function outimg = ct2mrireg(ct_img,mr_img,out_img, hires)

if ~exist('hires','var')
    hires=1;
end

if ischar(hires)
    hires = str2double(hires);
end

workdir = tempname();
mkdir(workdir);
temp_moving = fullfile(workdir, ['moving.nii.gz']);
temp_ref = fullfile(workdir, ['ref.nii.gz']);

workDir = tempname();
mkdir(workDir);

if hires~=0
    mr_img_hires = fullfile(workdir, ['hires_mr.nii.gz']);
    vct=load_untouch_nii_gz(ct_img);
    vct.hdr.dime.pixdim(2:4)
    % % Make the header look like BrainSuite header
    v=load_untouch_nii_gz(mr_img);
    v.hdr.hist.srow_x(1:3)=[v.hdr.dime.pixdim(2),0,0];
    v.hdr.hist.srow_y(1:3)=[0,v.hdr.dime.pixdim(3),0];
    v.hdr.hist.srow_z(1:3)=[0,0,v.hdr.dime.pixdim(4)];
    v.hdr.dime.scl_slope = 0;
    save_untouch_nii(v,mr_img_hires);
    
    %Generate high resolution MR so that output is hi res
    svreg_resample(mr_img_hires, mr_img_hires, '-res', vct.hdr.dime.pixdim(2), vct.hdr.dime.pixdim(3), vct.hdr.dime.pixdim(4));
    mr_img=mr_img_hires;
    
end

try
    check_nifti_file(ct_img, workDir);
    temp_moving = ct_img;
catch
    % If there is error in the header, replace it with 1mm isotropic header.
    v=load_untouch_nii(ct_img);
    % Make the header look like BrainSuite header
    v.hdr.hist.srow_x(1:3)=[v.hdr.dime.pixdim(2),0,0];
    v.hdr.hist.srow_y(1:3)=[0,v.hdr.dime.pixdim(3),0];
    v.hdr.hist.srow_z(1:3)=[0,0,v.hdr.dime.pixdim(4)];
    v.hdr.dime.scl_slope = 0;
    save_untouch_nii(v,temp_moving);
end


try
    check_nifti_file(mr_img, workDir);
    temp_ref = mr_img;
catch
    % If there is error in the header, replace it with 1mm isotropic header.
    v=load_untouch_nii(mr_img);
    % Make the header look like BrainSuite header
    v.hdr.hist.srow_x(1:3)=[v.hdr.dime.pixdim(2),0,0];
    v.hdr.hist.srow_y(1:3)=[0,v.hdr.dime.pixdim(3),0];
    v.hdr.hist.srow_z(1:3)=[0,0,v.hdr.dime.pixdim(4)];
    v.hdr.dime.scl_slope = 0;
    save_untouch_nii(v,temp_ref);
end

ct_img=temp_moving;
mr_img=temp_ref;
% dof = 6 rigid model
% optional input
opts = struct(...
    'dof', 6, ...
    'pngout', false,   ...
    'nthreads', 2     ... Number of (possible) parallel threads to use
    );

opts.similarity='cr';
%warning('off', 'MATLAB:maxNumCompThreads:Deprecated');
[M_world, ref_loc] = register_files_affine(ct_img, mr_img, out_img, opts);
%warning('on', 'MATLAB:maxNumCompThreads:Deprecated');
% Transform moving file using cubic interpolation


end
