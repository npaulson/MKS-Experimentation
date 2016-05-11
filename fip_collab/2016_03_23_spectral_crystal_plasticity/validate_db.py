import numpy as np
import h5py
import constants
import evalf
import sys


var_id_set = {}
var_id_set[0] = "sigma'11"
var_id_set[1] = "sigma'22"
var_id_set[2] = "sigma'33"
var_id_set[3] = "sigma'12"
var_id_set[4] = "sigma'12"
var_id_set[5] = "sigma'23"
var_id_set[6] = "shear rate"
var_id_set[7] = "w12"
var_id_set[8] = "w13"
var_id_set[9] = "w23"

# var_id = 0
# thr = 0.0
# LL_p = 20

var_id = np.int64(sys.argv[1])
thr = np.float64(sys.argv[2])
LL_p = np.int64(sys.argv[3])

C = constants.const()

f = h5py.File("check_data_cal.hdf5", 'r')
data = f.get('data')[...]

theta = data[:, 0]
euler = data[:, 1:4]
Y = data[:, 4+var_id]
Y_ = evalf.evalf(theta, euler, var_id, thr, LL_p).real
error = np.abs(Y-Y_)

"""get a few error metrics"""
tmp = str(error.mean()) + ", " + str(error.max()) + ", " + str(error.std())
print "mean, max and std of error: %s" % tmp

tmp = str(Y.min()) + ", " + str(Y.mean()) + ", " + str(Y.max())
print "min, mean and max of function value: %s" % tmp

tmp = str(Y_.min()) + ", " + str(Y_.mean()) + ", " + str(Y_.max())
print "min, mean and max of reconstruction value: %s" % tmp

import matplotlib.pyplot as plt
plt.figure(num=1, figsize=[6.5, 4.5])
indx = np.argsort(Y)
sortY = Y[indx]
sortY_ = Y_[indx]
plt.plot(np.arange(Y.size), sortY_, 'r.', markersize=3, label="prediction")
plt.plot(np.arange(Y.size), sortY, 'b.', markersize=3, label="simulation")
plt.title("simulated versus predicted %s for L=%s"
          % (var_id_set[var_id], LL_p))
plt.xlabel("index of sorted prediction value")
plt.ylabel("%s (normalized)" % var_id_set[var_id])
plt.legend(loc='upper left', shadow=True, fontsize='medium')

plt.show()
