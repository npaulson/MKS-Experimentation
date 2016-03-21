import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.filters import correlate


el = 21
base = np.float32(np.random.random((21, 21)) < 0.738)

img = np.ones((6, 7))
img[0, 0] = 0.
img[0, 6] = 0.
img[5, 0] = 0.
img[5, 6] = 0.
img[1, 2] = 0.
img[1, 4] = 0.
img[3, 1] = 0.
img[3, 5] = 0.
img[4, 2:5] = 0.
base[3:9, 8:15] = img
base[11:17, 4:11] = img

weights = img

raw = correlate(base, weights)
amin = raw.min()
amax = raw.max()
scaled = (raw - amin)/(amax-amin)

sve = np.int8(scaled == scaled.max())

plt.figure(num=1, figsize=[8, 6])

plt.subplot(221)

ax = plt.imshow(base, origin='upper', interpolation='none', cmap='magma')
plt.colorbar(ax)

plt.subplot(222)

ax = plt.imshow(weights, origin='upper', interpolation='none', cmap='magma')
plt.colorbar(ax)

plt.subplot(223)

ax = plt.imshow(raw, origin='upper', interpolation='none', cmap='magma')
plt.colorbar(ax)

plt.subplot(224)

ax = plt.imshow(sve, origin='upper', interpolation='none', cmap='magma')
plt.colorbar(ax)

plt.show()
