import numpy as np
import db_functions as fn
import gsh_cub_tri_L0_24 as gsh
import constants
import h5py
import time


def evalf(theta, euler, var_id, thr, LL_p):

    filename = "log_eval.txt"

    C = constants.const()

    f = h5py.File('coef.hdf5', 'r')
    coef = f.get('coef')[:, var_id]
    f.close()

    basis_info = gsh.gsh_basis_info()
    N_p_tmp = np.sum(basis_info[:, 0] <= LL_p)  # number of GSH bases to evaluate

    N_pts = theta.size

    """Select the desired set of coefficients"""

    msg = "cmax: %s" % C['cmax']
    fn.WP(msg, filename)

    cmat = np.unravel_index(np.arange(C['cmax']), C['N_tuple'])
    cmat = np.array(cmat).T

    cuttoff = thr*np.abs(coef).max()
    print "cutoff: %s" % cuttoff
    cuttoffvec = (np.abs(coef) > cuttoff) * \
                 (np.arange(C['cmax']) < N_p_tmp*C['N_q'])
    print "cuttoffvec.shape: %s" % str(cuttoffvec.shape)
    indxvec = np.arange(C['cmax'])[cuttoffvec]

    N_coef = indxvec.size
    pct_coef = 100.*N_coef/C['cmax']
    fn.WP("number of coefficients retained: %s" % N_coef, filename)
    fn.WP("percentage of coefficients retained %s%%"
          % np.round(pct_coef, 4), filename)

    """Evaluate the parts of the basis function individually"""

    st = time.time()

    p_U = np.unique(cmat[indxvec, 0])
    q_U = np.unique(cmat[indxvec, 1])

    all_basis_p = np.zeros([N_pts, C['N_p']], dtype='complex128')
    for p in p_U:
        all_basis_p[:, p] = np.squeeze(gsh.gsh_eval(euler, [p]))

    fn.WP("number of p basis functions used: %s" % p_U.size, filename)

    all_basis_q = np.zeros([N_pts, C['N_q']], dtype='complex128')
    for q in q_U:
        all_basis_q[:, q] = np.cos(q*np.pi*theta/C['L_th'])

    fn.WP("number of q basis functions used: %s" % q_U.size, filename)

    """Perform the prediction"""

    Y_ = np.zeros(theta.size, dtype='complex128')

    for ii in indxvec:

        p, q = cmat[ii, :]
        basis_p = all_basis_p[:, p]
        basis_q = all_basis_q[:, q]

        ep_set = basis_p*basis_q

        Y_ += coef[ii]*ep_set

        if np.mod(ii, 1000) == 0:
            msg = "evaluation complete for coefficient" +\
                  " %s out of %s" % (ii, N_coef)
            fn.WP(msg, filename)

    Ttime = np.round(time.time()-st, 3)
    msg = "total interpolation time: %ss" % Ttime
    fn.WP(msg, filename)
    msg = "interpolation time per point: %s" % (Ttime/theta.size)
    fn.WP(msg, filename)

    return Y_


if __name__ == '__main__':
    theta = 30*(np.pi/180.)
    euler = np.array([[30, 30, 30]])*(np.pi/180.)
    thr = 1e-5
    Y_ = evalf(theta, euler, thr)
    print Y_
