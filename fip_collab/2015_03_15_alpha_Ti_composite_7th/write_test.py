import numpy as np

for ii in xrange(500):
    np.save('testfile_%s' % ii, np.random.rand(10000))
