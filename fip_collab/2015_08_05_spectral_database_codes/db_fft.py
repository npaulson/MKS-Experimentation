import numpy as np
import h5py
import sys
import time

"""
This code is designed to arrange simulation database chunks, take the fft and
select the frequencies with the highest magnitudes

"""

# initialize important variables

tnum = sys.argv

comp = "11"  # strain component of interest

n_theta = 13  # number of theta samples
n_phi1 = 72  # number of phi1 samples
n_Phi = 72  # number of Phi samples
n_phi2 = 72  # number of phi2 samples

a = .0064  # start of range for legendre interpolation
b = .0096  # end of range for legendre interpolation

# highest order legendre polynomial in the fourier representation
N = 10

# collect the simulation data by tensor id

st = time.time()

chunk = np.zeros([13, n_phi1, n_Phi, n_phi2, N+1])

for tt in xrange(n_theta):

    # create file for pre-database outputs
    f = h5py.File('coeff_extract_%s.hdf5' % str(tt+1).zfill(2), 'r')

    ep_tmp = f.get("ep_set")

    chunk[tt, ...] = ep_tmp

    f.close()

# collect into final form before fft

pre_fft = np.zeros([24, n_phi1, n_Phi, n_phi2, N+1])

# insert chunk into pre_fft with correct symmetric arrangement so that the
# first dimension has angles ranging from 0:115 degrees and the remaining
# three have angles ranging from 0:355
pre_fft[0:13, ...] = chunk  # 0 to 60 deg
pre_fft[13:24, ...] = np.flipud(chunk[1:12, ...])  # 65 to 115 deg
# pre_fft[24:37, ...] = chunk  # 120 to 180 deg
# pre_fft[37:48, ...] = np.flipud(chunk[1:12, ...])  # 185 to 235 deg
# pre_fft[48:61, ...] = chunk  # 240 to 300 deg
# pre_fft[61:72, ...] = np.flipud(chunk[1:12, ...])  # 305 to 355 deg

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
db_fft = np.fft.fftshift(db_fft, axes=(0, 1, 2, 3)).reshape([sz, N+1])

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
ratio = (np.float64(f_list.shape[0])/np.float64(sz))*100
print 'percentage of frequencies retained from fft: %s%%' % ratio

# save s_list and f_list to hdf5 file

f_db = h5py.File('final_db.hdf5', 'w')

f_db.create_dataset("s_list", data=s_list)
f_db.create_dataset("f_list", data=f_list)

f_db.close()
