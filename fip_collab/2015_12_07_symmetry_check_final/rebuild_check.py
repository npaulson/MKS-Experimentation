import numpy as np


"""
This code takes a fully symmetric set of input variables that cover
all orientation/ deformation space. Here I attempt to rebuild this
array only from one of the fundamental zones. This is important to
formulate correctly as we need to create a fully periodic array
from a single FZ in order to utilize the FFT for interpolation

Noah Paulson
12/8/2015
"""

inc = 5  # degree increment for angular variables
r2d = 180./np.pi
d2r = np.pi/180.
r2s = r2d/inc

n_th_max = 120/inc  # number of theta samples in FOS
n_max = 360/inc  # number of phi1, Phi and phi2 samples in FOS
n_hlf = 180/inc  # half n_max

n_th = (60/inc)+1  # number of theta samples for FZ
n_p1 = 360/inc  # number of phi1 samples for FZ
n_P = (90/inc)+1  # number of Phi samples for FZ
n_p2 = 60/inc  # number of phi2 samples for FZ

FOS_orig = np.load('pre_fft.npy')
FZ0 = FOS_orig[:n_th, :n_p1, :n_P, :n_p2, :]

pre_fft = np.zeros(FOS_orig.shape)

""" fill the theta 0:60, phi1 0:360, Phi 0:90, phi2: 0:60 degree zone """
pre_fft[:n_th, :, :n_P, :n_p2, :] = FZ0

""" fill the theta 0:60, phi1 0:360, Phi 90:180, phi2: 0:60 degree zone """

# roll 180 degrees in phi1
tmp = np.roll(FZ0, n_hlf, 1)
# flip in Phi
tmp = tmp[:, :, ::-1, :, :]
# flip in phi2
tmp_red = tmp[:, :, :, 1:, :]
tmp_red = tmp_red[:, :, :, ::-1, :]

tmp[:, :, :, 1:, :] = tmp_red

pre_fft[:n_th, :, n_P-1:n_hlf+1, :n_p2, :] = tmp
del tmp, tmp_red

print np.all(np.isclose(pre_fft[:n_th, :, :n_hlf, :n_p2, :],
                        FOS_orig[:n_th, :, :n_hlf, :n_p2, :]))
print pre_fft[3, 3, 30, 3, -1]
print FOS_orig[3, 3, 30, 3, -1]

""" fill the theta 0:60, phi1 0:360, Phi 180:360, phi2: 0:60 degree zone """
tmp = pre_fft[:n_th, :, :n_hlf+1, :n_p2, :]
tmp = tmp[:, :, ::-1, :, :]

pre_fft[:n_th, :, n_hlf:, :n_p2, :] = tmp[:, :, :-1, :, :]
del tmp

print np.all(np.isclose(pre_fft[:n_th, :, :, :n_p2, :],
                        FOS_orig[:n_th, :, :, :n_p2, :]))

""" fill the theta 0:120, phi1 0:360, Phi 0:360, phi2: 0:60 degree zone """
tmp = pre_fft[1:n_th-1, :, :, :n_p2, :]
pre_fft[n_th:, :, :, :n_p2, :] = tmp[::-1, ...]
del tmp

print np.all(np.isclose(pre_fft[:, :, :, :n_p2, :],
                        FOS_orig[:, :, :, :n_p2, :]))

""" fill the theta 0:120, phi1 0:360, Phi 0:360, phi2: 60:360 degree zone """
tmp = pre_fft[:, :, :, :n_p2, :]
pre_fft[:, :, :, 1*n_p2:2*n_p2, :] = tmp
pre_fft[:, :, :, 2*n_p2:3*n_p2, :] = tmp
pre_fft[:, :, :, 3*n_p2:4*n_p2, :] = tmp
pre_fft[:, :, :, 4*n_p2:5*n_p2, :] = tmp
pre_fft[:, :, :, 5*n_p2:, :] = tmp
del tmp

print np.all(np.isclose(pre_fft,
                        FOS_orig))
