import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.filters import convolve
from scipy.ndimage.filters import gaussian_filter


def scale_array(raw):
    amin = raw.min()
    amax = raw.max()
    return (raw-amin)/(amax-amin)

el = 21
base = np.random.random((21, 21))
# base = np.int8(base > .02)

# weights = np.zeros((3, 3))
# weights[0, 0] = .75
# weights[0, 1] = .25
# weights[1, 0] = .25
# weights[1, 1] = 1.0
# weights[2, 2] = .75
# weights[1, 2] = .25
# weights[2, 1] = .25

r2a = np.random.randint(1, 5)
r2b = np.random.randint(1, 5)
weights = np.random.random(size=(r2a, r2b))

raw = convolve(base, weights, mode='wrap')

sigset = [0., .2, .4, .6, .8]

blur = gaussian_filter(raw, sigma=np.random.choice(sigset))
scaled = scale_array(blur)

H = 4
vf_bounds = np.sort(np.random.rand(H-1))
print vf_bounds


sve = np.int8(scaled >= .5)

plt.figure(num=1, figsize=[10, 8])

plt.subplot(231)

ax = plt.imshow(base, origin='lower', interpolation='none', cmap='magma')
plt.colorbar(ax)

plt.subplot(232)

ax = plt.imshow(weights, origin='lower', interpolation='none', cmap='magma')
plt.colorbar(ax)

plt.subplot(233)

ax = plt.imshow(raw, origin='lower', interpolation='none', cmap='magma')
plt.colorbar(ax)

plt.subplot(234)

ax = plt.imshow(scaled, origin='lower', interpolation='none', cmap='magma')
plt.colorbar(ax)

plt.subplot(235)

ax = plt.imshow(sve, origin='lower', interpolation='none', cmap='magma')
plt.colorbar(ax)

plt.show()
