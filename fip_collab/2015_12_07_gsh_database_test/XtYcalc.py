import numpy as np
import h5py
import time


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

filename = 'log_XtY.txt'

N_p = 8
cmax = N_p
cvec = np.arange(cmax)

st = time.time()

f = h5py.File('pre_fourier.hdf5', 'r')
var_set = f.get('var_set')
Y = var_set[:, 1]
f.close

XtY = np.zeros(cmax, dtype='complex128')

for ii in xrange(cmax):

    WP(str(ii), filename)

    p = cvec[ii, :]
    set_id_ii = 'set_%s' % p
    f = h5py.File('pre_fourier_p%s.hdf5' % p, 'r')
    ep_set_ii = f.get(set_id_ii)[...]
    f.close()

    XtY[ii] = np.dot(ep_set_ii.conj(), Y)

f = h5py.File('XtYtotal.hdf5', 'w')
f.create_dataset('XtY', data=XtY)
f.close()

WP("XtY prepared: %ss" % (np.round(time.time()-st, 3)), filename)
