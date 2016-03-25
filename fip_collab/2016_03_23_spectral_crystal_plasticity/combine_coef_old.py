import numpy as np
import db_functions as fn
import h5py
import constants_old


def combine():

    C = constants_old.const()
    filename = 'log_combine_coef.txt'

    """ Combine the results of the coefficient determination"""
    # coeff is the combined vector of coefficients as calculated by the
    # orthogonal regression
    coef = np.zeros((C['cmax'], 10), dtype='complex128')

    c = 0
    for tnum in xrange(C['integrate_njobs']):

        fn.WP(str(tnum), filename)

        # load partially filled coefficient arrays from each file
        f = h5py.File(C['integrate_output'] % str(tnum).zfill(5), 'r')
        coef_prt = f.get('coef_prt')[...]
        f.close()

        clen = coef_prt.shape[0]

        coef[c:c+clen, :] = coef_prt
        c += clen

    # save the coefficients file
    f = h5py.File(C['combinecoef_coef'], 'w')
    f.create_dataset('coef', data=coef)
    f.close()

    rrr = np.hstack([np.arange(coef.shape[0])[:, None],
                     coef[:, 0].real[:, None]])
    print np.round(rrr, 1)

if __name__ == '__main__':
    combine()
