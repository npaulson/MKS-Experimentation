import numpy as np
import h5py
import constants
import evalf


"""data contents
data[:, 0] = theta
data[:, 1:4] = phi1, Phi, phi2
data[:, 4:10] = sigma'11, sigma'22, sigma'33,
                sigma'12, sigma'13, sigma'23
                (outputs indexed 0:6)
data[:, 10] = total shear rate (output indexed 6)
data[:, 11:14] = w12, w13, w23 (outputs indexed 7:10)
"""

var_id = 0
thr = 0.0

C = constants.const()

f = h5py.File(C['combineread_output'], 'r')
data = f.get('var_set')[...]

theta_U = np.unique(data[:, 0])
# print "unique theta: %s" % str(theta_U)
phi1_U = np.unique(data[:, 1])
# print "unique phi1: %s" % str(phi1_U)
Phi_U = np.unique(data[:, 2])
# print "unique Phi: %s" % str(Phi_U)
phi2_U = np.unique(data[:, 3])
# print "unique phi2: %s" % str(phi2_U)

np.random.seed()

th = theta_U[np.int64(np.random.rand()*theta_U.size)]
# phi1 = phi1_U[np.int64(np.random.rand()*phi1_U.size)]
# Phi = Phi_U[np.int64(np.random.rand()*Phi_U.size)]
phi2 = phi2_U[np.int64(np.random.rand()*phi2_U.size)]

ang_sel = (data[:, 0] == th) * \
    (data[:, 3] == phi2)

print "theta: %s" % th
print "phi2: %s" % phi2

parameters = np.array([th, phi2])

theta = data[ang_sel, 0]
euler = data[ang_sel, 1:4]
Y = data[ang_sel, 4+var_id]
Y_ = evalf.evalf(theta, euler, var_id, thr)
error = np.abs(Y-Y_)

"""get a few error metrics"""
print "mean error: %s" % error.mean()
print "maximum error: %s" % error.max()

print "minimum function value: %s" % Y.min()
print "minimum reconstruction value: %s" % Y_.min()

print "mean function value: %s" % Y.mean()
print "mean reconstruction value: %s" % Y_.mean()

print "maximum function value: %s" % Y.max()
print "maximum reconstruction value: %s" % Y_.max()

slc = np.zeros((np.sum(ang_sel), 6))
slc[:, 0] = theta
slc[:, 1:4] = euler
slc[:, 4] = Y
slc[:, 5] = Y_
print slc.shape

f = h5py.File('slice.hdf5', 'w')
f.create_dataset('slice', data=slc)
f.create_dataset('parameters', data=parameters)
f.close()
