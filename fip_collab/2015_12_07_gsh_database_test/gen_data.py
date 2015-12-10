import numpy as np
import h5py


def testfunc(x):
    # return -.75*np.cos(x)+.25*np.cos(4*x)
    return np.cos(0.5*x)**10


L = np.pi

N = 100  # number of samples
xsamp = np.linspace(0, L, N)  # x samples
ysamp = testfunc(xsamp)  # function value

var_set = np.zeros((N, 2))
var_set[:, 0] = xsamp
var_set[:, 1] = ysamp


f = h5py.File('pre_fourier.hdf5', 'a')
f.create_dataset('var_set', data=var_set)
f.close()
