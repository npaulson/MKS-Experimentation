import numpy as np
import db_functions as fn
import gsh_hex_tri_L0_16 as gsh
import h5py
import time
import sys
import constants


tnum = np.int64(sys.argv[1])
C = constants.const()
filename = 'log_integrate_parallel_%s.txt' % str(tnum)

""" Load Y vec """
f = h5py.File('var_extract_total.hdf5', 'r')
var_set = f.get('var_set')
sinphi = np.sin(var_set[:, 2])
Y = var_set[:, 5]
f.close

""" Calculate basis function indices """
# cmax: total number of permutations of basis functions
fn.WP(str(C['cmax']), filename)

# cmat is the matrix containing all permutations of basis function indices
cmat = np.unravel_index(np.arange(C['cmax']), C['N_tuple'])
cmat = np.array(cmat).T

""" Deal with the parallelization of this operation specifically pick range
of indxmat to calculate """
# n_ii: number dot products per job
n_ii = np.int64(np.ceil(np.float(C['cmax'])/C['n_jobs_integrate']))
fn.WP(str(n_ii), filename)

ii_stt = tnum*n_ii  # start index
if (tnum+1)*n_ii > C['cmax']:
    ii_end = C['cmax']
else:
    ii_end = (tnum+1)*n_ii  # end index

msg = "ii_stt = %s" % ii_stt
fn.WP(msg, filename)
msg = "ii_end = %s" % ii_end
fn.WP(msg, filename)

""" perform the orthogonal regressions """

coeff_prt = np.zeros(ii_end-ii_stt, dtype='complex128')
test_prt = np.zeros(Y.shape, dtype='complex128')

f = h5py.File('X_parts.hdf5', 'r')
c = 0
p_old = -1
q_old = -1
r_old = -1

indxvec = gsh.gsh_basis_info()

for ii in xrange(ii_stt, ii_end):

    msg = str(ii)
    fn.WP(msg, filename)

    st = time.time()

    p, q, r = cmat[ii, :]

    """only load the basis if necessary!!!"""
    if p != p_old:
        basis_p = f.get('p_%s' % p)[...]
    if r != r_old:
        basis_q = f.get('q_%s' % q)[...]
    if q != q_old:
        basis_r = f.get('r_%s' % r)[...]

    msg = "load time: %ss" % np.round(time.time()-st, 3)
    fn.WP(msg, filename)

    st = time.time()

    ep_set = np.squeeze(basis_p)*basis_q*basis_r

    l = indxvec[p, 0]
    c_eul = (1./(2.*l+1.))*C['fzsz_eul']

    if q == 0:
        c_th = 1./C['L_th']
    else:
        c_th = 2./C['L_th']

    if r == 0:
        c_en = 1./C['L_en']
    else:
        c_en = 2./C['L_en']

    c_tot = c_eul*c_th*c_en*C['bsz_eul']*C['bsz_th']*C['bsz_en']

    tmp = c_tot*np.sum(Y*ep_set.conj()*sinphi)

    test_prt += tmp*ep_set
    del ep_set

    coeff_prt[c] = tmp

    msg = "integration time: %ss" % np.round(time.time()-st, 3)
    fn.WP(msg, filename)

    p_old = p
    q_old = q
    r_old = r
    c += 1

f.close()

f = h5py.File('coeff_prt_%s.hdf5' % tnum, 'w')
f.create_dataset('coeff_prt', data=coeff_prt)
f.create_dataset('test_prt', data=test_prt)
f.close()
