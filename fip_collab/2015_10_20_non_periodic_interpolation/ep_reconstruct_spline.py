import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

# load raw data
et_norm = np.load('et_norm.npy')
ep = np.load('ep.npy')

a = .0060  # start of range for legendre interpolation
b = .0100  # end of range for legendre interpolation

st_e = 0.0001

ai = np.int8(np.round(a/st_e))-1
bi = np.int8(np.round(b/st_e))-1


yvar = ep[:, 0]

sample_indx = np.arange(ai, bi, 4)

xsamp = et_norm[sample_indx]
ysamp = yvar[sample_indx]

# tck = interpolate.splrep(xsamp, ysamp, k=5, s=0)
tck = interpolate.splrep(xsamp, ysamp, k=3)

ytest = interpolate.splev(et_norm[ai:bi+1], tck, der=0)

# calculate error in this approach based on sampled values
error = 100*np.abs((yvar[ai:bi+1] - ytest)/et_norm[ai:bi+1])

print "mean error: %s%%" % np.mean(error)
print "maximum error: %s%%" % np.max(error)

# plot functions of interest
plt.figure(num=1, figsize=[7, 5])

# plot the original dependent variable data versus the normalized total strain
# quantity
plt.plot(et_norm[ai:bi+1], yvar[ai:bi+1], 'bx')
plt.plot(xsamp, ysamp, 'bo')

# xinterp = np.linspace(.0060, .01, 150)
xinterp = np.linspace(.0064, .0096, 150)

yinterp = interpolate.splev(xinterp, tck, der=0)
plt.plot(xinterp, yinterp, 'r')

plt.show()
