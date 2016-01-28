import numpy as np
# import itertools as it
import db_functions as fn
import gsh_hex_tri_L0_16 as gsh
import h5py
import time
import sys


tnum = np.int64(sys.argv[1])

filename = 'log_integrate_parallel_%s.txt' % str(tnum)

""" Load Y vec """
f = h5py.File('var_extract_total.hdf5', 'r')
var_set = f.get('var_set')
sinphi = np.sin(var_set[:, 2])
Y = var_set[:, 5]
f.close

""" Initialize important variables """
N_p = 215  # number of GSH bases to evaluate
N_q = 9  # number of cosine bases to evaluate
N_r = 10  # number of legendre bases to evaluate

n_jobs = 50.  # number of jobs submitted to cluster

inc = 6

n_th = 60/inc  # number of theta samples for FZ
n_p1 = 360/inc  # number of phi1 samples for FZ
n_P = 90/inc  # number of Phi samples for FZ
n_p2 = 60/inc  # number of phi2 samples for FZ
n_en = 12

a = 0.0050
b = 0.0085

L_th = np.pi/3.

sub2rad = inc*np.pi/180.

n_eul = n_p1*n_P*n_p2


""" Calculate basis function indices """
cmax = N_p*N_q*N_r  # total number of permutations of basis functions
fn.WP(str(cmax), filename)

# cmat is the matrix containing all permutations of basis function indices
cmat = np.unravel_index(np.arange(cmax), [N_p, N_q, N_r])
cmat = np.array(cmat).T

""" Deal with the parallelization of this operation specifically pick range
of indxmat to calculate """
n_ii = np.int64(np.ceil(np.float(cmax)/n_jobs))  # number dot products per job
fn.WP(str(n_ii), filename)

ii_stt = tnum*n_ii  # start index
if (tnum+1)*n_ii > cmax:
    ii_end = cmax
else:
    ii_end = (tnum+1)*n_ii  # end index

msg = "ii_stt = %s" % ii_stt
fn.WP(msg, filename)
msg = "ii_end = %s" % ii_end
fn.WP(msg, filename)

""" perform the orthogonal regressions """

coeff_prt = np.zeros(ii_end-ii_stt, dtype='complex128')

f = h5py.File('X_parts.hdf5', 'r')
c = 0

indxvec = gsh.gsh_basis_info()

bsz_gsh = ((np.pi**3)/3)/n_eul
bsz_cos = L_th/n_th
bsz_leg = (b-a)/n_en

for ii in xrange(ii_stt, ii_end):

    msg = str(ii)
    fn.WP(msg, filename)

    st = time.time()

    p, q, r = cmat[ii, :]
    basis_p = f.get('p_%s' % p)[...]
    basis_q = f.get('q_%s' % q)[...]
    basis_r = f.get('r_%s' % r)[...]

    ep_set = np.squeeze(basis_p)*basis_q*basis_r

    msg = "load time: %ss" % np.round(time.time()-st, 3)
    fn.WP(msg, filename)

    st = time.time()

    l = indxvec[p, 0]
    c_gsh = (1./(2.*l+1.))*(3./(2.*np.pi**2))

    if q == 0:
        c_cos = 1./L_th
    else:
        c_cos = 2./L_th

    c_leg = 2*r+1

    c_tot = c_gsh*c_cos*c_leg*bsz_gsh*bsz_cos*bsz_leg

    tmp = c_tot*np.sum(Y*ep_set.conj()*sinphi)

    del ep_set

    coeff_prt[c] = tmp

    msg = "regression time: %ss" % np.round(time.time()-st, 3)
    fn.WP(msg, filename)

    c += 1

f.close()

f = h5py.File('coeff_prt_%s.hdf5' % tnum, 'w')
f.create_dataset('coeff_prt', data=coeff_prt)
f.close()
