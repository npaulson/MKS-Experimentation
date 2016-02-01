import numpy as np
import db_functions as fn
import h5py
import time


filename = 'log_combine_coeff.txt'

""" Initialize important variables """
a = 0.00485  # start for en range
b = 0.00905  # end for en range
N_p = 500  # number of GSH bases to evaluate
N_q = 40  # number of cosine bases to evaluate for theta
N_r = 14  # number of cosine bases to evaluate for en

# pick range of indxmat to calculate
n_jobs = 50  # number of jobs submitted to PACE

st = time.time()  # start timing

f = h5py.File('var_extract_total.hdf5', 'r')
var_set = f.get('var_set')

theta = var_set[:, 0]

X = np.zeros((theta.size, 3), dtype='float64')
X[:, 0] = var_set[:, 1]  # phi1
X[:, 1] = var_set[:, 2]  # phi
X[:, 2] = var_set[:, 3]  # phi2

et_norm = var_set[:, 4]
Y = var_set[:, 5]

f.close()

cmax = N_p*N_q*N_r  # total number of permutations of basis functions
print cmax

""" Combine the results of the coefficient determination and
calculate the value of the test function """
# coeff is the combined vector of coefficients as calculated by the
# orthogonal regression
coeff = np.zeros(cmax, dtype='complex128')
Y_ = np.zeros(Y.shape, dtype='complex128')

c = 0
for tnum in xrange(n_jobs):

    fn.WP(str(tnum), filename)

    # load partially filled coefficient arrays from each file
    f = h5py.File('coeff_prt_%s.hdf5' % tnum, 'r')
    coeff_prt = f.get('coeff_prt')
    test_prt = f.get('test_prt')
    f.close()

    Y_ += test_prt  # add pre-calculated portions to function prediction

    # insert pre-calculated coefficients to final list
    for ii in xrange(coeff_prt.shape[0]):

        coeff[c] = coeff_prt[ii]
        c += 1

# save the coefficients file
f = h5py.File('coeff_total.hdf5', 'w')
f.create_dataset('coeff', data=coeff)
f.close()

Ttime = np.round(time.time()-st, 3)
msg = "total interpolation time: %ss" % Ttime
fn.WP(msg, filename)

msg = str(Y_.shape)
fn.WP(msg, filename)

error = np.abs(np.real(Y_) - Y)

msg = "min function value: %s" % Y.min()
fn.WP(msg, filename)
msg = "mean function values: %s" % Y.mean()
fn.WP(msg, filename)
msg = "max function value: %s" % Y.max()
fn.WP(msg, filename)

msg = "mean prediction value: %s" % np.real(Y_).mean()
fn.WP(msg, filename)

msg = "mean error: %s" % error.mean()
fn.WP(msg, filename)
msg = "std of error: %s" % error.std()
fn.WP(msg, filename)
msg = "max error: %s" % error.max()
fn.WP(msg, filename)

f = h5py.File('final_results.hdf5', 'w')
# results = f.create_dataset("results", (Y.size, 8))

results = np.zeros((Y.size, 8), dtype='complex128')
results[:, 0] = theta
results[:, 1:4] = X
results[:, 4] = et_norm
results[:, 5] = Y
results[:, 6] = Y_
results[:, 7] = error
f.create_dataset('results', data=results)
f.close()
