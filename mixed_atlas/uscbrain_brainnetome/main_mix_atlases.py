import nilearn
from dfsio import readdfs, writedfs
from surfproc import view_patch_vtk, patch_color_labels
import numpy as np
from scipy.spatial import cKDTree


def interpolate_labels(fromsurf=[], tosurf=[]):
    ''' interpolate labels from surface to to surface'''
    tree = cKDTree(fromsurf.vertices)
    d, inds = tree.query(tosurf.vertices, k=1, p=2)
    tosurf.labels = fromsurf.labels[inds]
    return tosurf



brannetome_base = '/ImagePTE1/ajoshi/code_farm/svreg/USCBrainMulti/Brainnetome/BCI-Brainnetome'
uscbrain_base = '/ImagePTE1/ajoshi/code_farm/svreg/USCBrainMulti/USCBrain'
left_surf_uscbrain_file = uscbrain_base + '.left.mid.cortex.dfs'
left_surf_brainnetome_file = brannetome_base + '.left.mid.cortex.dfs'




uscbrain_ids = [[502,503,504,505]]
brainnnetome_ids = [[163,164,165,166,167,168,169,170,171,172,173,174]]


uscbrain_left = readdfs(left_surf_uscbrain_file)
brainnetome_left = readdfs(left_surf_brainnetome_file)
brainnetome_left.vertices = uscbrain_left.vertices
uscbrain_left = patch_color_labels(uscbrain_left)
brainnetome_left = patch_color_labels(brainnetome_left)

view_patch_vtk(uscbrain_left)
view_patch_vtk(brainnetome_left)

class btmlCl:
    pass

btml = btmlCl()

class ubCl:
    pass

ub = ubCl()

for i in range(len(uscbrain_ids)):
    uid = uscbrain_ids[i]
    bid = brainnnetome_ids[i]

    u_ind = np.in1d(uscbrain_left.labels, uid).nonzero()[0]
    ub.labels = uscbrain_left.labels[u_ind]
    ub.vertices = uscbrain_left.vertices[u_ind,]

    b_ind = np.in1d(brainnetome_left.labels, bid).nonzero()[0]
    btml.labels = brainnetome_left.labels[b_ind]
    btml.vertices = brainnetome_left.vertices[b_ind,]



    print('Replacing', uid)
    print('With', bid)

    
    interpolate_labels(fromsurf=btml, tosurf=ub)

    uscbrain_left.labels[u_ind] = ub.labels

uscbrain_left = patch_color_labels(uscbrain_left)
brainnetome_left = patch_color_labels(brainnetome_left)

view_patch_vtk(uscbrain_left)







