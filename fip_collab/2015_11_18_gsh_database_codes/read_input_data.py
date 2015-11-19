import numpy as np
import lagr_interp_func as lagr
import h5py
import sys

"""
in this version of the code the id of the tensor is an argument to
the script.

trying to reduce the amount of data to analyse by half sampling in
the angular variable
"""

# initialize important variables

tnum = sys.argv[1]

# define the number of increments for angular variables:

# these indices are defined for the original db inputs
inc_o = 3  # degree increment for angular variables

n_p1_o = 360/inc_o  # number of phi1 samples for FZ
n_P_o = (90/inc_o)+1  # number of Phi samples for FZ
n_p2_o = 60/inc_o  # number of phi2 samples for FZ

# n_eul_o is the number of orientations in the original db input set
n_eul_o = n_p1_o * n_P_o * n_p2_o

# these indices are defined for the sampled db inputs
inc = 6  # degree increment for angular variables

n_th = (60/inc)+1  # number of theta samples for FZ
n_p1 = 360/inc  # number of phi1 samples for FZ
n_P = (90/inc)+1  # number of Phi samples for FZ
n_p2 = 60/inc  # number of phi2 samples for FZ
n_en_guess = 16  # desired number of en samples

# n_eul_o is the number of orientations in the sampled db input set
n_eul = n_p1 * n_P * n_p2

# here we determine the sampling for en based on the roots of the
# chebyshev polynomial
a = 0.0050  # start for en range
b = 0.0085  # end for en range
en_inc = 0.0001  # en increment
envec = np.arange(a, b + en_inc, en_inc)
ai = np.int8(np.round(a/en_inc))-1  # index for start of en range
bi = np.int8(np.round(b/en_inc))-1  # index for end of en range
sample_indx = lagr.chebyshev_nodes(a, b, ai, en_inc, n_en_guess)
n_en = sample_indx.size

xnode = envec[sample_indx]  # en values for nodes of lagrange interpolation
print xnode

nvec = np.array([n_th, n_p1, n_P, n_p2, n_en])
print nvec

# create file for pre-database outputs
f_nhp = h5py.File('var_extract_%s.hdf5' % str(tnum).zfill(2), 'w')
var_set = f_nhp.create_dataset("var_set",
                               (n_eul*n_en, 6))

# Read Simulation info from "sim" file
filename = 'sim_Ti64_tensor_%s.txt' % str(tnum).zfill(2)

f = open(filename, "r")

linelist = f.readlines()

stmax = linelist[1].split()[4:7]

test_no = np.zeros([n_eul_o], dtype='int8')
euler = np.zeros([n_eul_o, 3])

for k in xrange(n_eul_o):
    temp_line = linelist[k+1]
    euler[k, :] = temp_line.split()[1:4]

f.close()

et_vec = np.linspace(.0001, .0100, 100)

# Get data for all simulations

# open file containing Matthew's data
filename = 'Results_tensor_%s.hdf5' % str(tnum).zfill(2)
f_mwp = h5py.File(filename, 'r')

max_err = 0
c = 0

print n_eul_o
print n_eul

for ii in xrange(0, n_eul_o):

    euldeg = euler[ii, :]*(180./np.pi)
    eulint = np.int64(np.round(euldeg))
    eulmod = np.mod(eulint, inc)
    # print ii
    # print euler[ii, :]
    # print euldeg
    # print eulint
    # print eulmod
    # print np.all(eulmod == 0)

    test_id = 'sim%s' % str(ii+1).zfill(7)

    if ii % 10000 == 0:
        print test_id

    if np.all(eulmod == 0) == True:

        dset = f_mwp.get(test_id)

        """
        Column order in each dataset:
        time,...
        sig11,sig22,sig33,sig12,sig13,sig23...
        e11,e22,e33,e12,e13,e23
        ep11,ep22,ep33,ep12,ep13,ep23,
        fip,gamdot,signorm

        """

        et = dset[:, 7:13]

        # calculate the norm of et
        et_norm = np.sqrt(np.sum(et[:, 0:3]**2, 1) +
                          2*np.sum(et[:, 3:6]**2, 1))

        err = np.max(np.abs(et_norm-et_vec))
        if err > max_err:
            print err
            max_err = err

        et_norm_red = et_norm[sample_indx+ai]
        var = dset[sample_indx+ai, 13]

        for jj in xrange(n_en):

            tmp = np.hstack([(np.int8(tnum)-1)*inc,
                             euler[ii, :],
                             et_norm_red[jj],
                             var[jj]])

            var_set[c, :] = tmp
            c += 1

# print np.prod(nvec[1:])
# print c

f_mwp.close()
f_nhp.close()
