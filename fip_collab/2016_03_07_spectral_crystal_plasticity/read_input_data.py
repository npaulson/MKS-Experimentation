import numpy as np
import h5py
import sys

"""
in this version of the code the id of the tensor is an argument to
the script.

"""

# initialize important variables

tnum = sys.argv[1]

# these indices are defined for the sampled db inputs
inc = 1  # degree increment for angular variables
sub2rad = inc*np.pi/180.

n_th = np.int64(60/inc)  # number of theta samples for FZ
n_p1 = 360/inc  # number of phi1 samples for FZ
n_P = 90/inc  # number of Phi samples for FZ
n_p2 = 90/inc  # number of phi2 samples for FZ

# n_eul is the number of orientations in the sampled db input set
n_eul = n_p1 * n_P * n_p2

nvec = np.array([n_th, n_p1, n_P, n_p2])
print "nvec: %s" % str(nvec)

# create file for pre-database outputs
f = h5py.File('var_extract_%s.hdf5' % str(tnum).zfill(2), 'w')
var_set = f.create_dataset("var_set", (n_eul, 12))

th_val = ((np.int64(tnum)-1)+0.5)*sub2rad
print "th_val: %s" % str(th_val*(180/np.pi))

for ii in xrange(1, 7):

    eulerset = np.loadtxt('euler%s.inp' % ii, skiprows=1)
    print eulerset.shape

    varset1 = np.loadtxt("crystalstresses%s_%s" % (ii, tnum), skiprows=)
    varset2 = np.loadtxt("wstar%s_%s" % (ii, tnum), skiprows=)
    
    print "set %s" % ii
    print "eulerset.shape: %s" % str(eulerset.shape)
    print "varset1.shape: %s" % str(varset1.shape)
    print "varset2.shape: %s" % str(varset2.shape)

    """varset1 contents (for columns)
    sigma'22, sigma'11, sigma'33, sigma'12, sigma'13, sigma'23, total shear rate



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

    var = dset[sample_indx, 13:19]
    var_norm = np.sqrt(np.sum(var[:, 0:3]**2+2*var[:, 3:]**2, 1))

    for jj in xrange(n_en):

        tmp = np.hstack([th_val,
                         euler[ii, :],
                         xnode[jj],
                         var_norm[jj]])

        var_set[c, :] = tmp
        c += 1

print n_eul*n_en
print c
print d

f_mwp.close()
f_nhp.close()
