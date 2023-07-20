
function reg_prepost_new(bse_exe, mov_img, ref_img, reg_img, err_file)

ref_img_bse=[tempname(),'.nii.gz'];
outdir = tempname();

%zip the nii files, as the codes that are used later need .nii.gz
%extensions
[pth, fname, ext]=fileparts(mov_img);
if ~strcmp(ext,'.gz')
    gzip(mov_img,outdir);
    mov_img=fullfile(outdir,[fname,'.nii.gz']);
end

[pth, fname, ext]=fileparts(ref_img);

if ~strcmp(ext,'.gz')
    gzip(ref_img,outdir);
    ref_img=fullfile(outdir,[fname,'.nii.gz']);
end


similarity='cr';
%perform skull stripping used for later
system(sprintf('%s -i %s -o %s --auto --trim',bse_exe, ref_img, ref_img_bse));

%perform rigid registration
usc_rigid_reg(mov_img, ref_img, reg_img, similarity, [])

% Load the images and normalize their intensities
vref = load_untouch_nii_gz(ref_img);
vwrp = load_untouch_nii_gz(reg_img);
msk = load_untouch_nii_gz(ref_img_bse);
vwrp.img=(255.0/max(double(vwrp.img(msk.img(:)>0))))*double(vwrp.img);
vref.img=(255.0/max(double(vref.img(msk.img(:)>0))))*double(vref.img);

% compute the error and smooth the error
vwrp.img = sqrt((double(vref.img) - double(vwrp.img)).^2);
vwrp.img = vwrp.img.*(msk.img>0);
vwrp.img=smooth3(vwrp.img,'gaussian',[7,7,7],1);

% Try to estimate the error mask using morphological operations
vwrp.img=bwareaopen(255.0*(vwrp.img>30),50,18);

SE = strel('cube',3);
vwrp.img=imerode(vwrp.img,SE);
vwrp.img=bwareaopen(255.0*(vwrp.img>0),150,18);
vwrp.img=imdilate(vwrp.img,SE);
vwrp.img=cast(vwrp.img,'uint8')*255;
save_untouch_nii_gz(vwrp, [err_file,'.mask.nii.gz'], 2);

