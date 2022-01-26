import nilearn as nl
import nilearn.image as ni
import numpy as np
from dfsio import readdfs
from scipy.spatial import cKDTree


def interpolate_labels(fromsurf=[], tosurf=[]):
    ''' interpolate labels from surface to to surface'''
    tree = cKDTree(fromsurf.vertices)
    d, inds = tree.query(tosurf.vertices, k=1, p=2)
    tosurf.labels = fromsurf.labels[inds]
    return tosurf


subbasename = 'data/BCI'

BCI_base = '/home/ajoshi/BrainSuite21a/svreg/BCI-DNI_brain_atlas/BCI-DNI_brain'

left_mid = readdfs(BCI_base + '.left.mid.cortex.dfs')
right_mid = readdfs(BCI_base + '.right.mid.cortex.dfs')
left_inner = readdfs(BCI_base + '.left.inner.cortex.dfs')
right_inner = readdfs(BCI_base + '.right.inner.cortex.dfs')
left_pial = readdfs(BCI_base + '.left.pial.cortex.dfs')
right_pial = readdfs(BCI_base + '.right.pial.cortex.dfs')
lsurf = readdfs(subbasename + '.left.mid.cortex.dfs')
rsurf = readdfs(subbasename + '.right.mid.cortex.dfs')


r1_vert = (right_pial.vertices + right_mid.vertices)/2.0
r2_vert = (right_inner.vertices + right_mid.vertices)/2.0
l1_vert = (left_pial.vertices + left_mid.vertices)/2.0
l2_vert = (left_inner.vertices + left_mid.vertices)/2.0

vol_lab = ni.load_img(
    '/home/ajoshi/BrainSuite21a/svreg/BCI-DNI_brain_atlas/BCI-DNI_brain.dws.label.nii.gz')
vol_img = vol_lab.get_fdata()

xres = vol_lab.header['pixdim'][1]
yres = vol_lab.header['pixdim'][2]
zres = vol_lab.header['pixdim'][3]

X, Y, Z = np.meshgrid(np.arange(vol_lab.shape[0]), np.arange(vol_lab.shape[1]),
                      np.arange(vol_lab.shape[2]), indexing='ij')

X = X*xres
Y = Y*yres
Z = Z*zres
#vol_img = sp.mod(vol_img, 1000)
# (np.floor((vol_img/10)) == 150) | (np.floor((vol_img/10)) == 151)
ind = (vol_img >= 1000) & (vol_img != 2000)
Xc = X[ind]
Yc = Y[ind]
Zc = Z[ind]


class t:
    pass


class f:
    pass


t.vertices = np.concatenate((Xc[:, None], Yc[:, None], Zc[:, None]), axis=1)
f.vertices = np.concatenate((left_mid.vertices, right_mid.vertices,
                             left_inner.vertices, right_inner.vertices,
                             left_pial.vertices, right_pial.vertices,
                             l1_vert, r1_vert, l2_vert, r2_vert))

f.labels = np.concatenate((lsurf.labels, rsurf.labels,
                           lsurf.labels, rsurf.labels,
                           lsurf.labels, rsurf.labels,
                           lsurf.labels, rsurf.labels,
                           lsurf.labels, rsurf.labels))

t = interpolate_labels(fromsurf=f, tosurf=t)

# here make sure that hanns labels are not modified TBD


uscbrain_data = vol_img * 0
uscbrain_data[ind] = t.labels
uscbrain_data[vol_img == 2000] = 2000

bn = ni.load_img(
    '/ImagePTE1/ajoshi/code_farm/svreg/USCBrainMulti/Brainnetome/BCI-Brainnetome.label.nii.gz')

""" uscbrain = ni.load_img(
    '/ImagePTE1/ajoshi/code_farm/svreg/USCBrainMulti/USCBrain.label.nii.gz')
 """
bn_data = bn.get_fdata()

ind = np.where(bn_data > 210)
uscbrain_data[ind] = 400 + bn_data[ind]  # Map Brainnetome subcortical IDs, which are 210> to USCBrain subcortical ID range (>600)

uscbrain = ni.new_img_like(BCI_base+'.label.nii.gz', np.int16(uscbrain_data))

uscbrain.to_filename('data/BCI.label.nii.gz')
