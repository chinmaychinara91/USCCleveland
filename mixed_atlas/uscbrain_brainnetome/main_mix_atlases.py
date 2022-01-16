import nilearn
from dfsio import readdfs, writedfs
from surfproc import view_patch_vtk, patch_color_labels
import numpy as np


brannetome_base = '/ImagePTE1/ajoshi/code_farm/svreg/USCBrainMulti/Brainnetome/BCI-DNI_Brainnetome'
uscbrain_base = '/ImagePTE1/ajoshi/code_farm/svreg/USCBrainMulti/USCBrain'
left_surf_uscbrain_file = uscbrain_base + '.left.mid.cortex.dfs'
left_surf_brainnetome_file = brannetome_base + '.left.mid.cortex.dfs'


uscbrain_ids = [[502,503,504,505]]
brainnnetome_ids = [[163,164,165,166,167,168,169,170,171,172,173,174]]


uscbrain_left = readdfs(left_surf_uscbrain_file)
brainnetome_left = readdfs(left_surf_brainnetome_file)

view_patch_vtk(uscbrain_left)
view_patch_vtk(brainnetome_left)


for i in range(len(uscbrain_ids)):
    uid = uscbrain_ids[i]
    bid = brainnnetome_ids[i]

    ind = np.in1d(uscbrain_left.labels, uid)
    uscbrain_left.labels[ind]= 2000

    ind = np.in1d(brainnetome_left.labels, brainnnetome_ids)
    brainnetome_left.labels[ind]= 2000


    uscbrain_left = patch_color_labels(uscbrain_left)
    brainnetome_left = patch_color_labels(brainnetome_left)

    print(uid)
    print(bid)





view_patch_vtk(uscbrain_left)
view_patch_vtk(brainnetome_left)







