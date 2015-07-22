import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

# load raw data
et_norm = np.load('et_norm.npy')
et = np.load('et.npy')
ep = np.load('ep.npy')
sig = np.load('sig.npy')
I1 = np.load('I1.npy')
I2 = np.load('I2.npy')
I3 = np.load('I3.npy')

# yvar = ep[:, 0]
yvar = I2

# sample_indx = np.array([59, 62, 65, 68, 71, 74, 77, 80, 83, 86, 89, 92, 95, 98])
sample_indx = np.arange(59, 99, 3)
print sample_indx
# sample_indx = np.arange(59, 100)

xsamp = et_norm[sample_indx]
ysamp = yvar[sample_indx]

# plot functions of interest
plt.figure(num=1, figsize=[7, 5])

# plot the original dependent variable data versus the normalized total strain
# quantity
plt.plot(et_norm, yvar, 'bx')
plt.plot(xsamp, ysamp, 'bo')

# xinterp = np.linspace(.0060, .01, 150)
xinterp = np.linspace(.0064, .0094, 150)

# tck = interpolate.splrep(xsamp, ysamp, k=5, s=0)
tck = interpolate.splrep(xsamp, ysamp, k=3)

yinterp = interpolate.splev(xinterp, tck, der=0)

plt.plot(xinterp, yinterp, 'r')

plt.show()
