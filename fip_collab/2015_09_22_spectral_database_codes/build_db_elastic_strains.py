import numpy as np
import h5py
import sys

"""
in this version of the code the id of the tensor is an argument to
the script.

the script saves the stress for a mostly elastic total strain
"""

# initialize important variables

tnum = sys.argv

inc = 5  # degree increment for angular variables

n_th_max = 120/inc  # number of theta samples in FOS
n_max = 360/inc  # number of phi1, Phi and phi2 samples in FOS
n_hlf = 180/inc  # half n_max

n_th = (60/inc)+1  # number of theta samples for FZ
n_p1 = 360/inc  # number of phi1 samples for FZ
n_P = (90/inc)+1  # number of Phi samples for FZ
n_p2 = 60/inc  # number of phi2 samples for FZ

n_tot = n_max**3  # total number of orientations

# create file for pre-database outputs
f_nhp = h5py.File('stress_extract_%s.hdf5' % str(tnum[1]).zfill(2), 'w')
sig_set = f_nhp.create_dataset("sig_set", (n_max, n_max, n_max))

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

euler_set = f_nhp.create_dataset("euler_set", euler.shape)
euler_set[...] = euler

for ii in xrange(0, n_tot):

    test_id = 'sim%s' % str(ii+1).zfill(7)

    if ii % 10000 == 0:
        print tnum[1]
        print test_id

    dset = f_mwp.get(test_id)

    """
    Column order in each dataset:
    time,...
    sig11,sig22,sig33,sig12,sig13,sig23...
    e11,e22,e33,e12,e13,e23
    ep11,ep22,ep33,ep12,ep13,ep23
    """

    sig11 = dset[2, 2]
    e11 = dset[2, 7]
    ep11 = dset[2, 13]

    if (ep11/e11)*100 > 0.1:
        print euler[ii, :]
        print "total strain: %s" % e11
        print "plastic strain: %s" % ep11

    eindx = np.int16(np.round((180./(inc*np.pi))*euler[ii, :]))
    sig_set[eindx[0], eindx[1], eindx[2]] = sig11

f_mwp.close()
f_nhp.close()
