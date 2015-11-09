import numpy as np
import h5py
import sys

"""
in this version of the code the id of the tensor is an argument to
the script.

"""

# initialize important variables

tnum = sys.argv

# define the number of increments for angular variables:

inc = 3  # degree increment for angular variables

n_th_max = 120/inc  # number of theta samples in FOS
n_max = 360/inc  # number of phi1, Phi and phi2 samples in FOS
n_hlf = 180/inc  # half n_max

n_th = (60/inc)+1  # number of theta samples for FZ
n_p1 = 360/inc  # number of phi1 samples for FZ
n_P = (90/inc)+1  # number of Phi samples for FZ
n_p2 = 60/inc  # number of phi2 samples for FZ

n_tot = n_p1 * n_P * n_p2  # total number of orientations

N_samp = 100
width = 4 + 2*(100-59)

# create file for pre-database outputs
f_nhp = h5py.File('samp_interp_test_%s.hdf5' % str(tnum[1]).zfill(2), 'w')
ep_set = f_nhp.create_dataset("ep_set",
                              (N_samp, width))

# Read Simulation info from "sim" file
filename = 'sim_Ti64_tensor_%s.txt' % str(tnum[1]).zfill(2)

f = open(filename, "r")

linelist = f.readlines()

stmax = linelist[1].split()[4:7]

test_no = np.zeros([n_tot], dtype='int8')
euler = np.zeros([n_tot, 3])

for k in xrange(n_tot):
    temp_line = linelist[k+1]
    euler[k, :] = temp_line.split()[1:4]

f.close()

# Get data for all simulations

# open file containing Matthew's data
filename = 'Results_tensor_%s.hdf5' % str(tnum[1]).zfill(2)
f_mwp = h5py.File(filename, 'r')

iivec = np.unique(np.floor(np.random.rand(2*N_samp)*n_tot))[:N_samp]
c = 0

for ii in iivec:

    test_id = 'sim%s' % str(int(ii)+1).zfill(7)

    dset = f_mwp.get(test_id)

    """
    Column order in each dataset:
    time,...
    sig11,sig22,sig33,sig12,sig13,sig23...
    e11,e22,e33,e12,e13,e23
    ep11,ep22,ep33,ep12,ep13,ep23
    """

    et = dset[59:100, 7:13]
    ep11 = dset[59:100, 13]

    # calculate the norm of et
    et_norm = np.sqrt(et[:, 0]**2 + et[:, 1]**2 + et[:, 2]**2 +
                      et[:, 3]**2 + et[:, 4]**2 + et[:, 5]**2)

    tmp = np.hstack([np.int8(tnum[1])*inc, euler[ii, :], et_norm, ep11])

    ep_set[c, :] = np.float32(tmp)
    c += 1

f_mwp.close()
f_nhp.close()
