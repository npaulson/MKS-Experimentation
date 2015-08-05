import numpy as np
import matplotlib.pyplot as plt
import lagrange_interp as li
import chebyshev

# load raw data
et_norm = np.load('et_norm.npy')
# et = np.load('et.npy')
ep = np.load('ep.npy')
# sig = np.load('sig.npy')
# I1 = np.load('I1.npy')
# I2 = np.load('I2.npy')
# I3 = np.load('I3.npy')

yvar = ep[:, 0]
# yvar = I2

# the following vector closely matches that of et_norm
xvec = np.linspace(.0001, .0100, 100)
# find the maximum percent deviation between etvec and et_norm
et_err = 100*np.mean(np.abs((xvec-et_norm)/xvec))

msg = "maximum %% devation in et_norm scales: %s%%" % et_err
print msg

# sample_indx = np.array([55, 57, 59, 63, 67, 71, 75, 79, 83, 87, 91, 95, 97, 99])
xk = chebyshev.chebyshev_nodes(63., 95., 11)
sample_indx = np.int8(np.round(xk-1))
print xk
print sample_indx

xsamp = et_norm[sample_indx]
ysamp = yvar[sample_indx]

# plot functions of interest
plt.figure(num=1, figsize=[10, 6])

# plot the original dependent variable data versus the normalized total strain
# quantity
plt.plot(et_norm, yvar, 'bx')
plt.plot(xsamp, ysamp, 'bo')

xinterp = np.linspace(.0064, .0094, 150)

yinterp = li.lagrange_interp(xsamp, ysamp, xinterp)

plt.plot(xinterp, yinterp, 'r')

plt.xlabel("$|\epsilon^t|$")
plt.ylabel("$\epsilon_{11}^p$")
plt.title("$|\epsilon^t|$ vs. $\epsilon_{11}^p$ with Lagrange Interpolation")

plt.show()

# calculate error in this approach based on sampled values
print yvar[63:96]
print li.lagrange_interp(xsamp, ysamp, et_norm[63:96])
error = 100*np.abs((yvar[63:96] - li.lagrange_interp(xsamp, ysamp, et_norm[63:96]))/yvar[95])
print error
print 'mean error: %s%%' % np.mean(error)
print 'max error: %s%%' % np.max(error)
