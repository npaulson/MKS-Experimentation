import matplotlib.pyplot as plt
import numpy as np

mean_curve = np.load('mean_curve.npy')
std_curve = np.load('std_curve.npy')

et_vec = np.linspace(.006, .01, 41)

plt.figure()

plt.errorbar(et_vec, mean_curve, yerr=std_curve)

plt.show()
