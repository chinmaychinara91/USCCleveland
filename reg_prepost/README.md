==README==

* This program performs rigid coregistration of pre and post MRIs and then 
computes the error mask (hopefully delineation of the ablation or resection).

* Please open sample_rigid_reg.m to see the usage. The inlined comments describe the usage.

Estimated error mask indicating resection or ablation may contain inaccuracies, 
as it is suseptible to MRI artifacts
If the error mask is not correct, then open reg_img (registered image) in BrainSuite 
and the use mask tool from BrainSuite to get the correct mask.

Please refer to the documentation of mask tool for the delineation
http://brainsuite.org/delineation/roi/masking/


Anand A Joshi
ajoshi@usc.edu
