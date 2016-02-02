import matplotlib.pyplot as plt
import numpy as np
import h5py


f = h5py.File('coeff_total.hdf5', 'r')
coef = np.abs(f.get('coeff')[...])
f.close()

plt.figure(num=1, figsize=[14, 8])

n, bins, patches = plt.hist(coef,
                            500,
                            normed=1,
                            facecolor='green',
                            alpha=0.75)

plt.title("histogram of coefficient magnitudes")
plt.xlabel("coefficient magnitude")

coef_max = coef.max()
n_coef = coef.size

thr_vec = np.array([1e-6, 3.162e-6,
                    1e-5, 3.162e-5,
                    1e-4, 3.162e-4,
                    1e-3, 3.162e-3,
                    1e-2, 3.162e-2,
                    1e-1, 3.162e-1,
                    1e0])

athr = np.zeros(thr_vec.size)

for ii in xrange(thr_vec.size):

    thr = thr_vec[ii]
    gt_thr = np.sum(coef >= thr*coef_max)

    athr[ii] = gt_thr


plt.figure(num=2, figsize=[10, 6])
plt.loglog(thr_vec, athr, 'bx-', basex=10)
# plt.semilogx(thr_vec, athr, basex=10)

plt.title("number of coefficients vs. threshold")
plt.xlabel("threshold (fraction of maximum magnitude coefficient)")
plt.ylabel("number of coefficients > threshold")
plt.grid(True)

print "number of coefficients: %s" % n_coef
print "maximum coefficient magnitude: %s" % coef_max

plt.show()
