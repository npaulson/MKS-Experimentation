import numpy as np
import time

rrr = np.random.rand(.5E8)
print rrr.nbytes/(1E9)
rrr = np.round(rrr)
print np.mean(rrr)

st = time.time()

mmm = rrr == 0

print np.round(time.time()-st, 3)

st = time.time()

mmm = np.abs(rrr-1)

print np.round(time.time()-st, 3)