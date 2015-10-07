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

tnum = sys.argv

comp = "11"  # strain component of interest

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

a = .0064  # start of range for legendre interpolation
b = .0096  # end of range for legendre interpolation

# number of samples for the fourier representation of the legendre polynomial
N = 11

maxerr = 0  # maximum % error seen for any et vs ep curve

# create file for pre-database outputs
f_nhp = h5py.File('coeff_extract_%s.hdf5' % str(tnum[1]).zfill(2), 'w')
ep_set = f_nhp.create_dataset("ep_set",
                              (n_p1, n_P, n_p2, N))

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

etvec = np.linspace(.0001, .0100, 100)

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

    et = dset[:, 7:13]
    ep = dset[:, 13:19]

    # check that et is traceless
    et_tr = et[:, 0] + et[:, 1] + et[:, 2]

    et_tr_max = np.max(np.abs(et_tr))

    if et_tr_max > 1E-4:
        print ii
        print et_tr_max

    # calculate the norm of et
    et_norm = np.sqrt(et[:, 0]**2 + et[:, 1]**2 + et[:, 2]**2 +
                      et[:, 3]**2 + et[:, 4]**2 + et[:, 5]**2)

    # check that this curve is represented well with legendre polynomial

    ep11 = ep[:, 0]

    nodes, weights, rootsamp = lif.get_nodes(et_norm, ep11, a, b, N-1)

    eindx = np.int16(np.round((180./(inc*np.pi))*euler[ii, :]))

    ep_set[eindx[0], eindx[1], eindx[2], :] = rootsamp

f_mwp.close()
f_nhp.close()
