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

msg = "rank(XtX): %s" % np.linalg.matrix_rank(XtX)
fn.WP(msg, filename)

ind_vec = fn.independent_columns(XtX)
msg = "independent columns of X: %s" % str(ind_vec)
fn.WP(msg, filename)

# XtX_plus: the psudeo-inverse of XtX
XtX_plus = np.linalg.pinv(XtX)
# coeff: vector of least squares coefficients for the selected basis functions.
# This is calculated with the pseudo-inverse above
coeff = np.dot(XtX_plus, XtY)

f = h5py.File('reg_coeff.hdf5', 'w')
f.create_dataset('coeff', data=coeff)
f.close()
