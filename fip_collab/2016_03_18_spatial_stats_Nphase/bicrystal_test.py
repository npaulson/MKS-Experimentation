import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist


el = 21

gridvec = np.arange(el)
gridx, gridy = np.meshgrid(gridvec, gridvec)
gridx = gridx.reshape(gridx.size)
gridy = gridy.reshape(gridy.size)
grid = np.vstack([gridx, gridy]).T
print grid.shape
print grid[:10, :]

loc1 = np.zeros((1, 2))

randi2 = np.int8(2*np.random.rand())
randi4 = np.int8(4*np.random.rand())
randi21 = np.int8(21*np.random.rand())

if randi4 == 0:
    loc1[0, 0] = 0
    loc1[0, 1] = randi21
elif randi4 == 1:
    loc1[0, 0] = 20
    loc1[0, 1] = randi21
elif randi4 == 2:
    loc1[0, 0] = randi21
    loc1[0, 1] = 0
elif randi4 == 3:
    loc1[0, 0] = randi21
    loc1[0, 1] = 20

# loc1 = np.int8(el*np.random.random((1, 2)))
loc2 = np.int8(el*np.random.random((1, 2)))

print loc1
print loc2

dist_loc1 = cdist(grid, loc1)
dist_loc2 = cdist(grid, loc2)

if randi2 == 0:
    dist_xgy = dist_loc1 >= dist_loc2
if randi2 == 1:
    dist_xgy = dist_loc1 < dist_loc2

sve = dist_xgy.reshape(el, el)

plt.figure(num=1, figsize=[8, 8])

plt.plot(loc1[0, 0], loc1[0, 1], 'ro')
plt.plot(loc2[0, 0], loc2[0, 1], 'ro')

plt.imshow(sve, origin='lower', interpolation='none', cmap='magma')
plt.grid(True)

plt.show()
