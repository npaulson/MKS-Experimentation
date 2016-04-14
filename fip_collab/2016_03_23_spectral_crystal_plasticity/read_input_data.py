import numpy as np
import constants
import h5py
import sys
import os

"""initialize important variables"""

tnum = np.int64(sys.argv[1])

C = constants.const()

# these indices are defined for the sampled db inputs
sub2rad = C['inc']*np.pi/180.

nvec = np.array([C['n_th'], C['n_p1'], C['n_P'], C['n_p2']])
print "nvec: %s" % str(nvec)

# create file for pre-database outputs
f = h5py.File(C['read_output'] % str(tnum).zfill(5), 'w')
var_set = f.create_dataset("var_set",
                           (C['n_eul'], 14))

c = 0

th_val = (tnum+0.5)*sub2rad
print "th_val: %s" % str(th_val*(180/np.pi))

for ii in xrange(1, 7):

    os.chdir('..')
    # nwd = os.getcwd() + '\\dir_db_input'
    nwd = os.getcwd() + '/dir_db_input'  # for unix
    os.chdir(nwd)

    """eulerset contents (for columns)
    phi1, Phi, phi2"""
    eulerset = np.loadtxt('euler%s.inp' % ii, skiprows=1)*(np.pi/180)

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

    sigma = varset1[:, :6]/(C['s']*C['epsdot']**C['m'])
    shearrate = (varset1[:, 6]/C['epsdot'])[:, None]
    wstar = varset2/C['epsdot']

    print "set %s" % ii
    print "thetaset.shape: %s" % str(thetaset.shape)
    print "eulerset.shape: %s" % str(eulerset.shape)
    print "sigma.shape: %s" % str(sigma.shape)
    print "wstar.shape: %s" % str(wstar.shape)
    print "shearrate.shape: %s" % str(shearrate.shape)

    var_set[c:c+setL, :] = np.hstack([thetaset,
                                      eulerset,
                                      sigma,
                                      shearrate,
                                      wstar])

    c += setL

f.close()

f_flag = open("flag%s" % str(tnum).zfill(5), 'w')
f_flag.close()
