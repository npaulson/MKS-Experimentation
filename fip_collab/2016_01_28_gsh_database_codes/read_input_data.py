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

tnum = sys.argv[1]

# these indices are defined for the sampled db inputs
inc_eul = 5  # degree increment for angular variables
inc_th = 1.5
sub2rad_eul = inc_eul*np.pi/180.
sub2rad_th = inc_th*np.pi/180.


n_th = np.int64(60/inc_th)  # number of theta samples for FZ
n_p1 = 360/inc_eul  # number of phi1 samples for FZ
n_P = 90/inc_eul  # number of Phi samples for FZ
n_p2 = 60/inc_eul  # number of phi2 samples for FZ

# n_eul is the number of orientations in the sampled db input set
n_eul = n_p1 * n_P * n_p2
# n_eul_old = n_p1 * (n_P+1) * n_p2
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
sample_indx = np.arange(ai, bi+5, 3)
n_en = sample_indx.size

print sample_indx

# xnode: en values for nodes
xnode = et_norm[sample_indx]
print xnode

nvec = np.array([n_th, n_p1, n_P, n_p2, n_en])
print "nvec: %s" % str(nvec)

# create file for pre-database outputs
f_nhp = h5py.File('var_extract_%s.hdf5' % str(tnum).zfill(2), 'w')
var_set = f_nhp.create_dataset("var_set",
                               (n_eul*n_en, 6))

# Read Simulation info from "sim" file
filename = 'sim_Ti64_tensor_%s.txt' % str(tnum).zfill(2)

f = open(filename, "r")

linelist = f.readlines()

euler = np.zeros([n_eul_old, 3])

for k in xrange(n_eul_old):
    temp_line = linelist[k+1]
    euler[k, :] = temp_line.split()[1:4]

f.close()

# Get data for all simulations

# open file containing Matthew's data
filename = 'Results_tensor_%s.hdf5' % str(tnum).zfill(2)
f_mwp = h5py.File(filename, 'r')

c = 0
d = 0

th_val = ((np.int64(tnum)-1)+0.5)*sub2rad_th
print "th_val: %s" % str(th_val*(180/np.pi))

for ii in xrange(0, n_eul_old):

    if np.isclose(euler[ii, 1], np.pi/2):
        d += 1
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

    for jj in xrange(n_en):

        tmp = np.hstack([th_val,
                         euler[ii, :],
                         xnode[jj],
                         var[jj]])

        var_set[c, :] = tmp
        c += 1

print n_eul*n_en
print c
print d

f_mwp.close()
f_nhp.close()
