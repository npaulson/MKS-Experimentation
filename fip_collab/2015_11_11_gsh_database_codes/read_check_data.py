import numpy as np
import h5py
import sys
import leg_interp_func as lif

"""
in this version of the code the id of the tensor is an argument to
the script.

the script saves the magnitudes of the roots for the legendre polynomial
"""

# initialize important variables

tnum = sys.argv[1]

inc = 1

n_p1 = 11  # number of phi1 samples
n_P = 11  # number of Phi samples
n_p2 = 11  # number of phi2 samples
n_en = 100  # number of en samples

n_eul = n_p1*n_P*n_p2

# create file for pre-database outputs
f_nhp = h5py.File('test_extract_%s.hdf5' % str(tnum[1]).zfill(2), 'w')
ep_set = f_nhp.create_dataset("ep_set",
                              (n_eul*n_en, 6))

# Read Simulation info from "sim" file
filename = 'sim_Ti64_tensor_%s.txt' % str(tnum[1]).zfill(2)

f = open(filename, "r")

linelist = f.readlines()

stmax = linelist[1].split()[4:7]

test_no = np.zeros([n_eul], dtype='int8')
euler = np.zeros([n_eul, 3])

for k in xrange(n_eul):
    temp_line = linelist[k+1]
    euler[k, :] = temp_line.split()[1:4]

f.close()

et_vec = np.linspace(.0001, .0100, n_en)

# Get data for all simulations

# open file containing Matthew's data
filename = 'Results_tensor_%s.hdf5' % str(tnum).zfill(2)
f_mwp = h5py.File(filename, 'r')

euler_set = f_nhp.create_dataset("euler_set", euler.shape)
euler_set[...] = euler

max_err = 0
c = 0

for ii in xrange(0, n_eul):

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
    ep11,ep22,ep33,ep12,ep13,ep23
    """

    et = dset[:, 7:13]
    ep = dset[:, 13:19]

    # calculate the norm of et
    et_norm = np.sqrt(et[:, 0]**2 + et[:, 1]**2 + et[:, 2]**2 +
                      2*(et[:, 3]**2 + et[:, 4]**2 + et[:, 5]**2))

    ep11 = ep[:, 0]

    for jj in xrange(n_en):

        tmp = np.hstack([(np.int8(tnum)-1)*inc,
                         euler[ii, :],
                         et_norm[jj],
                         ep11[jj]])

        ep_set[c, :] = tmp
        c += 1

f_mwp.close()
f_nhp.close()
