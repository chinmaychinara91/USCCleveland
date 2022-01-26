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


hemi = 'right'

outbase = 'data/BCI'
brannetome_base = '/ImagePTE1/ajoshi/code_farm/svreg/USCBrainMulti/Brainnetome/BCI-Brainnetome'
uscbrain_base = '/ImagePTE1/ajoshi/code_farm/svreg/USCBrainMulti/USCBrain'
hemi_surf_uscbrain_file = uscbrain_base + '.'+hemi+'.mid.cortex.dfs'
hemi_surf_brainnetome_file = brannetome_base + '.'+hemi+'.mid.cortex.dfs'
hemi_surf_out_file = outbase + '.'+hemi+'.mid.cortex.dfs'
hemi_surf_smooth_out_file = outbase + '.'+hemi+'.smooth.mid.cortex.dfs'


uscbrain_ids = [[502, 503, 504, 505]]
brainnnetome_ids = [[163, 164, 165, 166,
                     167, 168, 169, 170, 171, 172, 173, 174]]
uscbrain_new_ids = [[563, 564, 565, 566,
                     567, 568, 569, 570, 571, 572, 573, 574]]

uscbrain_hemi = readdfs(hemi_surf_uscbrain_file)
uscbrain_hemi_labs = uscbrain_hemi.labels.copy()
brainnetome_hemi = readdfs(hemi_surf_brainnetome_file)
brainnetome_hemi_vertices = brainnetome_hemi.vertices
brainnetome_hemi.vertices = uscbrain_hemi.vertices
uscbrain_hemi = patch_color_labels(uscbrain_hemi)
brainnetome_hemi = patch_color_labels(brainnetome_hemi)

view_patch_vtk(uscbrain_hemi)
view_patch_vtk(brainnetome_hemi)


class btmlCl:
    pass


btml = btmlCl()


class ubCl:
    pass


ub = ubCl()

for i in range(len(uscbrain_ids)):
    uid = uscbrain_ids[i]
    bid = brainnnetome_ids[i]
    uid_new = uscbrain_new_ids[i]

    u_ind = np.in1d(uscbrain_hemi.labels, uid).nonzero()[0]
    ub.labels = uscbrain_hemi.labels[u_ind]
    ub.vertices = uscbrain_hemi.vertices[u_ind, ]

    b_ind = np.in1d(brainnetome_hemi.labels, bid).nonzero()[0]
    btml.labels = brainnetome_hemi.labels[b_ind]

        

    btml.vertices = brainnetome_hemi.vertices[b_ind, ]

    print('Replacing', uid)
    print('With', uid_new)


    interpolate_labels(fromsurf=btml, tosurf=ub)

    for ind, r in enumerate(bid):
        ub.labels[ub.labels == r] = uid_new[ind]




    uscbrain_hemi.labels[u_ind] = ub.labels

uscbrain_hemi = patch_color_labels(uscbrain_hemi)
brainnetome_hemi = patch_color_labels(brainnetome_hemi)

view_patch_vtk(uscbrain_hemi)


#writedfs(hemi_surf_out_file, uscbrain_hemi)

uscbrain_hemi.vertices = brainnetome_hemi_vertices

writedfs(hemi_surf_out_file, uscbrain_hemi)

uscbrain_hemi.labels = uscbrain_hemi_labs

writedfs(hemi_surf_smooth_out_file, uscbrain_hemi)
