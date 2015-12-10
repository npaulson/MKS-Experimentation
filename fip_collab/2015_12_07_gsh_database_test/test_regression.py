import numpy as np
import numpy.polynomial.legendre as leg
import matplotlib.pyplot as plt
import h5py


def WP(msg, filename):
    """
    Summary:
        This function takes an input message and a filename, and appends that
        message to the file. This function also prints the message
    Inputs:
        msg (string): the message to write and print.
        filename (string): the full name of the file to append to.
    Outputs:
        both prints the message and writes the message to the specified file
    """
    fil = open(filename, 'a')
    print msg
    fil.write(msg)
    fil.write('\n')
    fil.close()

filename = 'log_test_regression.txt'

f = h5py.File('reg_coeff.hdf5', 'r')
coeff = f.get('coeff')[...]
f.close()

f = h5py.File('pre_fourier.hdf5', 'r')
var_set = f.get('var_set')

et_norm = var_set[:, 0]
Y = var_set[:, 1]

f.close()

N_p = 8
cmax = N_p

WP(str(et_norm.size), filename)
WP(str(cmax), filename)

cmat = np.arange(cmax)

vec = np.zeros(et_norm.size, dtype='complex128')

for ii in xrange(cmax):

    if np.mod(ii, 10) == 0:
        WP(str(ii), filename)

    p = cmat[ii]

    p_vec = np.zeros(p+1)
    p_vec[p] = 1

    tmp = np.zeros(et_norm.size, dtype='complex128')

    tmp[:] = leg.legval(et_norm, p_vec)
    tmp[:] *= coeff[ii]

    vec[:] += tmp

msg = str(vec.shape)
WP(msg, filename)

error = np.abs(np.real(vec) - Y)

msg = "mean error: %s" % np.mean(error)
WP(msg, filename)
msg = "std of error: %s" % np.std(error)
WP(msg, filename)
msg = "min error: %s" % np.min(error)
WP(msg, filename)

plt.figure(1)
plt.plot(et_norm, vec, 'r-')
plt.plot(et_norm, Y, 'b-')
plt.show()
