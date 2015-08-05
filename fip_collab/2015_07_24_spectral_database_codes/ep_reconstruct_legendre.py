import numpy as np
import numpy.polynomial.legendre as leg
import matplotlib.pyplot as plt
from scipy import interpolate

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

sample_indx = np.arange(0, 100, 1)
# print sample_indx

xsamp = et_norm[sample_indx]
ysamp = yvar[sample_indx]

# plot functions of interest
plt.figure(num=1, figsize=[10, 6])

# plot the original dependent variable data versus the normalized total strain
# quantity
plt.plot(et_norm, yvar, 'bx')

# a = .0060
# b = .0100
a = .0064
b = .0096
xorig = np.linspace(a, b, 150)

tck = interpolate.splrep(xsamp, ysamp, k=3)

yspl = interpolate.splev(xorig, tck, der=0)

# plt.plot(xorig, yspl, 'r')
error = 100*np.abs((ysamp - interpolate.splev(xsamp, tck, der=0))/ysamp[95])
print "mean error for splines: %s%%" % np.mean(error)

# highest order legendre polynomial in the fourier representation
N = 5

# calculate legendre nodes and weights
[nodes, weights] = leg.leggauss(N+1)

# calculate locations of the legendre nodes scaled into the range [a,b]
nodes_usc = 0.5*(nodes + 1.0)*(b-a)+a

# calculate the strain value at the node locations
rootsamp = interpolate.splev(nodes_usc, tck, der=0)

# plot the legendre nodes
plt.plot(nodes_usc, rootsamp, 'bo')

coeff_set = np.zeros(N+1)

for kk in xrange(0, N+1):

    # Pk is the 'kk'-th order legendre polynomial evaluated at the nodes of
    # the 'N+1'-st order legendre polynomial
    c = np.zeros(N+1)
    c[kk] = 1
    Pk = leg.legval(nodes, c)

    tmp = 0

    for ii in xrange(0, N+1):

        tmp += weights[ii]*rootsamp[ii]*Pk[ii]

    coeff_set[kk] = 0.5*(2*kk+1)*tmp

print coeff_set

# calculate locations of the desired interpolation points scaled into the
# range [-1,1]
xleg = 2.0*((xorig-a)/(b-a))-1.0
yleg = leg.legval(xleg, coeff_set)

xsamp_sc = 2.0*((xsamp[63:96]-a)/(b-a))-1.0
print xsamp_sc

# calculate error in this approach based on sampled values
print ysamp[63:96]
print leg.legval(xsamp_sc, coeff_set)
error = 100*np.abs((ysamp[63:96] - leg.legval(xsamp_sc, coeff_set))/ysamp[95])
print error
print "mean error: %s%%" % np.mean(error)
print "max error: %s%%" % np.max(error)

plt.plot(xorig, yleg, 'r')

plt.xlabel("$|\epsilon^t|$")
plt.ylabel("$\epsilon_{11}^p$")
plt.title("$|\epsilon^t|$ vs. $\epsilon_{11}^p$ with Legendre Interpolation")

plt.show()
