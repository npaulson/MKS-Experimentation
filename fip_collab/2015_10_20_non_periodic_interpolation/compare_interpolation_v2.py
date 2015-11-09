import h5py
import numpy as np
from scipy import interpolate
import leg_interp_func as leg
import lagr_interp_func as lagr
import spli_interp_func as spli
import trig_interp_func as trig
import matplotlib.pyplot as plt

"""
This code compares the accuracy versus number of nodes required for
four different interpolation techniques
"""

# define the number of increments for angular variables:

inc = 3  # degree increment for angular variables

n_th_max = 120/inc  # number of theta samples in FOS
n_max = 360/inc  # number of phi1, Phi and phi2 samples in FOS
n_hlf = 180/inc  # half n_max

n_th = (60/inc)+1  # number of theta samples for FZ
n_p1 = 360/inc  # number of phi1 samples for FZ
n_P = (90/inc)+1  # number of Phi samples for FZ
n_p2 = 60/inc  # number of phi2 samples for FZ

N_samp = 100
width = 4 + 2*(100-59)

N_tot = N_samp*n_th

alldata = np.zeros([N_tot, width])

for tt in xrange(n_th):

    # create file for pre-database outputs
    f = h5py.File('samp_interp_test_%s.hdf5' % str(tt+1).zfill(2), 'r')

    ep_tmp = f.get("ep_set")

    alldata[tt*N_samp:(tt+1)*N_samp, ...] = ep_tmp

    f.close()

a = .0060  # start of range for legendre interpolation
b = .0100  # end of range for legendre interpolation

st_e = 0.0001

# the following vector closely matches that of et_norm
etvec = np.arange(a, b + st_e, st_e)

ai = np.int8(np.round(a/st_e))-1
bi = np.int8(np.round(b/st_e))-1

# for legendre and lagrange interpolation these sets refer to total
# numbers of nodes
leg_set = np.array([4, 5, 6, 7, 8, 9, 10, 15, 20])
leg_error = np.zeros([leg_set.size, N_tot, 100-59])
Nvec_leg = np.zeros(leg_set.size)

lagr_set = np.array([4, 5, 6, 7, 8, 9, 10, 15, 20])
lagr_error = np.zeros([lagr_set.size, N_tot, 100-59])
Nvec_lagr = np.zeros(lagr_set.size)

spli_set = np.array([1, 2, 3, 4, 5, 6, 8, 10])
spli_error = np.zeros([spli_set.size, N_tot, 100-59])
Nvec_spli = np.zeros(spli_set.size)

trig_set = np.array([1, 2, 3, 4, 5, 6, 7, 9, 11])
trig_error = np.zeros([trig_set.size, N_tot, 100-59])
Nvec_trig = np.zeros(trig_set.size)


for ii in xrange(N_tot):

    xvar = alldata[ii, 4:45]
    yvar = alldata[ii, 45:86]

    c = 0
    for N in leg_set:

        xnode, ynode, weights = leg.get_nodes(etvec, yvar, a, b, N)

        coeff_set = leg.get_coeff(xnode, ynode, weights, N)

        ytest = leg.get_interp(xvar, coeff_set, a, b)

        # calculate error in this approach based on sampled values
        error = np.abs(yvar - ytest)*1E6

        leg_error[c, ii, :] = error

        Nvec_leg[c] = N

        c += 1

    c = 0
    for N in lagr_set:

        xnode, ynode = lagr.select_nodes(a, b, ai, bi, st_e, N, etvec, yvar)

        ytest = lagr.lagrange_interp(xnode, ynode, xvar)

        # calculate error in this approach based on sampled values
        error = np.abs(yvar - ytest)*1E6

        lagr_error[c, ii, :] = error

        Nvec_lagr[c] = N

        c += 1

    c = 0
    for st_i in spli_set:

        tck, ai, bi, xnode, ynode = \
            spli.interp_prep(ai, bi, st_e, st_i, etvec, yvar)

        N = xnode.size

        ytest = interpolate.splev(xvar, tck, der=0)

        # calculate error in this approach based on sampled values
        error = np.abs(yvar - ytest)*1E6

        spli_error[c, ii, :] = error

        Nvec_spli[c] = N

        c += 1

    c = 0
    for st_i in trig_set:

        [xnode, ynode, etvecS, etvecE, N, L] = \
            trig.mirror_inputs(yvar, a, ai, bi, st_i, st_e)

        ytest = trig.pretrig(xvar, ynode, etvecS, N, L)

        # calculate error in this approach based on sampled values
        error = np.abs(yvar - ytest)*1E6

        trig_error[c, ii, :] = error

        Nvec_trig[c] = N

        c += 1


plt.figure(num=1, figsize=[10, 6])

mean = np.mean(trig_error, axis=(1, 2))
std = np.std(trig_error, axis=(1, 2))
plt.errorbar(Nvec_trig, mean, yerr=std)

mean = np.mean(lagr_error, axis=(1, 2))
std = np.std(lagr_error, axis=(1, 2))
plt.errorbar(Nvec_lagr, mean, yerr=std)

mean = np.mean(spli_error, axis=(1, 2))
std = np.std(spli_error, axis=(1, 2))
plt.errorbar(Nvec_spli, mean, yerr=std)

mean = np.mean(leg_error, axis=(1, 2))
std = np.std(leg_error, axis=(1, 2))
plt.errorbar(Nvec_leg, mean, yerr=std)

# plt.axis([3.0, 21.0, -0.01, 0.07])
plt.title("Error in interpolation versus number of nodes")
plt.xlabel("number of interpolation nodes")
plt.ylabel("mean error in $\epsilon_{p}$ (ppm)")

plt.figure(num=2, figsize=[10, 6])

mean = np.mean(trig_error, axis=(1, 2))
trig, = plt.plot(Nvec_trig, mean, "rx-")

mean = np.mean(lagr_error, axis=(1, 2))
lagr, = plt.plot(Nvec_lagr, mean, "gx-")

mean = np.mean(spli_error, axis=(1, 2))
spli, = plt.plot(Nvec_spli, mean, "bx-")

mean = np.mean(leg_error, axis=(1, 2))
leg, = plt.plot(Nvec_leg, mean, "kx-")

plt.legend([trig, lagr, spli, leg],
           ["trigonometric", "lagrange", "spline", "legendre"])

plt.title("Mean error in interpolation methods versus number of nodes")
plt.xlabel("number of interpolation nodes")
plt.ylabel("mean error in $\epsilon_{p}$ (ppm)")

plt.figure(num=3, figsize=[10, 6])

std = np.std(trig_error, axis=(1, 2))
trig, = plt.plot(Nvec_trig, std, "rx-")

std = np.std(lagr_error, axis=(1, 2))
lagr, = plt.plot(Nvec_lagr, std, "gx-")

std = np.std(spli_error, axis=(1, 2))
spli, = plt.plot(Nvec_spli, std, "bx-")

std = np.std(leg_error, axis=(1, 2))
leg, = plt.plot(Nvec_leg, std, "kx-")

plt.legend([trig, lagr, spli, leg],
           ["trigonometric", "lagrange", "spline", "legendre"])

plt.title("Standard deviation of error in interpolation methods versus number of nodes")
plt.xlabel("number of interpolation nodes")
plt.ylabel("standard deviation of error in $\epsilon_{p}$ (ppm)")

plt.show()
