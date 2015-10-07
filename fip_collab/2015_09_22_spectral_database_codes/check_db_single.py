import numpy as np
import h5py
import time
import sys


fnum = sys.argv

inc = 3  # degree increment for angular variables

n_th_max = 120/inc  # number of theta samples in FOS
n_max = 360/inc  # number of phi1, Phi and phi2 samples in FOS

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

# open the error checking file
err_check = "test_extract_%s.hdf5" % str(fnum[1]).zfill(2)
f_err = h5py.File(err_check, 'r')

# retrieve the array of plastic strain values for various combination of input
# parameters
tmp = f_err.get("ep_set")
ep_set = tmp[...]

# ep_set = f_err.get("ep_set")[...]

tmp = f_err.get("euler_set")
euler_set = tmp[...]

# close the error checking file
f_err.close()

sh = ep_set.shape[:-1]
sz = np.prod(sh)

ep_set = ep_set.reshape([sz, 11])

print ep_set.shape
print euler_set.shape

# the columns of xi contain the position in degrees for each of the first four
# angular dimensions of interest
xi_set = np.ones([sz, 4])*(20.+np.int8(fnum[1])-1.)*(np.pi/180.)
# the deformation angle is constant, in this case fnum[1]
xi_set[:, 1:] = euler_set

print xi_set.shape

# vector of the ranges of the first 4 dimensions in radians
Lset = np.array([120., 360., 360., 360.])*(np.pi/180.)

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
* in each loop the product 'tmp' and the product of the previous 'tmp's is
taken and put into 'TMP'
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

# create a results file
f_res = h5py.File('results_%s.hdf5' % str(fnum[1]).zfill(2), 'w')
res_set = f_res.create_dataset("results", (sz, 11))

# the total number positions in the first 4 dimensions of the database
Numel = n_th_max*n_max**3

err_old = 0.

for jj in xrange(sz):

    xi = xi_set[jj, np.newaxis, :]

    for ii in xrange(4):

        tmp = np.exp((2*np.pi*1j*s_list[:, ii]*xi[:, ii:ii+1])/Lset[ii])

        tmp = np.expand_dims(tmp.T, axis=2)

        if ii == 0:
            TMP = np.ones(tmp.shape, dtype='complex64')

        TMP *= tmp

    Pvec = np.expand_dims(f_list, axis=1)*TMP

    # print Pvec.shape
    # print Pvec.nbytes

    results = np.real(np.sum(Pvec, 0)/Numel)

    # # display the time required for interpolation
    # print "time to interpolate: %ss" % (time.time()-st)

    # calculate the error for every location in 'results'
    err = np.abs((results - ep_set[jj, :]) / 0.0096) * 100

    res_set[jj, :] = err

    if np.sum(err) > np.sum(err_old):
        err_old = err
        print jj
        print np.max(err)

f_res.close()
