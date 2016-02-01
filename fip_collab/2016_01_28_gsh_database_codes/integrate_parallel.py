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
a = 0.00485  # start for en range
b = 0.00905  # end for en range
N_p = 500  # number of GSH bases to evaluate
N_q = 40  # number of cosine bases to evaluate for theta
N_r = 14  # number of cosine bases to evaluate for en

n_jobs = 50.  # number of jobs submitted to cluster

inc = 3

inc_eul = 5.  # degree increment for angular variables
inc_th = 1.5

n_th = 60/inc_th  # number of theta samples for FZ
n_p1 = 360/inc_eul  # number of phi1 samples for FZ
n_P = 90/inc_eul  # number of Phi samples for FZ
n_p2 = 60/inc_eul  # number of phi2 samples for FZ
n_en = 14  # number of et samples for FZ

L_th = np.pi/3.
L_en = b-a

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

bsz_eul = ((np.pi**3)/3)/n_eul
bsz_th = L_th/n_th
bsz_en = L_en/n_en

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
    c_eul = (1./(2.*l+1.))*(3./(2.*np.pi**2))

    if q == 0:
        c_th = 1./L_th
    else:
        c_th = 2./L_th

    if r == 0:
        c_en = 1./L_en
    else:
        c_en = 2./L_en

    c_tot = c_eul*c_th*c_en*bsz_eul*bsz_th*bsz_en

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
