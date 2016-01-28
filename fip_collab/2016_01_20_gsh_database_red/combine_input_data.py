import h5py

"""

"""

# define the number of increments for angular variables:

inc = 6  # degree increment for angular variables

n_th = 60/inc  # number of theta samples for FZ
n_p1 = 360/inc  # number of phi1 samples for FZ
n_P = 90/inc  # number of Phi samples for FZ
n_p2 = 60/inc  # number of phi2 samples for FZ

n_par = n_p1*n_P*n_p2

f1 = h5py.File('var_extract_total.hdf5', 'w')
alldata = f1.create_dataset("var_set", (n_par*n_th, 5))

c = 0

for tt in xrange(0, n_th):

    print "Deformation Mode: %s deg" % (tt*inc)

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
