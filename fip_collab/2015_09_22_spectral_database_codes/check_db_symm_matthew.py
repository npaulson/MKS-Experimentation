import numpy as np
import matplotlib.pyplot as plt
import h5py


"""
check whether the database exhibits hexagonal-triclinic crystal
symmetry

"""

inc = 5  # degree increment for angular variables

n_th_max = 120/inc  # number of theta samples in FOS
n_max = 360/inc  # number of phi1, Phi and phi2 samples in FOS
n_hlf = 180/inc  # half n_max

n_th = (60/inc)+1  # number of theta samples for FZ
n_p1 = 360/inc  # number of phi1 samples for FZ
n_P = (90/inc)+1  # number of Phi samples for FZ
n_p2 = 60/inc  # number of phi2 samples for FZ

db = np.load("pre_fft_5deg.npy")
print db.shape

db_mean = np.mean(db)

c = 0
d = 0

error = np.zeros([n_th*n_p1*n_P*n_p2, 11])

f = h5py.File('symm_check_matthew.hdf5', 'w')
data = f.create_dataset("data", (n_th*n_p1*n_P*n_p2, 10))

for th in xrange(n_th):
    for p1 in xrange(n_p1):
        for P in xrange(n_P):
            for p2 in xrange(n_p2):
                th_sym = n_th_max - th
                p1_sym = np.mod(p1+n_hlf, n_max)
                P_sym = n_hlf - P
                p2_sym = (60/inc) - np.mod(p2, (60/inc))

                th_sym = np.mod(th_sym, n_th_max)
                p1_sym = np.mod(p1_sym, n_max)
                P_sym = np.mod(P_sym, n_max)
                p2_sym = np.mod(p2_sym, n_max)

                orig_loc = np.array([th, p1, P, p2])*inc
                fin_loc = np.array([th_sym, p1_sym, P_sym, p2_sym])*inc

                data[c, 0:4] = orig_loc
                data[c, 4:8] = fin_loc

                db_orig = db[th, p1, P, p2]
                db_sym = db[th_sym, p1_sym, P_sym, p2_sym]

                data[c, 8] = db_orig[-1]
                data[c, 9] = db_sym[-1]

                error[c] = (np.abs(db_orig[-1]-db_sym[-1])/0.0096)*100

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
print "mean error: %s%%" % np.mean(error)
print "maximum error: %s%%" % np.max(error)
print "standard deviation of error: %s%%" % np.std(error)

plt.hist(error, 100)

plt.show()
