import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.filters import convolve
from scipy.ndimage.filters import gaussian_filter


def scale_array(raw):
    amin = raw.min()
    amax = raw.max()
    return (raw-amin)/(amax-amin)

el = 21
H = 2

base = np.random.random((21, 21))

r2a = np.random.randint(1, 5)
r2b = np.random.randint(1, 5)
weights = np.random.random(size=(r2a, r2a))

raw = convolve(base, weights, mode='wrap')

sigset = [0., .2, .4, .6, .8, 2, 5]

blur = gaussian_filter(raw, sigma=np.random.choice(sigset))
scaled = scale_array(blur)

scaled_lin = scaled.reshape(21**2)
sve = np.zeros((21**2))

vf_bounds = np.zeros(H+1)
vf_bounds[-1] = 1
tmp = np.sort(np.random.rand(H-1))
vf_bounds[1:H] = tmp
print vf_bounds

for ii in xrange(H):
    indx = (scaled_lin > vf_bounds[ii])*(scaled_lin <= vf_bounds[ii+1])
    print np.sum(indx)

    sve[indx] = ii

sve = sve.reshape(21, 21)


plt.figure(num=1, figsize=[10, 8])

plt.subplot(231)

ax = plt.imshow(base, origin='lower', interpolation='none', cmap='magma')
plt.colorbar(ax)

plt.subplot(232)

ax = plt.imshow(weights, origin='lower', interpolation='none', cmap='gray',
                vmin=0, vmax=1)
plt.colorbar(ax)

plt.subplot(233)

ax = plt.imshow(raw, origin='lower', interpolation='none', cmap='magma')
plt.colorbar(ax)

plt.subplot(234)

ax = plt.imshow(scaled, origin='lower', interpolation='none', cmap='magma')
plt.colorbar(ax)

plt.subplot(235)

ax = plt.imshow(sve, origin='lower', interpolation='none', cmap='viridis')
plt.colorbar(ax)

plt.show()
