import numpy as np
import h5py
import sys
import time

"""
This code is designed to arrange simulation database chunks, take the fft and
select the frequencies with the highest magnitudes

Important Acronyms:
FZ: hexagonal-triclinic fundamental zone
FOS: full euler orientation space (0-360 degree in each angle)

"""

# initialize important variables

tnum = sys.argv

comp = "11"  # strain component of interest

# define the number of increments for angular variables:

inc = 3  # degree increment for angular variables

n_th_max = 120/inc  # number of theta samples in FOS
n_max = 360/inc  # number of phi1, Phi and phi2 samples in FOS
n_hlf = 180/inc  # half n_max

n_th = (60/inc)+1  # number of theta samples for FZ
n_p1 = 360/inc  # number of phi1 samples for FZ
n_P = (90/inc)+1  # number of Phi samples for FZ
n_p2 = 60/inc  # number of phi2 samples for FZ

a = .0064  # start of range for legendre interpolation
b = .0096  # end of range for legendre interpolation

# number of samples for the fourier representation of the legendre polynomial
N = 11

# collect the simulation data by tensor id

st = time.time()

chunk = np.zeros([n_th, n_p1, n_P, n_p2, N])

for tt in xrange(n_th):

    # create file for pre-database outputs
    f = h5py.File('coeff_extract_%s.hdf5' % str(tt+1).zfill(2), 'r')

    ep_tmp = f.get("ep_set")

    chunk[tt, ...] = ep_tmp

    f.close()

# collect into final form before fft

pre_fft = np.zeros([40, n_max, n_max, n_max, N])

# insert chunk into pre_fft with correct symmetric arrangement so that the
# first dimension has angles ranging from 0:115 degrees and the remaining
# three have angles ranging from 0:355

# fill the theta 0:60, phi1 0:360, Phi 0:90, phi2: 0:60 degree zone
pre_fft[:n_th, :, :n_P, :n_p2, :] = chunk

# fill the theta 0:60, phi1 0:360, Phi 90:180, phi2: 0:60 degree zone
tmp = np.roll(chunk[:, :, ::-1, ::-1, :], n_hlf, 1)
pre_fft[:n_th, :, n_P:n_hlf+1, :n_p2, :] = tmp[:, :, 1:, :, :]
del tmp

# fill the theta 0:60, phi1 0:360, Phi 180:360, phi2: 0:60 degree zone
tmp = pre_fft[:n_th, :, :n_hlf, :n_p2, :]
tmp = tmp[:, :, ::-1, :, :]
pre_fft[:n_th, :, n_hlf+1:, :n_p2, :] = tmp[:, :, 1:, :, :]
del tmp

# fill the theta 0:120, phi1 0:360, Phi 0:360, phi2: 0:60 degree zone
tmp = pre_fft[1:n_th-1, :, :, :n_p2, :]
pre_fft[n_th:, :, :, :n_p2, :] = tmp[::-1, ...]
del tmp

# fill the theta 0:120, phi1 0:360, Phi 0:360, phi2: 60:360 degree zone
tmp = pre_fft[:, :, :, :n_p2, :]
pre_fft[:, :, :, 1*n_p2:2*n_p2, :] = tmp
pre_fft[:, :, :, 2*n_p2:3*n_p2, :] = tmp
pre_fft[:, :, :, 3*n_p2:4*n_p2, :] = tmp
pre_fft[:, :, :, 4*n_p2:5*n_p2, :] = tmp
pre_fft[:, :, :, 5*n_p2:, :] = tmp
del tmp

np.save("pre_fft.npy", pre_fft)

# how large is pre_fft?
print "size of pre_fft: %s gb" % np.round(pre_fft.nbytes/(1E9), decimals=2)

print "time to prepare for fft: %ss" % np.round(time.time()-st, decimals=5)

st = time.time()

# perform the fft on the first 4 dimensions of pre_fft
db_fft = np.fft.fftn(pre_fft, axes=(0, 1, 2, 3))

del chunk, pre_fft

print "time to take fft: %ss" % np.round(time.time()-st, decimals=5)

# sh is the shape of the dft itself, the last dimension for the
# legendre root values are not included
sh = db_fft.shape[:-1]
sz = np.prod(sh)

# center the fft s.t. the 0th frequency is centered
db_fft = np.fft.fftshift(db_fft, axes=(0, 1, 2, 3)).reshape([sz, N])

# find half of the range for each dimension in the fft
kmax = np.int8(np.floor(np.array(sh)/2.))
kmax = np.expand_dims(kmax, 1)

# generate indices associated with the fft
INDX = np.unravel_index(np.arange(sz), sh)
# array containing indices associated with the fft
INDX = np.transpose(np.array(INDX) - kmax)

fftsum = np.sum(np.abs(db_fft), axis=1)

# amplitude of frequency with max amplitude
maxf = np.max(fftsum)

# find the indices of fft frequencies with magnitudes greater than .25% of
# the largest value of the fft
gt_p25 = fftsum > 0.0 * maxf

s_list = INDX[gt_p25, :]
f_list = db_fft[gt_p25, :]


print 'shape of s_list:'
print s_list.shape
print 'shape of f_list:'
print f_list.shape
print 'sz size'
print sz
ratio = (np.float64(f_list.shape[0])/np.float64(sz))*100
print 'percentage of frequencies retained from fft: %s%%' % ratio

# save s_list and f_list to hdf5 file

f_db = h5py.File('final_db.hdf5', 'w')

f_db.create_dataset("s_list", data=s_list)
f_db.create_dataset("f_list", data=f_list)

f_db.close()
