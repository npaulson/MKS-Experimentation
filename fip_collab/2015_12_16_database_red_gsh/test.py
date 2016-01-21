import numpy as np

testvec = np.random.rand(10000)

print np.sum(0.5*testvec)
print 0.5*np.sum(testvec)