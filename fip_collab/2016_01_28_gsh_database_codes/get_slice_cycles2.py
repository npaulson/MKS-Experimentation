import numpy as np
import h5py
import sys


tnum = sys.argv[1]

f = h5py.File('var_extract_%s.hdf5' % str(tnum).zfill(2), 'r')
data = f.get('var_set')[...].real
f.close()

n_cyc = 100

"""Perform analysis on statistics cycle to cycle"""

ang_sel = data[:, 4] == 0
min_cyc0 = data[ang_sel, 5].min()
min_cyc0 = data[ang_sel, 5].min()
min_cyc0 = data[ang_sel, 5].min()

minvec = np.zeros(n_cyc)
meanvec = np.zeros(n_cyc)
maxvec = np.zeros(n_cyc)

for cyc in xrange(n_cyc):

    ang_sel = data[:, 4] == cyc
    minvec[cyc] = data[ang_sel, 5].min()
    meanvec[cyc] = data[ang_sel, 5].mean()
    maxvec[cyc] = data[ang_sel, 5].max()

print "minimum FIP per cycle: %s" % str(minvec)
print "mean FIP per cycle: %s" % str(meanvec)
print "maximum FIP per cycle: %s" % str(maxvec)

diffvec = np.zeros(n_cyc - 2)

for cyc in xrange(1, n_cyc-1):

    ang_sel_prev = data[:, 4] == cyc - 1
    ang_sel_curr = data[:, 4] == cyc

    diff = np.abs(data[ang_sel_curr, 5] - data[ang_sel_prev, 5])
    diffnorm = diff/data[ang_sel_curr, 5]

    diffvec[cyc-1] = diffnorm.mean()

print "mean of absolute value of FIP difference per cycle: %s" % str(diffvec)

f = h5py.File('slice_%s.hdf5' % str(tnum).zfill(2), 'w')
f.create_dataset('minvec', data=minvec)
f.create_dataset('meanvec', data=meanvec)
f.create_dataset('maxvec', data=maxvec)
f.create_dataset('diffvec', data=diffvec)
f.close()
