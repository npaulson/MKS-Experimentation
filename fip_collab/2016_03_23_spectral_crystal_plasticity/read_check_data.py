import numpy as np
import constants
import h5py
import os

"""initialize important variables"""

C = constants.const()

# these indices are defined for the sampled db inputs
sub2rad = C['inc']*np.pi/180.

nvec = np.array([C['n_th'], C['n_p1'], C['n_P'], C['n_p2']])
print "nvec: %s" % str(nvec)

# create file for pre-database outputs
f = h5py.File("check_data.hdf5", 'w')

os.chdir('..')
# nwd = os.getcwd() + '\\dir_db_input'
nwd = os.getcwd() + '/check'  # for unix
os.chdir(nwd)

print os.getcwd()

"""angleset contents (for columns)
phi1, Phi, phi2, theta"""
angleset = np.loadtxt('testEuler.txt', skiprows=0)*(np.pi/180)
eulerset = angleset[:, :3]
thetaset = angleset[:, 3][:, None]

"""varset1 contents (for columns)
sigma'22, sigma'11, sigma'33, sigma'12, sigma'13, sigma'23,
total shear rate"""
varset1 = np.loadtxt("CrsytalStresses.txt", skiprows=0)

"""varset2 contents (for columns)
w12, w13, w23"""
varset2 = np.loadtxt("Wstar.txt", skiprows=0)

os.chdir('..')
# nwd = os.getcwd() + '\\dir_nhp'
nwd = os.getcwd() + '/dir_db_check'  # for unix
os.chdir(nwd)

sigma = varset1[:, :6]/(C['s']*C['epsdot']**C['m'])
shearrate = (varset1[:, 6]/C['epsdot'])[:, None]
wstar = varset2/C['epsdot']

print "thetaset.shape: %s" % str(thetaset.shape)
print "eulerset.shape: %s" % str(eulerset.shape)
print "sigma.shape: %s" % str(sigma.shape)
print "wstar.shape: %s" % str(wstar.shape)
print "shearrate.shape: %s" % str(shearrate.shape)

data = np.hstack([thetaset,
                  eulerset,
                  sigma,
                  shearrate,
                  wstar])

var_set = f.create_dataset("data", data=data)

f.close()
