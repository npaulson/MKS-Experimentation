import h5py
import numpy as np

"""

"""

# define the number of increments for angular variables:

inc = 1.  # degree increment for angular variables

n_th = np.int64(60/inc)  # number of theta samples for FZ
n_p1 = 360/inc  # number of phi1 samples for FZ
n_P = 90/inc  # number of Phi samples for FZ
n_p2 = 90/inc  # number of phi2 samples for FZ

n_par = np.int64(n_p1*n_P*n_p2)

f1 = h5py.File('var_extract_total.hdf5', 'w')
alldata = f1.create_dataset("var_set", (n_par*n_th, 14))

c = 0

for tt in xrange(0, n_th):

    print "Deformation Mode: %s deg" % str((tt+0.5)*inc)

    f2 = h5py.File('var_extract_%s.hdf5' % str(tt).zfill(2), 'r')

    ep_tmp = f2.get("var_set")
    print ep_tmp.shape

    stt = (c)*n_par
    print "start index: %s" % stt

    end = (c+1)*n_par
    print "end index: %s" % end

    alldata[stt:end, :] = ep_tmp

    f2.close()

    c += 1

print alldata.shape

f1.close()
