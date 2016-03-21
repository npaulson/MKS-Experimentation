import numpy as np
import constants
import h5py
import sys

"""
in this version of the code the id of the tensor is an argument to
the script.

trying to reduce the amount of data to analyse by half sampling in
the angular variable
"""

# initialize important variables

tnum = np.int64(sys.argv[1])

C = constants.const()

# these indices are defined for the sampled db inputs
sub2rad_eul = C['inc_eul']*np.pi/180.
sub2rad_th = C['inc_th']*np.pi/180.

# here we determine the sampling for en
a_std = 0.0050
b_std = 0.0085
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

nvec = np.array([C['n_th'], C['n_p1'], C['n_P'], C['n_p2'], C['n_en']])
print "nvec: %s" % str(nvec)

# create file for pre-database outputs
f_nhp = h5py.File(C['read_output'] % str(tnum).zfill(5), 'w')
var_set = f_nhp.create_dataset("var_set",
                               (C['n_eul']*C['n_en'], 6))

# Read Simulation info from "sim" file
filename = 'sim_Ti64_tensor_%s.txt' % str(tnum+1).zfill(2)

f = open(filename, "r")

linelist = f.readlines()

euler = np.zeros([C['n_eul'], 3])

for k in xrange(C['n_eul']):
    temp_line = linelist[k+1]
    euler[k, :] = temp_line.split()[1:4]

print np.max(euler, 0)*(180./np.pi)

f.close()

# Get data for all simulations

# open file containing Matthew's data
filename = 'Results_tensor_%s.hdf5' % str(tnum+1).zfill(2)
f_mwp = h5py.File(filename, 'r')

c = 0

th_val = (tnum+0.5)*sub2rad_th
print "th_val: %s" % str(th_val*(180/np.pi))

for ii in xrange(0, C['n_eul']):

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

    var = dset[sample_indx, 13:19]
    var_norm = np.sqrt(np.sum(var[:, 0:3]**2+2*var[:, 3:]**2, 1))

    for jj in xrange(n_en):

        tmp = np.hstack([th_val,
                         euler[ii, :],
                         xnode[jj],
                         var_norm[jj]])

        var_set[c, :] = tmp
        c += 1

print C['n_eul']*C['n_en']
print c

f_flag = open("flag%s" % str(tnum).zfill(5), 'w')
f_flag.close()

f_mwp.close()
f_nhp.close()
