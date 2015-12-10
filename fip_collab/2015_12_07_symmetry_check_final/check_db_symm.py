import numpy as np
import matplotlib.pyplot as plt
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

inc = 6  # degree increment for angular variables
np.random.seed()  # generate seed for random
symhex = ef.symhex()
r2d = 180./np.pi
d2r = np.pi/180.
r2s = r2d/inc

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

# convert euler angles to subscripts
FZ_subs_sym = np.int64(np.round(FZ_euler_sym*r2s))

# # make sure all of the euler angles within the appropriate
# # ranges (eg. not negative)
for ii in xrange(3):
    lt = FZ_subs_sym[..., ii] < 0.0
    FZ_subs_sym[..., ii] += n_max*lt
print np.sum(FZ_subs_sym < 0)

# determine the deviation from symmetry by finding the value of
# the function for symmetric locations and comparing these values

f = h5py.File('symm_check.hdf5', 'w')
error = f.create_dataset("error", (n_th, 12, n_FZ, 5))

for th in xrange(n_th):
    for sym in xrange(12):
        error[th, sym, :, 0:3] = FZ_subs_sym[sym, ...]*inc

        origFZ = db[th,
                    FZ_subs_sym[0, :, 0],
                    FZ_subs_sym[0, :, 1],
                    FZ_subs_sym[0, :, 2]]
        symFZ = db[th,
                   FZ_subs_sym[sym, :, 0],
                   FZ_subs_sym[sym, :, 1],
                   FZ_subs_sym[sym, :, 2]]

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
th_rand = np.int64(np.round((n_th-1)*np.random.rand()))
g_rand = np.int64(np.round((n_FZ-1)*np.random.rand()))

# badloc = np.argmax(error_sec[..., 4])
# badloc = np.unravel_index(badloc, error_sec[..., 3].shape)

# th_rand = badloc[0]
# g_rand = badloc[2]

print "\nexample comparison:"

print "deformation mode: %s degrees" % str(np.float(th_rand*inc))

for sym in xrange(12):
    print "operator number: %s" % sym
    eul_rand = error_sec[th_rand, sym, g_rand, 0:3]
    print "euler angles: %s (degrees)" % str(eul_rand)
    val_rand = error_sec[th_rand, sym, g_rand, 3]
    print "value of interest: %s" % str(val_rand)

errvec = error_sec[..., 4].reshape(error_sec[..., 4].size)

print "\noverall error metrics:"
print "mean database value: %s" % np.mean(db)
print "mean error: %s" % np.mean(errvec)
print "maximum error: %s" % np.max(errvec)
print "standard deviation of error: %s" % np.std(errvec)
print "total number of locations checked: %s" % (errvec.size)
err_count = np.sum(errvec != 0.0)

# plot the error histograms

error_indx = errvec != 0.0
print error_indx.shape
loc_hist = errvec[error_indx]
print loc_hist.shape
err_count = np.sum(loc_hist != 0.0)
print "number of locations with nonzero error: %s" % err_count

# errvec_p1 = error_sec[..., 0].reshape(error_sec[..., 0].size)[error_indx]
# plt.figure(num=4, figsize=[10, 6])
# plt.hist(errvec_p1, 361)

# errvec_P = error_sec[..., 1].reshape(error_sec[..., 1].size)[error_indx]
# plt.figure(num=5, figsize=[10, 6])
# plt.hist(errvec_P, 361)

# errvec_p2 = error_sec[..., 0].reshape(error_sec[..., 0].size)[error_indx]
# plt.figure(num=6, figsize=[10, 6])
# plt.hist(errvec_p2, 361)

# # plot the error histograms
# plt.figure(num=1, figsize=[10, 6])
# error_hist = error_sec[..., 4]
# plt.hist(error_hist.reshape(error_hist.size), 100)

# plot the symmetric orientations in euler space
plt.figure(2)

plt.plot(np.array([0, 360, 360, 0, 0]), np.array([0, 0, 180, 180, 0]), 'k-')
plt.plot(np.array([0, 360]), np.array([90, 90]), 'k-')

plt.xlabel('$\phi_1$')
plt.ylabel('$\Phi$')

sc = 1.05

plt.axis([-(sc-1)*360, sc*360, -(sc-1)*180, sc*180])

plt.figure(3)

plt.plot(np.array([0, 180, 180, 0, 0]), np.array([0, 0, 360, 360, 0]), 'k-')
plt.plot(np.array([90, 90]), np.array([0, 360]), 'k-')
plt.plot(np.array([0, 180]), np.array([60, 60]), 'k-')
plt.plot(np.array([0, 180]), np.array([120, 120]), 'k-')
plt.plot(np.array([0, 180]), np.array([180, 180]), 'k-')
plt.plot(np.array([0, 180]), np.array([240, 240]), 'k-')
plt.plot(np.array([0, 180]), np.array([300, 300]), 'k-')


plt.xlabel('$\Phi$')
plt.ylabel('$\phi2$')

sc = 1.05

plt.axis([-(sc-1)*180, sc*180, -(sc-1)*360, sc*360])

eul_plt = error_sec[th_rand, :, g_rand, 0:3]

plt.figure(2)
plt.plot(eul_plt[:, 0], eul_plt[:, 1],
         c='b', marker='o', linestyle='none')
plt.figure(3)
plt.plot(eul_plt[:, 1], eul_plt[:, 2],
         c='b', marker='o', linestyle='none')

plt.show()
