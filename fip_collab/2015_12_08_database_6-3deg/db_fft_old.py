import numpy as np
import h5py
import time

"""
This code is designed to arrange simulation database chunks, take the fft and
select the frequencies with the highest magnitudes

Important Acronyms:
FZ: hexagonal-triclinic fundamental zone
FOS: full euler orientation space (0-360 degree in each angle)
"""


def WP(msg, filename):
    """
    Summary:
        This function takes an input message and a filename, and appends that
        message to the file. This function also prints the message
    Inputs:
        msg (string): the message to write and print.
        filename (string): the full name of the file to append to.
    Outputs:
        both prints the message and writes the message to the specified file
    """
    fil = open(filename, 'a')
    print msg
    fil.write(msg)
    fil.write('\n')
    fil.close()


def check(s_list, f_list, xi, sz):

    Lset = np.array([120., 360., 360., 360.])*(np.pi/180.)

    st = time.time()

    Pvec = f_list[:, -1] * \
        np.exp((2*np.pi*1j*s_list[:, 0]*xi[0])/Lset[0]) * \
        np.exp((2*np.pi*1j*s_list[:, 1]*xi[1])/Lset[1]) * \
        np.exp((2*np.pi*1j*s_list[:, 2]*xi[2])/Lset[2]) * \
        np.exp((2*np.pi*1j*s_list[:, 3]*xi[3])/Lset[3])

    db_res = np.real(np.sum(Pvec, 0)/sz)

    interp_time = time.time()-st

    return db_res, interp_time


""" initialize important variables """

fname = "fip_results_6deg.txt"

inc = 6  # degree increment for angular variables

n_th_max = 120/inc  # number of theta samples in FOS
n_max = 360/inc  # number of phi1, Phi and phi2 samples in FOS
n_hlf = 180/inc  # half n_max

n_th = (60/inc)+1  # number of theta samples for FZ
n_p1 = 360/inc  # number of phi1 samples for FZ
n_P = (90/inc)+1  # number of Phi samples for FZ
n_p2 = 60/inc  # number of phi2 samples for FZ

# number of samples for the largrange polynomial
n_en = 10

""" collect the simulation data by tensor id """

st = time.time()

chunk = np.zeros([n_th, n_p1, n_P, n_p2, n_en])

for tt in xrange(n_th):

    # create file for pre-database outputs
    f = h5py.File('var_extract_%s.hdf5' % str(tt+1).zfill(2), 'r')

    var_tmp = f.get("var_set")

    chunk[tt, ...] = var_tmp

    f.close()

# collect into final form before fft

pre_fft = np.zeros([n_th_max, n_max, n_max, n_max, n_en])

""" insert chunk into pre_fft with correct symmetric arrangement so that
the first dimension has angles ranging from 0:115 degrees and the remaining
three have angles ranging from 0:355 """

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
msg = "size of pre_fft: %s gb" % np.round(pre_fft.nbytes/(1E9), decimals=2)
WP(msg, fname)

msg = "time to prepare for fft: %ss" % np.round(time.time()-st, decimals=5)
WP(msg, fname)

""" set up the test interpolation results """

# point for test interpolation in degrees
xi_deg = np.array([30., 30., 30., 30.])
xi_rad = xi_deg * (np.pi/180.)
# indices for test interpolation
xi = xi_deg/inc
# variable of interest value for test interpolation location
act_res = pre_fft[xi[0], xi[1], xi[2], xi[3], -1]

""" perform the fft on the first 4 dimensions of pre_fft """

st = time.time()

db_fft = np.fft.fftn(pre_fft, axes=(0, 1, 2, 3))

del chunk, pre_fft

msg = "time to take fft: %ss" % np.round(time.time()-st, decimals=5)
WP(msg, fname)

""" shape and sort the data for use in trigonometric interpolation """

# sh is the shape of the dft itself, the last dimension for the
# legendre root values are not included

sh = db_fft.shape[:-1]
sz = np.prod(sh)

# center the fft s.t. the 0th frequency is centered
db_fft = np.fft.fftshift(db_fft, axes=(0, 1, 2, 3)).reshape([sz, n_en])

# find half of the range for each dimension in the fft
kmax = np.int64(np.floor(np.array(sh)/2.))
kmax = np.expand_dims(kmax, 1)

# generate indices associated with the fft
INDX = np.unravel_index(np.arange(sz), sh)
# array containing indices associated with the fft
INDX = np.transpose(np.array(INDX) - kmax)

fftsum = np.sum(np.abs(db_fft), axis=1)

# amplitude of frequency with max amplitude
maxf = np.max(fftsum)

""" perform quick characterization of database at
different trunctation levels """

ret_list = np.array([1, .1, .01, .001, .0005, .0001, 0])*0.01
for pct in ret_list:

    gt_p25 = fftsum > pct * maxf

    s_list = INDX[gt_p25, :]
    f_list = db_fft[gt_p25, :]

    db_res, interp_time = check(s_list, f_list, xi_rad, sz)

    ratio = (np.float64(f_list.shape[0])/np.float64(sz))*100

    msg = "frequency threshold: %s%%" % (pct*100)
    WP(msg, fname)
    msg = "percentage of frequencies retained from fft: %s%%" % ratio
    WP(msg, fname)
    msg = "actual value: %s" % act_res
    WP(msg, fname)
    msg = "guess value: %s" % db_res
    WP(msg, fname)
    msg = "interpolation time: %ss" % interp_time
    WP(msg, fname)

    err = np.abs(act_res - db_res)

    msg = "interpolation error: %s" % err
    WP(msg, fname)
    msg = "number of frequencies retained: %s" % f_list.shape[0]
    WP(msg, fname)

    if pct == .001*.01:
        f_db = h5py.File('final_db.hdf5', 'w')
        f_db.create_dataset("s_list", data=s_list)
        f_db.create_dataset("f_list", data=f_list)
        f_db.close()
