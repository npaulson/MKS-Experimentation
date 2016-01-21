import numpy as np
import h5py
import sys

"""
in this version of the code the id of the tensor is an argument to
the script.

trying to reduce the amount of data to analyse by half sampling in
the angular variable
"""

# initialize important variables

tnum = 5

# these indices are defined for the sampled db inputs
inc = 6  # degree increment for angular variables
sub2rad = inc*np.pi/180.

n_p1 = 360/inc  # number of phi1 samples for FZ
n_P = 90/inc  # number of Phi samples for FZ
n_p2 = 60/inc  # number of phi2 samples for FZ

# n_eul is the number of orientations in the sampled db input set
n_eul = n_p1 * n_P * n_p2

# here we determine the sampling for en
a = 0.0050  # start for en range
b = 0.0085  # end for en range
en_inc = 0.0001  # en increment
et_norm = np.linspace(.0001, .0100, 100)
ai = np.int64(np.round(a/en_inc))-1  # index for start of en range
bi = np.int64(np.round(b/en_inc))-1  # index for end of en range
sample_indx = bi

print sample_indx

# xnode: en values for nodes of lagrange interpolation
xnode = et_norm[sample_indx]
print xnode

nvec = np.array([n_p1, n_P, n_p2])
print "nvec: %s" % str(nvec)

# create file for pre-database outputs
f_nhp = h5py.File('var_extract_total.hdf5', 'w')
var_set = f_nhp.create_dataset("var_set",
                               (n_eul, 4))

# Read Simulation info from "sim" file
filename = 'sim_Ti64_tensor_%s.txt' % str(tnum).zfill(2)

f = open(filename, "r")

linelist = f.readlines()

euler = np.zeros([n_eul, 3])

for k in xrange(n_eul):
    temp_line = linelist[k+1]
    euler[k, :] = temp_line.split()[1:4]

f.close()

# Get data for all simulations

# open file containing Matthew's data
filename = 'Results_tensor_%s.hdf5' % str(tnum).zfill(2)
f_mwp = h5py.File(filename, 'r')

c = 0

for ii in xrange(0, n_eul):

    if np.isclose(euler[ii, 1], np.pi/2):
        continue

    test_id = 'sim%s' % str(ii+1).zfill(7)

    if ii % 10000 == 0:
        print test_id

    dset = f_mwp.get(test_id)

    """
    Column order in each dataset:
    time,...
    sig11,sig22,sig33,sig12,sig13,sig23...
    e11,e22,e33,e12,e13,e23
    ep11,ep22,ep33,ep12,ep13,ep23,
    fip,gamdot,signorm

    """

    var = dset[sample_indx, 19]

    tmp = np.hstack([euler[ii, :],
                     var])
    var_set[c, :] = tmp

    c += 1

f_mwp.close()
f_nhp.close()
