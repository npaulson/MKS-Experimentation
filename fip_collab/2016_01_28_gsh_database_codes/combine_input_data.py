import h5py
import numpy as np

"""

"""

# define the number of increments for angular variables:

inc_eul = 5  # degree increment for angular variables
inc_th = 1.5

n_th = np.int64(60/inc_th)  # number of theta samples for FZ
n_p1 = 360/inc_eul  # number of phi1 samples for FZ
n_P = 90/inc_eul  # number of Phi samples for FZ
n_p2 = 60/inc_eul  # number of phi2 samples for FZ
n_en = 14  # number of et samples for FZ

n_par = n_p1*n_P*n_p2*n_en

f1 = h5py.File('var_extract_total.hdf5', 'w')
alldata = f1.create_dataset("var_set", (n_par*n_th, 6))

c = 0

for tt in xrange(0, n_th):

    print "Deformation Mode: %s deg" % str((tt+0.5)*inc_th)

    # create file for pre-database outputs
    f2 = h5py.File('var_extract_%s.hdf5' % str(tt+1).zfill(2), 'r')

    ep_tmp = f2.get("var_set")

    stt = (c)*n_par
    print "start index: %s" % stt

    end = (c+1)*n_par
    print "end index: %s" % end

    alldata[stt:end, :] = ep_tmp

    f2.close()

    c += 1

print alldata.shape

f1.close()
