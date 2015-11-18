import h5py
import numpy as np

"""

"""

# define the number of increments for angular variables:

n_p1 = 11  # number of phi1 samples
n_P = 11  # number of Phi samples
n_p2 = 11  # number of phi2 samples
n_en = 100  # number of en samples

n_par = n_p1*n_P*n_p2*n_en

f1 = h5py.File('test_fourier.hdf5', 'w')
alldata = f1.create_dataset("ep_set", (n_par*n_th, 6))

for tt in xrange(n_th):

    print tt

    # create file for pre-database outputs
    f2 = h5py.File('test_extract_%s.hdf5' % str(tt+1).zfill(2), 'r')

    ep_tmp = f2.get("ep_set")

    stt = (tt)*n_par
    print stt

    end = (tt+1)*n_par
    print end

    alldata[stt:end, :] = ep_tmp

    f2.close()

print alldata.shape
print alldata.nbytes/(1E9)

f1.close()
