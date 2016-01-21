import numpy as np
import db_functions as fn
import h5py
import time


filename = 'log_test_regression.txt'

f = h5py.File('coeff_total.hdf5', 'r')
coeff = f.get('coeff')[...]
f.close()

f = h5py.File('var_extract_total.hdf5', 'r')
var_set = f.get('var_set')

theta = var_set[:, 0]

Y = var_set[:, 1]

f.close()

L_th = np.pi/3.

N_q = 16  # number of cosine bases to evaluate
cmax = N_q  # total number of permutations of basis functions

fn.WP(str(theta.size), filename)
fn.WP(str(cmax), filename)

cmat = np.arange(cmax)

st = time.time()

f = h5py.File('X_parts.hdf5', 'r')

vec = np.zeros(theta.size, dtype='complex128')

# for ii in xrange(10):
for ii in xrange(cmax):

    if np.mod(ii, 100) == 0:
        fn.WP(str(ii), filename)

    q = cmat[ii]
    basis_q = f.get('q_%s' % q)[...]

    ep_set = basis_q

    vec += coeff[ii]*ep_set

f.close()

Ttime = np.round(time.time()-st, 3)
msg = "total interpolation time: %ss" % Ttime
fn.WP(msg, filename)
msg = "interpolation time per point: %s" % (Ttime/theta.size)
fn.WP(msg, filename)

msg = str(vec.shape)
fn.WP(msg, filename)

error = np.abs(np.real(vec) - Y)

msg = "mean function value: %s" % np.mean(Y)
fn.WP(msg, filename)
msg = "std of function values: %s" % np.std(Y)
fn.WP(msg, filename)
msg = "min function value: %s" % np.min(Y)
fn.WP(msg, filename)

msg = "mean error: %s" % np.mean(error)
fn.WP(msg, filename)
msg = "std of error: %s" % np.std(error)
fn.WP(msg, filename)
msg = "min error: %s" % np.min(error)
fn.WP(msg, filename)

f = h5py.File('regression_results.hdf5', 'w')
# results = f.create_dataset("results", (Y.size, 8))

results = np.zeros((Y.size, 8), dtype='complex128')
results[:, 0] = theta
results[:, 1] = Y
results[:, 2] = vec
results[:, 3] = error
f.create_dataset('results', data=results)
f.close()
