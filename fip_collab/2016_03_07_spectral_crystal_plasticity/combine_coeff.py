import numpy as np
import db_functions as fn
import gsh_cub_tri_L0_16 as gsh
import h5py


filename = 'log_combine_coeff.txt'

""" Initialize important variables """
LL_p = 16  # gsh truncation level
indxvec = gsh.gsh_basis_info()
# N_p: number of GSH bases to evaluate
N_p = np.sum(indxvec[:, 0] <= LL_p)

N_q = 60  # number of cosine bases to evaluate for theta

# pick range of indxmat to calculate
n_jobs = 400  # number of jobs submitted to PACE

cmax = N_p*N_q  # total number of permutations of basis functions
print cmax

""" Combine the results of the coefficient determination and
calculate the value of the test function """
# coeff is the combined vector of coefficients as calculated by the
# orthogonal regression
coeff = np.zeros((cmax, 10), dtype='complex128')

c = 0
for tnum in xrange(n_jobs):

    fn.WP(str(tnum), filename)

    # load partially filled coefficient arrays from each file
    f = h5py.File('coeff_prt_%s.hdf5' % tnum, 'r')
    coeff_prt = f.get('coeff_prt')[...]
    f.close()

    # insert pre-calculated coefficients to final list
    for ii in xrange(coeff_prt.shape[0]):

        coeff[c, :] = coeff_prt[ii, :]
        c += 1

# save the coefficients file
f = h5py.File('coeff_total.hdf5', 'w')
f.create_dataset('coeff', data=coeff)
f.close()
