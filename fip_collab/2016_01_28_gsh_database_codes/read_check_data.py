import numpy as np
import h5py

"""
in this version of the code the id of the tensor is an argument to
the script.

trying to reduce the amount of data to analyse by half sampling in
the angular variable
"""

# initialize important variables
n_eul = 21**3
n_eul_old = n_eul

# here we determine the sampling for en
a_std = 0.0050
b_std = 0.0085
a = 0.00485  # start for en range
b = 0.00905  # end for en range
en_inc = 0.0001  # en increment
et_norm = np.linspace(.0001, .0100, 100)
ai = np.int64(np.round(a_std/en_inc))-1  # index for start of en range
bi = np.int64(np.round(b_std/en_inc))-1  # index for end of en range
sample_indx = np.arange(ai, bi+1, 1)
n_en = sample_indx.size

print sample_indx

# xnode: en values for nodes
xnode = et_norm[sample_indx]
print xnode

# create file for pre-database outputs
f_nhp = h5py.File('var_extract_check.hdf5', 'w')
var_set = f_nhp.create_dataset("var_set",
                               (n_eul*n_en, 6))

# Read Simulation info from "sim" file
filename = 'sim_Ti64_tensor_check.txt'

f = open(filename, "r")

linelist = f.readlines()

angles = np.zeros([n_eul_old, 4])

for k in xrange(n_eul_old):
    temp_line = linelist[k+1]
    angles[k, 0] = temp_line.split()[7]
    angles[k, 1:4] = temp_line.split()[1:4]

f.close()

# Get data for all simulations

# open file containing Matthew's data
filename = 'Results_tensor_check.hdf5'
f_mwp = h5py.File(filename, 'r')

for ii in xrange(n_eul_old):

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

    tmp = np.int64(np.random.rand()*sample_indx.size)
    indx_rand = sample_indx[tmp]

    en = et_norm[indx_rand]
    var = dset[indx_rand, 19]

    tmp = np.hstack([angles[ii, 0],
                     angles[ii, 1:4],
                     en,
                     var])

    var_set[ii, :] = tmp

f_mwp.close()
f_nhp.close()
