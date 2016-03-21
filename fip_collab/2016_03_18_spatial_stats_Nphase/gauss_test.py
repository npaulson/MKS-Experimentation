import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter


el = 21
base = np.random.random((21, 21))
sigma = [.3, 1.5]
blur_raw = gaussian_filter(base, sigma=sigma)
bmin = blur_raw.min()
bmax = blur_raw.max()
blur_scaled = (blur_raw - bmin)/(bmax-bmin)
sve = np.int8(blur_scaled > .5)

plt.figure(num=1, figsize=[10, 3])

plt.subplot(131)

ax = plt.imshow(base, origin='lower', interpolation='none', cmap='magma')
plt.colorbar(ax)

plt.subplot(132)

ax = plt.imshow(blur_scaled, origin='lower', interpolation='none', cmap='magma')
plt.colorbar(ax)

plt.subplot(133)

ax = plt.imshow(sve, origin='lower', interpolation='none', cmap='magma')
plt.colorbar(ax)

plt.show()
