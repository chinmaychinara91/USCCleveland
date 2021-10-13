# README

`brainsuite_process_all.exe` is a script written for automating the workflow for Cleveland clinic. 
To run the workflow, make sure that the following three files are in the same directory.
* brainsuite_process_all.exe
* config_brainsuite.ini
* t1list.txt

A sample of these three files can be downloaded with the release.
[Release_V1]


once all three files are in a directory, simply execute the `brainsuite_process_all.exe`. The executable will do the following for each T1 file:
1. read list of T1 images from  `t1list.txt`
2. read path of brainsuite from `config_brainsuite.ini`
3. Resample T1 images to 1mm cubic voxels are rename them to MRI_1mm.nii.gz
4. If the T1 files are not on `C:`, copy them to a temp directory, execute the entire brainsuite sequence, copy back the files to original location and delete the temp dir.
5. Run BrainSuite cortical extraction sequence
6. Run SVReg sequence using USCBrain atlas


The entire sequence takes about 1.5 hrs per subject, so please be patient.

If you have any questions, please email me Anand Joshi (ajoshi@usc.edu).
