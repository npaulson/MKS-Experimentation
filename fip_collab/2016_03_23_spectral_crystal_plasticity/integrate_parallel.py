import numpy as np
import db_functions as fn
import gsh_cub_tri_L0_16 as gsh
import h5py
import time
import sys
import constants_old


tnum = np.int64(sys.argv[1])
C = constants_old.const()
filename = 'log_integrate_parallel_%s.txt' % str(tnum).zfill(5)

"""calculate basis function indices"""

# cmax: total number of permutations of basis functions
fn.WP(str(C['cmax']), filename)

# cmat is the matrix containing all permutations of basis function indices
cmat = np.unravel_index(np.arange(C['cmax']), C['N_tuple'])
cmat = np.array(cmat).T

"""deal with the parallelization of this operation specifically pick range
of indxmat to calculate"""

# n_ii: number integrations per job
n_ii = np.int64(np.ceil(np.float(C['cmax'])/C['integrate_njobs']))
fn.WP(str(n_ii), filename)

ii_stt = tnum*n_ii  # start index
ii_end = ii_stt + n_ii  # end index
if ii_end > C['cmax']:
    ii_end = C['cmax']

msg = "ii_stt = %s" % ii_stt
fn.WP(msg, filename)
msg = "ii_end = %s" % ii_end
fn.WP(msg, filename)

"""Open file for raw data
file order:
theta, phi1, Phi, phi2,
sigma'22, sigma'11, sigma'33, sigma'12, sigma'13, sigma'23,
total shear rate,
w12, w13, w23
"""

f_raw = h5py.File(C['combineread_output'], 'r')
var_set = f_raw.get('var_set')
sinphi = np.sin(var_set[:, 2])
n_y = 10

"""perform the integrations"""

coef_prt = np.zeros((ii_end-ii_stt, n_y), dtype='complex128')

f_X = h5py.File(C['combineXcalc_output'], 'r')

p_old = -1
q_old = -1

indxvec = gsh.gsh_basis_info()

for hh in xrange(n_y):

    c = 0
    Y = var_set[:, hh+4]

    for ii in xrange(ii_stt, ii_end):

        msg = str(ii)
        fn.WP(msg, filename)

        st = time.time()

        p, q = cmat[ii, :]

        """only load the basis if necessary!!!"""
        if p != p_old:
            basis_p = f_X.get('p_%s' % str(p).zfill(5))[...]
        if q != q_old:
            basis_q = f_X.get('q_%s' % str(q).zfill(5))[...]

        msg = "load time: %ss" % np.round(time.time()-st, 3)
        fn.WP(msg, filename)

        st = time.time()

        ep_set = np.squeeze(basis_p)*basis_q

        l = indxvec[p, 0]
        c_eul = (1./(2.*l+1.))*C['fzsz_eul']

        if q == 0:
            c_th = 1./C['L_th']
        else:
            c_th = 2./C['L_th']

        c_tot = c_eul*c_th*C['bsz_eul']*C['bsz_th']

        tmp = np.sum(Y*ep_set.conj()*sinphi)
        coef_prt[c, hh] = c_tot*tmp

        msg = "integration time: %ss" % np.round(time.time()-st, 3)
        fn.WP(msg, filename)

        p_old = p
        q_old = q

        c += 1

f_X.close()
f_raw.close()

f = h5py.File(C['integrate_output'] % str(tnum).zfill(5), 'w')
f.create_dataset('coef_prt', data=coef_prt)
f.close()

f_flag = open("flag%s" % str(tnum).zfill(5), 'w')
f_flag.close()
