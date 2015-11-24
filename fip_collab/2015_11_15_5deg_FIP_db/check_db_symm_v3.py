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

np.random.seed() # generate seed for random
symhex = ef.symhex()
r2d = 180./np.pi
d2r = np.pi/180.

inc = 5  # degree increment for angular variables

n_th_max = 120/inc  # number of theta samples in FOS
n_max = 360/inc  # number of phi1, Phi and phi2 samples in FOS
n_hlf = 180/inc  # half n_max

n_th = (60/inc)+1  # number of theta samples for FZ
n_p1 = 360/inc  # number of phi1 samples for FZ
n_P = (90/inc)+1  # number of Phi samples for FZ
n_p2 = 60/inc  # number of phi2 samples for FZ

print "angle space shape: %s" % str(np.array([n_th, n_p1, n_P, n_p2]))

# only look at last in series for value of interest
db = np.load("pre_fft.npy")[:n_th, ..., -1]
print "db shape: %s" % str(db.shape)


# n_FZ: total number of sampled orientations in FZ
n_FZ = n_p1*n_P*n_p2
# FZ_indx: vector of linear indices for sampled orientations in FZ
FZ_indx = np.arange(n_FZ)
print "FZ_indx shape: %s" % str(FZ_indx.shape)
# FZ_subs: array of subscripts of sampled orientations in FZ
FZ_subs = np.unravel_index(FZ_indx, (n_p1, n_P, n_p2))
FZ_subs = np.array(FZ_subs).transpose()

print "FZ_subs shape: %s" % str(FZ_subs.shape)
# FZ_euler: array of euler angles of sampled orientations in FZ
FZ_euler = np.float64(FZ_subs*inc*d2r)

# g: array of orientation matrices (sample to crystal frame rotation
# matrices) for orientations in fundamental zone
g = ef.bunge2g(FZ_euler[:, 0],
               FZ_euler[:, 1],
               FZ_euler[:, 2])

print "g shape: %s" % str(g.shape)

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
        print "g_sym shape: %s" % str(g_sym.shape)
        print "tmp shape: %s" % str(tmp.shape)

    del g_sym
    FZ_euler_sym[sym, ...] = tmp
    del tmp

# make sure all of the euler angles within the appropriate
# ranges (eg. not negative)
for ii in xrange(3):
    ltz = FZ_euler_sym[..., ii] < 0.0
    FZ_euler_sym[..., ii] += 2*np.pi*ltz

# determine the deviation from symmetry by finding the value of
# the function for symmetric locations and comparing these values

f = h5py.File('symm_check.hdf5', 'w')
error = f.create_dataset("error", (n_th, 12, n_FZ, 5))

for th in xrange(n_th):
    for sym in xrange(12):
        error[th, sym, :, 0:3] = FZ_euler_sym[sym, ...]

        mm = r2d/inc

        p1tmp = np.int64(np.round(FZ_euler_sym[0, :, 0]*mm))
        Ptmp = np.int64(np.round(FZ_euler_sym[0, :, 1]*mm))
        p2tmp = np.int64(np.round(FZ_euler_sym[0, :, 2]*mm))

        print np.min(p1tmp)
        print np.max(p1tmp)

        print np.min(Ptmp)
        print np.max(Ptmp)

        print np.min(p2tmp)
        print np.max(p2tmp)

        origFZ = db[th, p1tmp, Ptmp, p2tmp]

        p1tmp = np.int64(np.round(FZ_euler_sym[sym, :, 0]*mm))
        Ptmp = np.int64(np.round(FZ_euler_sym[sym, :, 1]*mm))
        p2tmp = np.int64(np.round(FZ_euler_sym[sym, :, 2]*mm))

        symFZ = dg[th, p1tmp, Ptmp, p2tmp]

        if th == 0 and sym == 0:
            print "origFZ shape: %s" % str(origFZ.shape)
            print "symFZ shape: %s" % str(symFZ.shape)

        if th == 0:
            print "operator number: %s" % sym
            idcheck = np.all(FZ_euler_sym[0, ...] == FZ_euler_sym[sym, ...])
            print "are Euler angles in different FZs identical?: %s" % str(idcheck)

        orig_0sum = np.sum(origFZ == 0.0)
        sym_0sum = np.sum(symFZ == 0.0)

        if orig_0sum != 0 or sym_0sum != 0:
            print "number of zero values in origFZ: %s" % orig_0sum
            print "number of zero values in symFZ: %s" % sym_0sum

        error[th, sym, :, 3] = symFZ
        error[th, sym, :, 4] = np.abs(origFZ-symFZ)

error_sec = error[...]

f.close()

# perform error analysis

# generate random deformation mode and euler angle
th_rand = np.int64(np.round(n_th*np.random.rand()-1))
g_rand = np.int64(np.round(n_FZ*np.random.rand()-1))

print "\nexample comparison:"

print "deformation mode: %s degrees" % str(np.float(th_rand*inc))

for sym in xrange(12):
    print "operator number: %s" % sym
    eul_rand = error_sec[th_rand, sym, g_rand, 0:3]*r2d
    print "euler angles: %s (degrees)" % str(np.round(eul_rand))
    val_rand = error_sec[th_rand, sym, g_rand, 3]
    print "value of interest: %s" % str(val_rand)

print "\noverall error metrics:"
print "mean database value: %s" % np.mean(db)
print "mean error: %s" % np.mean(error_sec[..., 4])
print "maximum error: %s" % np.max(error_sec[..., 4])
print "standard deviation of error: %s\n" % np.std(error_sec[..., 4])

# plt.figure(num=1, figsize=[10, 6])
# plt.hist(error_sec.reshape(error_sec.size), 100)
# # plt.savefig('test.png')
# plt.show()
