import h5py
import sys
import time
import numpy as np
import check_test_5deg as cdb

"""
This code is designed to arrange simulation database chunks, take the fft and
select the frequencies with the highest magnitudes

Important Acronyms:
FZ: hexagonal-triclinic fundamental zone
FOS: full euler orientation space (0-360 degree in each angle)

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

# number of samples for the fourier representation of the lagrange polynomial
N = 10

# collect the simulation data by tensor id

st = time.time()

chunk = np.zeros([n_th, n_max, n_max, n_max, N])

for tt in xrange(n_th):

    # create file for pre-database outputs
    f = h5py.File('fip_extract_%s.hdf5' % str(tt+1).zfill(2), 'r')

    fip_tmp = f.get("fip_set")

    chunk[tt, ...] = fip_tmp

    f.close()

# collect into final form before fft

pre_fft = np.zeros([24, n_max, n_max, n_max, N])

# insert chunk into pre_fft with correct symmetric arrangement so that the
# first dimension has angles ranging from 0:115 degrees and the remaining
# three have angles ranging from 0:355
pre_fft[0:13, ...] = chunk  # 0 to 60 deg
pre_fft[13:24, ...] = np.flipud(chunk[1:12, ...])  # 65 to 115 deg

np.save("pre_fft.npy", pre_fft)

# how large is pre_fft?
print "size of pre_fft: %s gb" % np.round(pre_fft.nbytes/(1E9), decimals=2)

print "time to prepare for fft: %ss" % np.round(time.time()-st, decimals=5)

st = time.time()

# pre_fft = np.load("pre_fft_5deg.npy")

# perform the fft on the first 4 dimensions of pre_fft
db_fft = np.fft.fftn(pre_fft, axes=(0, 1, 2, 3))
act_res = pre_fft[3, 3, 3, 3, -1]

del pre_fft

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

ret_list = np.array([1, .1, .01, .001, .0005, .0001, 0])*0.01

for pct in ret_list:

    gt_p25 = fftsum > pct * maxf

    s_list = INDX[gt_p25, :]
    f_list = db_fft[gt_p25, :]

    db_res, interp_time = cdb.check(s_list, f_list)

    # print f_list.shape

    ratio = (np.float64(f_list.shape[0])/np.float64(sz))*100

    print "frequency threshold: %s%%" % (pct*100)
    print "percentage of frequencies retained from fft: %s%%" % ratio
    print "actual value: %s" % act_res
    print "guess value: %s" % db_res
    print "interpolation time: %ss" % interp_time

    err = np.abs(act_res - db_res) * 1E6

    print "interpolation error: %s (in ppm)" % err
    print "number of frequencies retained: %s" % f_list.shape[0]
