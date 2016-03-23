import numpy as np
import db_functions as fn
import h5py
import time
import constants


def combine():

    C = constants.const()
    filename = 'log_combine_coef.txt'

    st = time.time()  # start timing

    f = h5py.File(C['combineread_output'], 'r')
    var_set = f.get('var_set')

    theta = var_set[:, 0]

    X = np.zeros((theta.size, 3), dtype='float64')
    X[:, 0] = var_set[:, 1]  # phi1
    X[:, 1] = var_set[:, 2]  # phi
    X[:, 2] = var_set[:, 3]  # phi2

    et_norm = var_set[:, 4]
    Y = var_set[:, 5]

    f.close()

    """ Combine the results of the coefficient determination and
    calculate the value of the test function """
    # coeff is the combined vector of coefficients as calculated by the
    # orthogonal regression
    coef = np.zeros(C['cmax'], dtype='complex128')
    Y_ = np.zeros(Y.shape, dtype='complex128')

    c = 0
    for tnum in xrange(C['integrate_njobs']):

        fn.WP(str(tnum), filename)

        # load partially filled coefficient arrays from each file
        f = h5py.File('coef_prt_%s.hdf5' % str(tnum).zfill(5), 'r')
        coef_prt = f.get('coef_prt')[...]
        test_prt = f.get('test_prt')[...]
        f.close()

        Y_ += test_prt  # add pre-calculated portions to function prediction

        # insert pre-calculated coefficients to final list
        for ii in xrange(coef_prt.shape[0]):

            coef[c] = coef_prt[ii]
            c += 1

    # save the coefficients file
    f = h5py.File(C['combinecoef_coef'], 'w')
    f.create_dataset('coef', data=coef)
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

    f = h5py.File(C['combinecoef_results'], 'w')

    results = np.zeros((Y.size, 8), dtype='complex128')
    results[:, 0] = theta
    results[:, 1:4] = X
    results[:, 4] = et_norm
    results[:, 5] = Y
    results[:, 6] = Y_
    results[:, 7] = error
    f.create_dataset('results', data=results)
    f.close()


if __name__ == '__main__':
    combine()
