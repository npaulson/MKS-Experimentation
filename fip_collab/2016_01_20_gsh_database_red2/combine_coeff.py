import numpy as np
import db_functions as fn
import h5py


filename = 'log_combine_coeff.txt'

""" Initialize important variables """
# pick range of indxmat to calculate
n_jobs = 5  # number of jobs submitted to PACE

N_p = 215  # number of GSH bases to evaluate
cmax = N_p  # total number of permutations of basis functions
print cmax

""" Combine the results of the parallelized integration """
# coeff is the combined vector of coefficients as calculated by the
# integration
coeff = np.zeros(cmax, dtype='complex128')

c = 0
for tnum in xrange(n_jobs):

    fn.WP(str(tnum), filename)

    # load partially filled XtX arrays from each file
    f = h5py.File('coeff_prt_%s.hdf5' % tnum, 'r')
    coeff_prt = f.get('coeff_prt')

    for ii in xrange(coeff_prt.shape[0]):

        coeff[c] = coeff_prt[ii]
        c += 1

f = h5py.File('coeff_total.hdf5', 'w')
f.create_dataset('coeff', data=coeff)
f.close()
