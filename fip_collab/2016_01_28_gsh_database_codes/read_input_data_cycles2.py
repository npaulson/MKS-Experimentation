import numpy as np
import h5py
import sys

"""
in this version of the code the id of the tensor is an argument to
the script.

trying to reduce the amount of data to analyse by half sampling in
the angular variable
"""

tnum = sys.argv[1]

# initialize important variables
n_ang = 21**3
n_cyc = 100

# create file for pre-database outputs
f_nhp = h5py.File('var_extract_%s.hdf5' % str(tnum).zfill(2), 'w')
var_set = f_nhp.create_dataset("var_set",
                               (n_ang*n_cyc, 6))

# Read Simulation info from "sim" file
filename = 'sim_Ti64_tensor_%s.txt' % str(tnum).zfill(2)

f = open(filename, "r")

linelist = f.readlines()

angles = np.zeros([n_ang, 4])

for k in xrange(n_ang):
    temp_line = linelist[k+1]
    angles[k, 0] = temp_line.split()[7]
    angles[k, 1:4] = temp_line.split()[1:4]

f.close()

# Get data for all simulations

# open file containing Matthew's data
filename = 'Results_tensor_%s.hdf5' % str(tnum).zfill(2)
f_mwp = h5py.File(filename, 'r')

c = 0

for ii in xrange(n_ang):

    test_id = 'sim%s' % str(ii+1).zfill(7)

    if ii % 10000 == 0:
        print test_id

    dset = f_mwp.get(test_id)

    """
    Column order in each dataset:
    fip,gamdot,signorm

    """

    for jj in xrange(n_cyc):

        tmp = np.hstack([angles[ii, :],
                         jj,
                         dset[jj, 0]])

        var_set[c, :] = tmp
        c += 1

print c
print n_ang*n_cyc

f_mwp.close()
f_nhp.close()
