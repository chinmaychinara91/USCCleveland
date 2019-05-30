import nilearn as nl
from scipy.io import loadmat 

v = nl.image.load_img('/deneb_disk/M2005GBC/M2005GBC.nii.gz')


m = loadmat('/deneb_disk/M2005GBC/channels_and_mris.mat')

print('done')
