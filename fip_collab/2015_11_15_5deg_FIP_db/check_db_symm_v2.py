import numpy as np
import matplotlib.pyplot as plt
import euler_func as ef
import h5py


"""
check whether the database exhibits hexagonal-triclinic crystal
symmetry

first find 12 symmetric orientations in triclinic FZ (0<=phi1<2*pi, 0<=Phi<=pi, 0<=phi2<2*pi)

for each deformation mode sample (theta), check if the value of interest is the same for
all symmetric orientations
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

print np.array([n_th, n_p1, n_P, n_p2])

db = np.load("pre_fft.npy")
print db.shape

db_mean = np.mean(db)

# n_FZ: total number of sampled orientations in FZ
n_FZ = n_p1*n_P*n_p2
# FZ_indx: vector of linear indices for sampled orientations in FZ
FZ_indx = np.arange(n_FZ)
print FZ_indx.shape
# FZ_subs: array of subscripts of sampled orientations in FZ
FZ_subs = np.unravel_index(FZ_indx, (n_p1, n_P, n_p2))
FZ_subs = np.array(FZ_subs)
print FZ_subs.shape
# FZ_euler: array of euler angles of sampled orientations in FZ
FZ_euler =  np.float64(FZ_subs*inc)

# g: array of orientation matrices (sample to crystal frame rotation
# matrices) for orientations in fundamental zone
g = ef.bunge2g(FZ_euler[:, 0],
               FZ_euler[:, 1],
               FZ_euler[:, 2])

# FZ_euler_sym: array of euler angles of sampled orientations in
# FZ and their symmetric equivalents
FZ_euler_sym = np.zeros((12, n_FZ, 3))

# find the symmetric equivalents to the euler angle within the FZ
for sym in xrange(12):
    symop = symhex[ii, ...]
    g_sym = np.einsum('ij,...ij', symop, g)
    FZ_euler_sym[ii, ...] = ef.g2bunge(g_sym)

# FZ_subs_sym: array of subscripts of sampled orientations in
# FZ and their symmetric equivalents
FZ_subs_sym = np.int64(FZ_euler_sym/inc)
del FZ_euler_sym

# determine the deviation from symmetry by finding the value of
# the function for symmetric locations and comparing these values

for th in xre



c = 0
d = 0

error = np.zeros([n_th*n_p1*n_P*n_p2])

f = h5py.File('symm_check_matthew.hdf5', 'w')
data = f.create_dataset("data", (n_th*n_p1*n_P*n_p2, 10))

for th in xrange(n_th):
    for p1 in xrange(n_p1):
        for P in xrange(n_P):
            for p2 in xrange(n_p2):
                
                th_sym = n_th_max - th
                p1_sym = np.mod(p1+n_hlf, n_max)
                P_sym = n_hlf - P

                p2_symA1 = 1*n_p2 + p2
                p2_symA2 = 2*n_p2 + p2
                p2_symA3 = 3*n_p2 + p2
                p2_symA4 = 4*n_p2 + p2
                p2_symA5 = 5*n_p2 + p2

                p2_symB0 = 1*n_p2 - np.mod(p2, n_p2)
                p2_symB1 = 2*n_p2 - np.mod(p2, n_p2)
                p2_symB2 = 3*n_p2 - np.mod(p2, n_p2)
                p2_symB3 = 4*n_p2 - np.mod(p2, n_p2)
                p2_symB4 = 5*n_p2 - np.mod(p2, n_p2)
                p2_symB5 = 6*n_p2 - np.mod(p2, n_p2)

                th_sym = np.mod(th_sym, n_th_max)
                p1_sym = np.mod(p1_sym, n_max)
                P_sym = np.mod(P_sym, n_max)

                p2_sym_vec = np.array([p2_symA1, p2_symA2, p2_symA3,
                                       p2_symA4, p2_symA5, p2_symB0,
                                       p2_symB1, p2_symB2, p2_symB3,
                                       p2_symB4, p2_symB5])

                [p2_symA1, p2_symA2, p2_symA3,
                 p2_symA4, p2_symA5, p2_symB0,
                 p2_symB1, p2_symB2, p2_symB3,
                 p2_symB4, p2_symB5] = np.mod(p2_sym_vec, n_max)

                orig_loc = np.array([th, p1, P, p2])*inc
                fin_loc = np.array([th_sym, p1_sym, P_sym, p2_sym])*inc

                data[c, 0:4] = orig_loc
                data[c, 4:8] = fin_loc

                db_orig = db[th, p1, P, p2]
                db_sym = db[th_sym, p1_sym, P_sym, p2_sym]

                data[c, 8] = db_orig[-1]
                data[c, 9] = db_sym[-1]

                error[c] = np.abs(db_orig[-1]-db_sym[-1])

                c += 1

                if np.isclose(db_orig[-1], db_sym[-1], rtol=1E-2) == 0:

                    d += 1

                    # print c
                    # print orig_loc
                    # print fin_loc
                    # print db_orig
                    # print db_sym

f.close()

print c
print d
print "mean database value: %s" % np.mean(db)
print "mean error: %s" % np.mean(error)
print "maximum error: %s" % np.max(error)
print "standard deviation of error: %s" % np.std(error)

plt.hist(error, 100)

plt.show()
