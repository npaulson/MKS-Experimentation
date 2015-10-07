import numpy as np
import h5py
import sys
import time


f_db = h5py.File('final_db.hdf5', 'r')

tmp = f_db.get("s_list")
s_list = tmp[...]

tmp = f_db.get("f_list")
f_list = tmp[...]

f_db.close()

Lset = np.array([120., 360., 360., 360.])*(np.pi/180.)

st = time.time()

xi = np.array([5., 5., 5., 5.])*3*(np.pi/180)

Pvec = f_list[:, -1] * \
             np.exp((2*np.pi*1j*s_list[:, 0]*xi[0])/Lset[0]) * \
             np.exp((2*np.pi*1j*s_list[:, 1]*xi[1])/Lset[1]) * \
             np.exp((2*np.pi*1j*s_list[:, 2]*xi[2])/Lset[2]) * \
             np.exp((2*np.pi*1j*s_list[:, 3]*xi[3])/Lset[3])

Numel = 40*120*120*120

db_res = np.real(np.sum(Pvec, 0)/Numel)

print "time to interpolate: %ss" % (time.time()-st)

print db_res

pre_fft = np.load("pre_fft.npy")

print pre_fft.shape

act_res = pre_fft[5, 5, 5, 5, -1]

err = ((act_res - db_res) / 0.0096) * 100

print "error: %s%%" % err
