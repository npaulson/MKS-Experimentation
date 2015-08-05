import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

# load raw data
et_norm = np.load('et_norm.npy')
# et = np.load('et.npy')
ep = np.load('ep11.npy')
# sig = np.load('sig.npy')
# I1 = np.load('I1.npy')
# I2 = np.load('I2.npy')
# I3 = np.load('I3.npy')

yvar = ep
# yvar = I2

# sample_indx = np.array([59, 62, 65, 68, 71, 74, 77, 80, 83, 86, 89, 92, 95, 98])
sample_indx = np.arange(62, 96, 4)
print sample_indx
# sample_indx = np.arange(59, 100)

xsamp = et_norm[sample_indx]
ysamp = yvar[sample_indx]

# plot functions of interest
plt.figure(num=1, figsize=[10, 6])

# plot the original dependent variable data versus the normalized total strain
# quantity
plt.plot(et_norm, yvar, 'bx')
plt.plot(xsamp, ysamp, 'bo')

# xinterp = np.linspace(.0060, .01, 150)
xinterp = np.linspace(.0064, .0094, 150)

# tck = interpolate.splrep(xsamp, ysamp, k=5, s=0)
tck = interpolate.splrep(xsamp, ysamp, k=3)

yinterp = interpolate.splev(xinterp, tck, der=0)

# calculate error in this approach based on sampled values
x4err = np.linspace(.0064, .0096, len(yvar[63:96]))
print x4err
y4err_actual = yvar[63:96]
print y4err_actual
y4err_spline = interpolate.splev(x4err, tck, der=0)
print y4err_spline

error = 100*np.abs((y4err_actual - y4err_spline)/yvar[95])
print error
print "mean error: %s%%" % np.mean(error)
print "max error: %s%%" % np.max(error)


plt.plot(xinterp, yinterp, 'r')

plt.xlabel("$|\epsilon^t|$")
plt.ylabel("$\epsilon_{11}^p$")
plt.title("$|\epsilon^t|$ vs. $\epsilon_{11}^p$ with Spline Interpolation")

plt.show()
