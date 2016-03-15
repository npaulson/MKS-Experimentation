import numpy as np
# import itertools as it
import db_functions as fn
import gsh_cub_tri_L0_16 as gsh
import h5py
import time
import sys


tnum = np.int64(sys.argv[1])

filename = 'log_integrate_parallel_%s.txt' % str(tnum)

""" Initialize important variables """
a = 0.00485  # start for en range
b = 0.00905  # end for en range

LL_p = 16  # gsh truncation level
indxvec = gsh.gsh_basis_info()

# N_p: number of GSH bases to evaluate
N_p = np.sum(indxvec[:, 0] <= LL_p)
N_q = 60  # number of cosine bases to evaluate for theta

n_jobs = 400.  # number of jobs submitted to cluster

thetamax = 60
phi1max = 360
phimax = 90
phi2max = 90

inc_eul = 5.  # degree increment for euler angles
inc_th = 1.5  # degree increment for theta angle

n_th = thetamax/inc_th  # number of theta samples for FZ
n_p1 = phi1max/inc_eul  # number of phi1 samples for FZ
n_P = phimax/inc_eul  # number of Phi samples for FZ
n_p2 = phi2max/inc_eul  # number of phi2 samples for FZ

L_th = np.pi/3.

n_eul = n_p1*n_P*n_p2

""" Calculate basis function indices """
cmax = N_p*N_q  # total number of permutations of basis functions
fn.WP(str(cmax), filename)

# cmat is the matrix containing all permutations of basis function indices
cmat = np.unravel_index(np.arange(cmax), [N_p, N_q])
cmat = np.array(cmat).T

""" Deal with the parallelization of this operation specifically pick range
of indxmat to calculate """
n_ii = np.int64(np.ceil(np.float(cmax)/n_jobs))  # number integrations per job
fn.WP(str(n_ii), filename)

ii_stt = tnum*n_ii  # start index
ii_end = ii_stt + n_ii  # end index
if ii_end > cmax:
    ii_end = cmax

msg = "ii_stt = %s" % ii_stt
fn.WP(msg, filename)
msg = "ii_end = %s" % ii_end
fn.WP(msg, filename)

""" perform the orthogonal regressions """

c = 0

indxvec = gsh.gsh_basis_info()

# domain_eul_sz is the integration domain in radians
domain_eul_sz = phi1max*phimax*phi2max*(np.pi/180.)**3
# full_eul_sz is the size of euler space in radians
full_eul_sz = (2*np.pi)*(np.pi)*(2*np.pi)

eul_frac = domain_eul_sz/full_eul_sz

fzsz_eul = 1./(eul_frac*8.*np.pi**2)
bsz_eul = domain_eul_sz/n_eul

bsz_th = L_th/n_th


"""Open file for raw data
file order:
theta, phi1, Phi, phi2,
sigma'22, sigma'11, sigma'33, sigma'12, sigma'13, sigma'23,
total shear rate,
w12, w13, w23
"""

f_raw = h5py.File('var_extract_total.hdf5', 'r')
var_set = f_raw.get('var_set')
sinphi = np.sin(var_set[:, 2])
Yset = var_set[:, 4:]
n_y = Yset.shape[1]

f_raw.close()

f_X = h5py.File('X_parts.hdf5', 'r')

coeff_prt = np.zeros((ii_end-ii_stt, n_y), dtype='complex128')

for ii in xrange(ii_stt, ii_end):

    msg = str(ii)
    fn.WP(msg, filename)

    st = time.time()

    p, q = cmat[ii, :]
    basis_p = f_X.get('p_%s' % p)[...]
    basis_q = f_X.get('q_%s' % q)[...]

    ep_set = np.squeeze(basis_p)*basis_q

    msg = "load time: %ss" % np.round(time.time()-st, 3)
    fn.WP(msg, filename)

    st = time.time()

    l = indxvec[p, 0]
    c_eul = (1./(2.*l+1.))*fzsz_eul

    if q == 0:
        c_th = 1./L_th
    else:
        c_th = 2./L_th

    c_tot = c_eul*c_th*bsz_eul*bsz_th

    for jj in xrange(n_y):

        tmp = c_tot*np.sum(Yset[:, jj]*ep_set.conj()*sinphi)
        coeff_prt[c] = tmp

    msg = "integration time: %ss" % np.round(time.time()-st, 3)
    fn.WP(msg, filename)

    c += 1

f_X.close()  # close the evaluated basis function file

"""save this section of the coefficients"""
f_coef = h5py.File('coeff_prt_%s.hdf5' % tnum, 'w')
f_coef.create_dataset('coeff_prt', data=coeff_prt)
f_coef.close()
