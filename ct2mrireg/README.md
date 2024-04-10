# ct2mrireg
CT 2 MRI Registration using correlation ratio based on registration code writtern by Chitresh Bhushan.
It requires Image Processing Toolbox.

The registration is based on Correlation Ratio as the cost function.

The model is 6 degrees of freedom (Rigid registration).

## Matlab
Please see main_ct2mrireg.m for usage.

## Compiled Binary
ct2mrireg.exe ct_img mr_img output_img

ct_img: the CT image in NIFTI format
mr_img: MR image in NIFTI format
output_img: output image in the NIFTI format

example: Type the following on the windows command prompt
ct2mrreg.exe CT_1.nii.gz MRI_1.nii.gz CT2MRI_1.nii.gz

