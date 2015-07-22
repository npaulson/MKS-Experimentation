import matplotlib.pyplot as plt
import numpy as np

# mean_curve = np.load('mean_curve.npy')
# std_curve = np.load('std_curve.npy')
cmat = np.load('cmat.npy')

et_vec = np.linspace(.006, .01, 41)

plt.figure()

# plt.errorbar(et_vec, mean_curve, yerr=std_curve)

for ii in xrange(21):
    plt.plot(et_vec, cmat[ii, :])

plt.show()
