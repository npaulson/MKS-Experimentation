import numpy as np


for ii in xrange(100):

    rrr = np.random.rand(ii, ii, ii, ii, ii, ii)

    print rrr.shape

    memU = rrr.nbytes/(1E9)

    print "array memory usage: %s gb" % memU

    if memU > 75.0:
        break
