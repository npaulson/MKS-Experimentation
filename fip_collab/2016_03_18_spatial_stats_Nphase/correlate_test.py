import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.filters import correlate


el = 21
base = np.random.random((21, 21))
# base = np.zeros((21, 21))
base[1:4, 1:4] = 1
base[1, 1] = 0.7
base[1, 3] = 0.7
base[3, 1] = 0.7
base[3, 3] = 0.7
base[2, 2] = .2

weights = np.ones((3, 3))
weights[0, 0] = 0.7
weights[0, 2] = 0.7
weights[2, 0] = 0.7
weights[2, 2] = 0.7
weights[1, 1] = .2

# weights = np.random.rand(3, 3)

raw = correlate(base, weights)
amin = raw.min()
amax = raw.max()
scaled = (raw - amin)/(amax-amin)

sve = np.int8(scaled >= .8)

plt.figure(num=1, figsize=[8, 6])

plt.subplot(221)

ax = plt.imshow(base, origin='lower', interpolation='none', cmap='magma')
plt.colorbar(ax)

plt.subplot(222)

ax = plt.imshow(weights, origin='lower', interpolation='none', cmap='magma')
plt.colorbar(ax)

plt.subplot(223)

ax = plt.imshow(scaled, origin='lower', interpolation='none', cmap='magma')
plt.colorbar(ax)

plt.subplot(224)

ax = plt.imshow(sve, origin='lower', interpolation='none', cmap='magma')
plt.colorbar(ax)

plt.show()
