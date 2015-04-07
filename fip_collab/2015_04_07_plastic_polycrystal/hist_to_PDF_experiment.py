import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats


plt.figure(num=1, figsize=[10, 7])

ns = 1000.
dist = np.random.randn(ns)

dmin = np.amin([dist])
dmax = np.amax([dist])

nbins = 10

relfreqs, lowlim, binsize, extrapoints = stats.relfreq(dist, nbins)

print relfreqs.shape
print lowlim
print binsize
print np.linspace(lowlim, binsize*(nbins+1) + lowlim, nbins).shape

plt.plot(np.linspace(lowlim, binsize*(nbins+1) + lowlim, nbins), relfreqs)

# histogram 1
nbins = 9
n1, bins, patches = plt.hist(dist,
                             bins=nbins,
                             histtype='step',
                             hold=True,
                             range=(dmin, dmax),
                             color='white')

bincenters = 0.5*(bins[1:]+bins[:-1])
rsp1, = plt.plot(bincenters, n1/ns, 'r', linestyle='-', lw=1.0)

# # histogram 2
# nbins = 20
# n2, bins, patches = plt.hist(dist,
#                              bins=nbins,
#                              histtype='step',
#                              hold=True,
#                              range=(dmin, dmax),
#                              color='white')

# bincenters = 0.5*(bins[1:]+bins[:-1])
# rsp2, = plt.plot(bincenters, n2/ns, 'r', linestyle='-', lw=1.0)

# # histogram 3
# nbins = 100
# n3, bins, patches = plt.hist(dist,
#                              bins=nbins,
#                              histtype='step',
#                              hold=True,
#                              range=(dmin, dmax),
#                              color='white')

# bincenters = 0.5*(bins[1:]+bins[:-1])
# rsp3, = plt.plot(bincenters, n3/ns, 'g', linestyle='-', lw=1.0)

# plt.grid(True)

# plt.legend([rsp1, rsp2, rsp3], ["bins = 10", "bins = 20", "bins = 100"])

# plt.xlabel('x-axis')
# plt.ylabel('Frequency')

plt.ylim([0, 1.1])

plt.show()
