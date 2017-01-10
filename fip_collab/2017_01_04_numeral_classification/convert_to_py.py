import scipy.io as sio
import h5py
import numpy as np
import matplotlib.pyplot as plt


"""load the matlab file"""
raw = sio.loadmat('ex4data1.mat')

y = np.squeeze(raw['y'])   # classified digits
X = raw['X']   # raw image data

print "y.shape: " + str(y.shape)
print "X.shape: " + str(X.shape)

"""relabel y so that 0 is labeled 0 instead of 10"""
y[y == 10] = 0

"""save in hdf5 format"""
f = h5py.File('digits.hdf5', 'w')
f.create_dataset('X', data=X)
f.create_dataset('y', data=y)
f.close()

"""plot a random image and print the associated digit"""
ii = np.random.randint(y.size)

dim = np.int16(np.sqrt(X.shape[1]))
X_ = X[ii, :].reshape((dim, dim))

ax = plt.imshow(X_.T, origin='upper',
                interpolation='none', cmap='gray')
plt.colorbar(ax)
plt.title('y = %s' % y[ii])

plt.show()
