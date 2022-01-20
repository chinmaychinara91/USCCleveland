import nilearn as nl
import nilearn.image as ni
import numpy as np

bn = ni.load_img('/ImagePTE1/ajoshi/code_farm/svreg/USCBrainMulti/Brainnetome/BCI-Brainnetome.label.nii.gz')

uscbrain = ni.load_img('/ImagePTE1/ajoshi/code_farm/svreg/USCBrainMulti/USCBrain.label.nii.gz')

bn_data = bn.get_fdata()

uscbrain_data = uscbrain.get_fdata()

ind = np.where(bn_data>210)
uscbrain_data[ind] = bn_data[ind]

uscbrain=ni.new_img_like(uscbrain,uscbrain_data)

uscbrain.to_filename('mixed.label.nii.gz')