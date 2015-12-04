import numpy as np
import h5py
import time
import sys

fname = sys.argv

# initialize the variables of interest

inc = 5  # degree increment for angular variables

n_th_max = 120/inc  # number of theta samples in FOS
n_max = 360/inc  # number of phi1, Phi and phi2 samples in FOS
n_hlf = 180/inc  # half n_max

n_th = (60/inc)+1  # number of theta samples for FZ
n_p1 = 360/inc  # number of phi1 samples for FZ
n_P = (90/inc)+1  # number of Phi samples for FZ
n_p2 = 60/inc  # number of phi2 samples for FZ

# vector of the ranges of the first 4 dimensions in radians
Lset = np.array([(1./3.), 2., 2., 2.])*np.pi

# get data from the spectral coefficients file

# open the spectral coefficients file
f_db = h5py.File("final_db.hdf5", 'r')
# retrieve the list of indices
tmp = f_db.get("s_list")
s_list = tmp[...]
# retrieve associated list of fourier coefficients
tmp = f_db.get("f_list")
f_list = tmp[...]
# close the spectral coefficients file
f_db.close()

# get data from the validation data file

# open the error checking file
f_err = h5py.File(fname[1], 'r')
# retrieve the array of plastic strain values for various combination of input
# parameters
var_set = f_err.get("var_set")[...]
# close the error checking file
f_err.close()

# the columns of xi contain the position in degrees for each of the first four
# angular dimensions of interest
xi = var_set[5000:5001, :4]

# start timing the interpolation
st = time.time()

# perform the trigonometric interpolation
"""
* the slices of 's_list' and 'xi' have the shapes [c] and [n] for each
iteration of the loop below, where 'c' is the number of frequencies in the
database and 'n' is the number of interpolation points.
--> 'tmp' will start with the shape [n, c] (through broadcasting)
* 'tmp' is then transposed and an extra dimension is appended to the end.
--> 'tmp' has the shape [c, n, 1]
* in each loop 'tmp' is multiplied into 'TMP'
* after the loop we take 'f_list' with shape [c, p] and add an extra dimension
in the middle, where 'p' is the number of plastic strain values saved for each
combination of angular variables
--> 'f_list' has the shape [c, 1, p]
* Pvec is 'f_list' * 'TMP' (element-wise with broadcasting)
--> Pvec has the shape [c, n, p]
* to get the interpolation results sum 'Pvec' along the first dimension,
divide by 'Numel' and take only the real part of each number
--> 'results' has the shape [n, p]
"""

for ii in xrange(4):

    tmp = np.exp((2*np.pi*1j*s_list[:, ii]*xi[:, ii:ii+1])/Lset[ii])
    tmp = np.expand_dims(tmp.T, axis=2)

    if ii == 0:
        TMP = np.ones(tmp.shape, dtype='complex64')

    TMP *= tmp

Pvec = np.expand_dims(f_list, axis=1)*TMP

print Pvec.shape
print Pvec.nbytes/(1E9)

# the total number positions in the first 4 dimensions of the database
Numel = n_th_max*n_max**3

results = np.real(np.sum(Pvec, 0)/Numel)

# display the time required for interpolation
print "time to interpolate: %ss" % (time.time()-st)

# calculate the error for every location in 'results'
err = np.abs(results - var_set[5000:5001, 4:])

print "mean db value: %s" % np.mean(var_set[:, -1])
print "minimum db value: %s" % np.min(var_set[:, -1])
print "maximum db value: %s" % np.max(var_set[:, -1])
print "mean error: %s" % np.mean(err)
print "max error: %s" % np.max(err)
