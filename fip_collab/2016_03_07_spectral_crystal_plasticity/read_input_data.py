import numpy as np
import h5py
import sys
import os

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
var_set = f.create_dataset("var_set", (n_eul, 14))

th_val = (np.int64(tnum)+0.5)*sub2rad
print "th_val: %s" % str(th_val*(180/np.pi))

c = 0

for ii in xrange(1, 7):

    os.chdir('..')
    # nwd = os.getcwd() + '\\dir_db_input'
    nwd = os.getcwd() + '/dir_db_input'  # for unix
    os.chdir(nwd)

    """eulerset contents (for columns)
    phi1, Phi, phi2"""
    eulerset = np.loadtxt('euler%s.inp' % ii, skiprows=1)

    setL = eulerset.shape[0]

    thetaset = th_val*np.ones((setL, 1))

    """varset1 contents (for columns)
    sigma'22, sigma'11, sigma'33, sigma'12, sigma'13, sigma'23,
    total shear rate"""
    varset1 = np.loadtxt("crystalstresses%s_%s.dat" % (ii, tnum), skiprows=0)

    """varset2 contents (for columns)
    w12, w13, w23"""
    varset2 = np.loadtxt("wstar%s_%s.dat" % (ii, tnum), skiprows=0)

    os.chdir('..')
    # nwd = os.getcwd() + '\\dir_nhp'
    nwd = os.getcwd() + '/dir_nhp'  # for unix
    os.chdir(nwd)

    print "set %s" % ii
    print "thetaset.shape: %s" % str(thetaset.shape)
    print "eulerset.shape: %s" % str(eulerset.shape)
    print "varset1.shape: %s" % str(varset1.shape)
    print "varset2.shape: %s" % str(varset2.shape)

    var_set[c:c+setL, :] = np.hstack([thetaset, eulerset, varset1, varset2])

    c += setL

f.close()
