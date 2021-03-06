import h5py
import numpy as np
import lagr_interp_func as lagr

"""
in this version of the code the id of the tensor is an argument to
the script.

the script saves the stress for a mostly elastic total strain
"""

# initialize important variables
n_tot = 21**3
N = 10

a = 0.0050  # start for en range
b = 0.0085  # end for en range
en_inc = 0.0001  # en increment
envec = np.arange(0.0001, 0.0100, en_inc)
ai = np.int64(np.round(a/en_inc))-1  # index for start of en range
bi = np.int64(np.round(b/en_inc))-1  # index for end of en range
sample_indx = lagr.chebyshev_nodes(a, b, ai, en_inc, N)+ai
xnode = envec[sample_indx]  # en values for nodes of lagrange interpolation

# create file for pre-database outputs
f_nhp = h5py.File('var_val.hdf5', 'w')
var_set = f_nhp.create_dataset("var_set", (n_tot, 4+sample_indx.size))

# Read Simulation info from "sim" file
filename = 'sim_Ti64_tensor_val.txt'

f = open(filename, "r")
linelist = f.readlines()

angle = np.zeros([n_tot, 4])
for k in xrange(n_tot):
    temp_line = linelist[k+1]
    angle[k, 0] = temp_line.split()[7]
    angle[k, 1:] = temp_line.split()[1:4]

f.close()

# Get data for all simulations

# open file containing Matthew's data
filename = 'Results_tensor_val.hdf5'
f_mwp = h5py.File(filename, 'r')

for ii in xrange(0, n_tot):

    test_id = 'sim%s' % str(ii+1).zfill(7)

    dset = f_mwp.get(test_id)

    """
    Column order in each dataset:
    time,...
    sig11,sig22,sig33,sig12,sig13,sig23...
    e11,e22,e33,e12,e13,e23
    ep11,ep22,ep33,ep12,ep13,ep23,
    fip,gamdot,sig_max
    """

    if ii == 0:
        et = dset[:, 7:13]
        et_norm = np.sqrt(et[:, 0]**2 + et[:, 1]**2 + et[:, 2]**2 +
                          2*(et[:, 3]**2 + et[:, 4]**2 + et[:, 5]**2))
        etsame = np.all(np.isclose(et_norm[sample_indx], xnode))
        print "is et_norm the same as xnode?: %s" % str(etsame)

    var = np.log(dset[sample_indx, 20])

    tmp = np.hstack([angle[ii, :],
                     var])

    var_set[ii, :] = tmp

f_mwp.close()
f_nhp.close()
