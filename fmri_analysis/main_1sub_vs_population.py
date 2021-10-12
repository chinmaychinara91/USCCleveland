import glob
import os
import scipy.io as spio

bfpout_dir = '/big_disk/ajoshi/for_cleveland/bfpout/0*'
sub_bfpout = '/ImagePTE1/ajoshi/HBM_Fingerprint_Data_For_Anand/bfp_out/sub-F1988I21'

sub_data = []
sub_lst = glob.glob(bfpout_dir)

for j in range(len(sub_lst)):

    _, sub_name = os.path.split(sub_lst[j])
    fname = os.path.join(sub_lst[j], 'func', sub_name + '_rest_bold.32k.GOrd.filt.mat')
    d = spio.loadmat(fname)['dtseries']

    if j==0:
        sub_data = np.zeros(d.shape[0])



print('Done.')
