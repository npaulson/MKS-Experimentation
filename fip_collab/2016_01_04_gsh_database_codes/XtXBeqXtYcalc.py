import numpy as np
import h5py
import db_functions as fn


filename = 'log_XtXBeqXtYcalc.txt'

f = h5py.File('XtXtotal.hdf5', 'r')
XtX = f.get('XtX')[...]
f.close()

f = h5py.File('XtYtotal.hdf5', 'r')
XtY = f.get('XtY')[...]
f.close()

cmax = np.XtX.shape[0]

# coeff: vector of least squares coefficients for the selected basis functions.
coeff = np.zeros(cmax, dtype='complex128')

for ii in xrange(cmax):
	coeff[ii] = XtY[ii]/XtX[ii]

f = h5py.File('reg_coeff.hdf5', 'w')
f.create_dataset('coeff', data=coeff)
f.close()
