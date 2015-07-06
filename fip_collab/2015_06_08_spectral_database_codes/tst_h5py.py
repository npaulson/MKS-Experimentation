import numpy as np
import h5py

f = h5py.File("Results_tensor_11.hdf5", "r")
# dset = f.get("sim0074399")
dset = f.get("sim0010000")

"""
Column order in each dataset:
time,...
sig11,sig22,sig33,sig12,sig13,sig23...
e11,e22,e33,e12,e13,e23
ep11,ep22,ep33,ep12,ep13,ep23
"""

eps = dset[:, 7:13]

e_norm = np.sqrt(eps[:, 0]**2 + eps[:, 1]**2 + eps[:, 2]**2 +
                 eps[:, 3]**2 + eps[:, 4]**2 + eps[:, 5]**2)

stmax = eps[-1, :]

print stmax
print e_norm

tmp = e_norm - np.roll(e_norm, 1)
tmp = tmp[1:]
print np.mean(tmp)
print np.std(tmp)
