import numpy as np
import itertools as it
import h5py
import time
import sys

tnum = np.int64(sys.argv[1])

N_L = 15  # number of GSH basis functions
N_p = 8  # number of complex exponential basis functions
N_q = 8  # number of Legendre basis functions
cmax = N_L*N_p*N_q  # total number of permutations of basis functions
print cmax

# iivec is vector of indices for all permutations of basis function indices
Ivec = np.arange(cmax)

# cmat is the matrix containing all permutations of basis function indices
cmat = np.unravel_index(np.arange(cmax), [N_L, N_p, N_q])
cmat = np.array(cmat).transpose()

# indxmat is the matrix containing all unique combinations of elements of iivec
tmp = it.combinations_with_replacement(Ivec, 2)
Imat = np.array(list(tmp))
ImatL = Imat.shape[0]
print ImatL

# pick range of indxmat to calculate
n_jobs = 100.  # number of jobs submitted to PACE
n_I = np.int64(np.ceil(np.float(ImatL)/n_jobs))  # number dot products per job
print n_I

I_stt = tnum*n_I  # start index
if (tnum+1)*n_I > ImatL:
    I_end = ImatL
else:
    I_end = (tnum+1)*n_I  # end index

print "I_stt = %s" % I_stt
print "I_end = %s" % I_end


# XtX is the matrix (X^T * X) in the normal equation for multiple
# linear regression
XtX = np.zeros((cmax, cmax), dtype='complex128')


for ii in Imat[I_stt:I_end, 0]:

    L, p, q = cmat[ii, :]

    set_id_ii = 'set_%s_%s_%s' % (L, p, q)

    f = h5py.File('pre_fourier_p%s_q%s.hdf5' % (p, q), 'r')
    ep_set_ii = f.get(set_id_ii)[:]
    f.close()

    for jj in Imat[I_stt:I_end, 1]:

        # print np.array([ii, jj])

        st = time.time()

        L, p, q = cmat[jj, :]

        set_id_jj = 'set_%s_%s_%s' % (L, p, q)

        f = h5py.File('pre_fourier_p%s_q%s.hdf5' % (p, q), 'r')
        ep_set_jj = f.get(set_id_jj)[:]
        f.close()

        # print "load time: %ss" % np.round(time.time()-st, 3)

        st = time.time()

        tmp = np.dot(ep_set_ii.conjugate(), ep_set_jj)

        del ep_set_jj

        # print "dot product time: %ss" % np.round(time.time()-st, 3)

        if ii == jj:
            XtX[ii, ii] = tmp
        else:
            XtX[ii, jj] = tmp
            XtX[jj, ii] = tmp

        del tmp

    del ep_set_ii

f = h5py.File('XtX%s.hdf5' % tnum, 'w')
f.create_dataset('XtX', data=XtX)
f.close()
