import h5py
import sys
import numpy as np
import lagr_interp_func as lagr

"""
in this version of the code the id of the tensor is an argument to
the script.

the script saves the stress for a mostly elastic total strain
"""

# initialize important variables

tnum = sys.argv[1]

inc = 5  # degree increment for angular variables

n_th_max = 120/inc  # number of theta samples in FOS
n_max = 360/inc  # number of phi1, Phi and phi2 samples in FOS
n_hlf = 180/inc  # half n_max

n_th = 11  # number of theta samples for FZ
n_p1 = 11  # number of phi1 samples for FZ
n_P = 11  # number of Phi samples for FZ
n_p2 = 11  # number of phi2 samples for FZ

n_tot = n_p1*n_P*n_p2  # total number of orientations

# create file for pre-database outputs
f_nhp = h5py.File('check_extract_%s.hdf5' % str(tnum).zfill(2), 'w')
a = 0.0050  # start for en range
b = 0.0085  # end for en range
N = 10  # number of nodes
en_inc = 0.0001  # en increment
envec = np.arange(a, b + en_inc, en_inc)
ai = np.int8(np.round(a/en_inc))-1  # index for start of en range
bi = np.int8(np.round(b/en_inc))-1  # index for end of en range
sample_indx = lagr.chebyshev_nodes(a, b, ai, en_inc, N)
xnode = envec[sample_indx]  # en values for nodes of lagrange interpolation
print xnode

fip_set = f_nhp.create_dataset("fip_set", (n_p1, n_P, n_p2, N))

# Read Simulation info from "sim" file
filename = 'sim_Ti64_tensor_%s.txt' % str(tnum).zfill(2)

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
filename = 'Results_tensor_%s.hdf5' % str(tnum).zfill(2)
f_mwp = h5py.File(filename, 'r')

euler_set = f_nhp.create_dataset("euler_set", euler.shape)
euler_set[...] = euler

for ii in xrange(0, n_tot):

    test_id = 'sim%s' % str(ii+1).zfill(7)

    if ii % 10000 == 0:
        print tnum
        print test_id

    dset = f_mwp.get(test_id)

    """
    Column order in each dataset:
    time,...
    sig11,sig22,sig33,sig12,sig13,sig23...
    e11,e22,e33,e12,e13,e23
    ep11,ep22,ep33,ep12,ep13,ep23,
    fip
    """

    fip = dset[sample_indx, 19]

    eindx = np.int16(np.round((180./(1.*np.pi))*euler[ii, :])) - np.array([70, 130, 10])
    fip_set[eindx[0], eindx[1], eindx[2]] = np.log(fip)

f_mwp.close()
f_nhp.close()
