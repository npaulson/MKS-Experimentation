import numpy as np
# import matplotlib.pyplot as plt
import euler_func as ef
import h5py


"""
check whether the database exhibits hexagonal-triclinic crystal
symmetry

first find 12 symmetric orientations in triclinic FZ
(0<=phi1<2*pi, 0<=Phi<=pi, 0<=phi2<2*pi)

for each deformation mode sample (theta), check if the value of
interest is the same for all symmetric orientations
"""

symhex = ef.symhex()

inc = 5  # degree increment for angular variables

n_th_max = 120/inc  # number of theta samples in FOS
n_max = 360/inc  # number of phi1, Phi and phi2 samples in FOS
n_hlf = 180/inc  # half n_max

n_th = (60/inc)+1  # number of theta samples for FZ
n_p1 = 360/inc  # number of phi1 samples for FZ
n_P = (90/inc)+1  # number of Phi samples for FZ
n_p2 = 60/inc  # number of phi2 samples for FZ

print "angle space shape"
print np.array([n_th, n_p1, n_P, n_p2])

# only look at last in series for value of interest
db = np.load("pre_fft.npy")[:n_th, ..., -1]
print "db shape"
print db.shape

# n_FZ: total number of sampled orientations in FZ
n_FZ = n_p1*n_P*n_p2
# FZ_indx: vector of linear indices for sampled orientations in FZ
FZ_indx = np.arange(n_FZ)
print "FZ_indx shape"
print FZ_indx.shape
# FZ_subs: array of subscripts of sampled orientations in FZ
FZ_subs = np.unravel_index(FZ_indx, (n_p1, n_P, n_p2))
FZ_subs = np.array(FZ_subs).transpose()

print "FZ_subs shape"
print FZ_subs.shape
# FZ_euler: array of euler angles of sampled orientations in FZ
FZ_euler = np.float64(FZ_subs*inc)

# g: array of orientation matrices (sample to crystal frame rotation
# matrices) for orientations in fundamental zone
g = ef.bunge2g(FZ_euler[:, 0],
               FZ_euler[:, 1],
               FZ_euler[:, 2])

print "g shape"
print g.shape

# FZ_euler_sym: array of euler angles of sampled orientations in
# FZ and their symmetric equivalents
FZ_euler_sym = np.zeros((12, n_FZ, 3))

# find the symmetric equivalents to the euler angle within the FZ
for sym in xrange(12):
    op = symhex[sym, ...]

    # g_sym: array of orientation matrices transformed with a
    # hexagonal symmetry operator
    g_sym = np.einsum('ik,...kj', op, g)

    tmp = np.array(ef.g2bunge(g_sym)).transpose()

    if sym == 0:
        print "g_sym shape"
        print g_sym.shape
        print "tmp shape"
        print tmp.shape

    del g_sym
    FZ_euler_sym[sym, ...] = tmp
    del tmp

# determine the deviation from symmetry by finding the value of
# the function for symmetric locations and comparing these values

f = h5py.File('symm_check.hdf5', 'w')
error = f.create_dataset("error", (n_th, 12, n_FZ, 4))

for th in xrange(n_th):
    for sym in xrange(12):
        error[th, sym, :, 0:3] = FZ_euler_sym[sym, ...]

        origFZ = db[th,
                    np.int64(FZ_euler_sym[0, :, 0]/inc),
                    np.int64(FZ_euler_sym[0, :, 1]/inc),
                    np.int64(FZ_euler_sym[0, :, 2]/inc)]

        symFZ = db[th,
                   np.int64(FZ_euler_sym[sym, :, 0]/inc),
                   np.int64(FZ_euler_sym[sym, :, 1]/inc),
                   np.int64(FZ_euler_sym[sym, :, 2]/inc)]

        if th == 0 and sym == 0:
            print "origFZ shape"
            print origFZ.shape
            print np.sum(origFZ == 0.0)
            print "symFZ shape"
            print symFZ.shape
            print np.sum(symFZ == 0.0)

        error[th, sym, :, 3] = np.abs(origFZ-symFZ)

error_sec = error[:, :, :, 3]

f.close()

print "mean database value: %s" % np.mean(db)
print "mean error: %s" % np.mean(error_sec)
print "maximum error: %s" % np.max(error_sec)
print "standard deviation of error: %s" % np.std(error_sec)

# plt.figure(num=1, figsize=[10, 6])
# plt.hist(error_sec.reshape(error_sec.size), 100)
# # plt.savefig('test.png')
# plt.show()
