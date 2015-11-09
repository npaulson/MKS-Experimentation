import numpy as np
import h5py
import sys
import time

"""
This code is designed to arrange simulation database chunks, take the fft and
select the frequencies with the highest magnitudes

"""

# initialize important variables

# define the number of increments for angular variables:

inc = 5  # degree increment for angular variables

n_th_max = 120/inc  # number of theta samples in FOS
n_max = 360/inc  # number of phi1, Phi and phi2 samples in FOS
n_hlf = 180/inc  # half n_max

n_th = (60/inc)+1  # number of theta samples for FZ
n_p1 = 360/inc  # number of phi1 samples for FZ
n_P = (90/inc)+1  # number of Phi samples for FZ
n_p2 = 60/inc  # number of phi2 samples for FZ

a = .0064  # start of range for legendre interpolation
b = .0096  # end of range for legendre interpolation

# collect the simulation data by tensor id

st = time.time()

chunk = np.zeros([n_th, n_max, n_max, n_max])

for tt in xrange(n_th):

    # create file for pre-database outputs
    f = h5py.File('stress_extract_%s.hdf5' % str(tt+1).zfill(2), 'r')

    sig_tmp = f.get("sig_set")

    chunk[tt, ...] = sig_tmp

    f.close()

# collect into final form before fft

pre_fft = np.zeros([n_th_max, n_max, n_max, n_max])

# insert chunk into pre_fft with correct symmetric arrangement so that the
# first dimension has angles ranging from 0:115 degrees and the remaining
# three have angles ranging from 0:355
pre_fft[0:n_th, ...] = chunk  # 0 to 60 deg
pre_fft[n_th:n_th_max, ...] = np.flipud(chunk[1:n_th-1, ...])  # 65 to 115 deg

np.save("pre_fft_5deg_stress.npy", pre_fft)

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
sh = db_fft.shape
sz = np.prod(sh)

# center the fft s.t. the 0th frequency is centered
db_fft = np.fft.fftshift(db_fft, axes=(0, 1, 2, 3)).reshape(sz)

# find half of the range for each dimension in the fft
kmax = np.int8(np.floor(np.array(sh)/2.))
kmax = np.expand_dims(kmax, 1)

# generate indices associated with the fft
INDX = np.unravel_index(np.arange(sz), sh)
# array containing indices associated with the fft
INDX = np.transpose(np.array(INDX) - kmax)

# amplitude of frequency with max amplitude
maxf = np.max(np.abs(db_fft))

# find the indices of fft frequencies with magnitudes greater than .25% of
# the largest value of the fft
gt_p25 = np.abs(db_fft) > 0.0 * maxf

s_list = INDX[gt_p25, :]
f_list = db_fft[gt_p25]


print 'shape of s_list:'
print s_list.shape
print 'shape of f_list:'
print f_list.shape
ratio = (np.float64(f_list.shape[0])/np.float64(sz))*100
print 'percentage of frequencies retained from fft: %s%%' % ratio

# save s_list and f_list to hdf5 file

f_db = h5py.File('final_db_5deg_stress.hdf5', 'w')

f_db.create_dataset("s_list", data=s_list)
f_db.create_dataset("f_list", data=f_list)

f_db.close()
