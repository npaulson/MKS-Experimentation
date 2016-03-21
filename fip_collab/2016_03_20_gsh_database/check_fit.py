import numpy as np
import db_functions as fn
import gsh_hex_tri_L0_16 as gsh
import h5py
import time
import sys


thr = np.float64(sys.argv[1])  # threshold on coefs w/rt maximum magnitude coef

indxvec = gsh.gsh_basis_info()

a = 0.00485  # start for en range
b = 0.00905  # end for en range

# N_p: number of GSH bases to evaluate
# N_p = np.sum(indxvec[:, 0] <= LL_p)
N_p = 500
N_q = 40  # number of cosine bases to evaluate for theta
N_r = 14  # number of cosine bases to evaluate for en

L_th = np.pi/3.
L_en = b-a

filename = 'log_final_results9261.txt'

f = h5py.File('coeff_total.hdf5', 'r')
coeff = f.get('coeff')[...]
f.close()

f = h5py.File('var_extract_check.hdf5', 'r')
var_set = f.get('var_set')

N_pts = var_set.shape[0]

theta = var_set[:, 0]

X = np.zeros((N_pts, 3), dtype='float64')
X[:, 0] = var_set[:, 1]  # phi1
X[:, 1] = var_set[:, 2]  # phi
X[:, 2] = var_set[:, 3]  # phi2

et_norm = var_set[:, 4]
Y = var_set[:, 5]

f.close()

"""Select the desired set of coefficients"""

cmax = N_p*N_q*N_r  # total number of permutations of basis functions

fn.WP(str(cmax), filename)

cmat = np.unravel_index(np.arange(cmax), [N_p, N_q, N_r])
cmat = np.array(cmat).T

cuttoff = thr*np.abs(coeff).max()
indxvec = np.arange(cmax)[np.abs(coeff) > cuttoff]

N_coef = indxvec.size
pct_coef = 100.*N_coef/cmax
fn.WP("number of coefficients retained: %s" % N_coef, filename)
fn.WP("percentage of coefficients retained %s%%"
      % np.round(pct_coef, 4), filename)

"""Evaluate the parts of the basis function individually"""

st = time.time()

p_U = np.unique(cmat[indxvec, 0])
q_U = np.unique(cmat[indxvec, 1])
r_U = np.unique(cmat[indxvec, 2])

fn.WP("number of p basis functions used: %s" % p_U.size, filename)
fn.WP("number of q basis functions used: %s" % q_U.size, filename)
fn.WP("number of r basis functions used: %s" % r_U.size, filename)

all_basis_p = np.zeros([N_pts, N_p], dtype='complex128')
for p in p_U:
    all_basis_p[:, p] = np.squeeze(gsh.gsh_eval(X, [p]))

all_basis_q = np.zeros([N_pts, N_q], dtype='complex128')
for q in q_U:
    all_basis_q[:, q] = np.cos(q*np.pi*theta/L_th)

all_basis_r = np.zeros([N_pts, N_r], dtype='complex128')
for r in r_U:
    all_basis_r[:, r] = np.cos(r*np.pi*(et_norm-a)/L_en)

"""Perform the prediction"""

Y_ = np.zeros(theta.size, dtype='complex128')

for ii in indxvec:

    p, q, r = cmat[ii, :]
    basis_p = all_basis_p[:, p]
    basis_q = all_basis_q[:, q]
    basis_r = all_basis_r[:, r]

    ep_set = basis_p*basis_q*basis_r

    Y_ += coeff[ii]*ep_set

Ttime = np.round(time.time()-st, 3)
msg = "total interpolation time: %ss" % Ttime
fn.WP(msg, filename)
msg = "interpolation time per point: %s" % (Ttime/theta.size)
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

"""look at the prediction for a random angle set"""
randindx = np.int64(np.random.rand()*N_pts)
msg = "random predicted ep: %s" % Y_[randindx].real
fn.WP(msg, filename)
msg = "SP-CP ep: %s" % Y[randindx]
fn.WP(msg, filename)

f = h5py.File('final_results9261.hdf5', 'w')
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
