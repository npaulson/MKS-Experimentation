import numpy as np
import h5py
import sys
import time


# def triginterp(s_list, f_list, xi, Lset, Numel):

#     Pvec = f_list * \
#         np.exp((2*np.pi*1j*s_list[:, 0]*xi[:, 0:1])/Lset[0]) * \
#         np.exp((2*np.pi*1j*s_list[:, 1]*xi[:, 1:2])/Lset[1]) * \
#         np.exp((2*np.pi*1j*s_list[:, 2]*xi[:, 2:3])/Lset[2]) * \
#         np.exp((2*np.pi*1j*s_list[:, 3]*xi[:, 3:4])/Lset[3])

#     return np.real(np.sum(Pvec, 1)/Numel)


f_db = h5py.File('final_db.hdf5', 'r')

tmp = f_db.get("s_list")
s_list = tmp[...]

tmp = f_db.get("f_list")
f_list = tmp[...]

f_db.close()

# Lset = np.array([115., 355., 355., 355.])*(np.pi/180.)
Lset = np.array([120., 360., 360., 360.])*(np.pi/180.)

xi = np.array([[0., 0., 0., 0.],
               [1., 2., 3., 4.]])*5.*(np.pi/180)

Pvec = np.expand_dims(f_list, axis=1)

for ii in xrange(4):

    tmp = np.exp((2*np.pi*1j*s_list[:, ii]*xi[:, ii:ii+1])/Lset[ii])
    tmp = np.expand_dims(tmp.T, axis=2)

    if ii == 0:
        TMP = np.ones(tmp.shape, dtype='complex64')

    TMP *= tmp

Pvec = Pvec*TMP

print Pvec.shape

Numel = 24*72*72*72

results = np.real(np.sum(Pvec, 0)/Numel)

print results

pre_fft = np.load("pre_fft.npy")

print pre_fft[0, 0, 0, 0, :]
print pre_fft[1, 2, 3, 4, :]
