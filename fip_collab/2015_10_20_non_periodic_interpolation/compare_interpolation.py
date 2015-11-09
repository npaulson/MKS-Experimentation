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

n_tot = n_p1 * n_P * n_p2  # total number of orientations

N_samp = 100
width = 4 + 2*(100-59)

alldata = np.zeros([N_samp*n_th, width])

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


"""
Check if etnorm depends on orientation
"""
print np.unique(np.round(alldata[:, 44], 8))

"""
Check Legendre interpolation error
"""
# for legendre and lagrange interpolation these sets refer to total
# numbers of nodes
leg_set = np.array([4, 5, 6, 7, 8, 9, 10, 15, 20])
leg_error = np.zeros([leg_set.size, 9])

c = 0

for N in leg_set:
    mean_err = np.zeros(N_samp*n_th)
    max_err = np.zeros(N_samp*n_th)

    for ii in xrange(N_samp*n_th):

        xvar = alldata[ii, 4:45]
        yvar = alldata[ii, 45:86]

        xnode, ynode, weights = leg.get_nodes(etvec, yvar, a, b, N)

        coeff_set = leg.get_coeff(xnode, ynode, weights, N)

        ytest = leg.get_interp(xvar, coeff_set, a, b)

        # calculate error in this approach based on sampled values
        error = 100*np.abs((yvar - ytest)/xvar)

        # if N == 6 and ii > .3*N_samp*n_th:
        #     print np.mean(error)
        #     plt.figure(num=1, figsize=[10, 6])
        #     plt.plot(xvar, yvar, 'bx')
        #     plt.plot(etvec, ytest, 'r')
        #     plt.show()

        mean_err[ii] = np.mean(error)
        max_err[ii] = np.max(error)

    leg_error[c, :] = np.array([N,
                                np.mean(mean_err),
                                np.std(mean_err),
                                np.min(mean_err),
                                np.max(mean_err),
                                np.mean(max_err),
                                np.std(max_err),
                                np.min(max_err),
                                np.max(max_err)])

    c += 1

"""
Check Lagrange interpolation error
"""

lagr_set = np.array([4, 5, 6, 7, 8, 9, 10, 15, 20])
lagr_error = np.zeros([lagr_set.size, 9])

c = 0
err_bench = 0.0

for N in lagr_set:
    mean_err = np.zeros(N_samp*n_th)
    max_err = np.zeros(N_samp*n_th)

    for ii in xrange(N_samp*n_th):

        xvar = alldata[ii, 4:45]
        yvar = alldata[ii, 45:86]

        xnode, ynode = lagr.select_nodes(a, b, ai, bi, st_e, N, etvec, yvar)

        ytest = lagr.lagrange_interp(xnode, ynode, xvar)

        # calculate error in this approach based on sampled values
        error = 100*np.abs((yvar - ytest)/xvar)

        # # if st_i == 4 and ii > 0.0*N_samp*n_th:
        # if np.mean(error) > err_bench:
        #     err_bench = np.mean(error)
        #     print np.mean(error)
        #     plt.figure(num=1, figsize=[10, 6])
        #     plt.plot(xvar, yvar, 'bx')
        #     plt.plot(etvec, ytest, 'r')
        #     plt.show()

        mean_err[ii] = np.mean(error)
        max_err[ii] = np.max(error)

    lagr_error[c, :] = np.array([N,
                                 np.mean(mean_err),
                                 np.std(mean_err),
                                 np.min(mean_err),
                                 np.max(mean_err),
                                 np.mean(max_err),
                                 np.std(max_err),
                                 np.min(max_err),
                                 np.max(max_err)])

    c += 1

# for interpolation with splines and with trigonometric interpolation
# these sets contain node spacing

"""
Check Lagrange interpolation error
"""
spli_set = np.array([1, 2, 3, 4, 5, 6, 8, 10])
spli_error = np.zeros([spli_set.size, 9])

c = 0
err_bench = 0.0


for st_i in spli_set:
    mean_err = np.zeros(N_samp*n_th)
    max_err = np.zeros(N_samp*n_th)

    for ii in xrange(N_samp*n_th):

        xvar = alldata[ii, 4:45]
        yvar = alldata[ii, 45:86]

        tck, ai, bi, xnode, ynode = spli.interp_prep(ai,
                                                     bi,
                                                     st_e,
                                                     st_i,
                                                     etvec,
                                                     yvar)

        N = xnode.size

        ytest = interpolate.splev(xvar, tck, der=0)

        # calculate error in this approach based on sampled values
        error = 100*np.abs((yvar - ytest)/xvar)

        # # if st_i == 4 and ii > 0.0*N_samp*n_th:
        # if np.mean(error) > err_bench:
        #     err_bench = np.mean(error)
        #     print np.mean(error)
        #     plt.figure(num=1, figsize=[10, 6])
        #     plt.plot(xvar, yvar, 'bx')
        #     plt.plot(etvec, ytest, 'r')
        #     plt.show()

        mean_err[ii] = np.mean(error)
        max_err[ii] = np.max(error)

    spli_error[c, :] = np.array([N,
                                 np.mean(mean_err),
                                 np.std(mean_err),
                                 np.min(mean_err),
                                 np.max(mean_err),
                                 np.mean(max_err),
                                 np.std(max_err),
                                 np.min(max_err),
                                 np.max(max_err)])

    c += 1

"""
Check Trigonometric interpolation error
"""

trig_set = np.array([1, 2, 3, 4, 5, 6, 7, 9, 11])
trig_error = np.zeros([trig_set.size, 9])

c = 0
err_bench = 0.0


for st_i in trig_set:
    mean_err = np.zeros(N_samp*n_th)
    max_err = np.zeros(N_samp*n_th)

    for ii in xrange(N_samp*n_th):

        xvar = alldata[ii, 4:45]
        yvar = alldata[ii, 45:86]

        [xnode, ynode, etvecS, etvecE, N, L] = \
            trig.mirror_inputs(yvar, a, ai, bi, st_i, st_e)

        ytest = trig.pretrig(xvar, ynode, etvecS, N, L)

        # calculate error in this approach based on sampled values
        error = 100*np.abs((yvar - ytest)/xvar)

        # # if st_i == 4 and ii > 0.0*N_samp*n_th:
        # if np.mean(error) > err_bench:
        #     err_bench = np.mean(error)
        #     print np.mean(error)
        #     plt.figure(num=1, figsize=[10, 6])
        #     plt.plot(xvar, yvar, 'bx')
        #     plt.plot(etvec, ytest, 'r')
        #     plt.show()

        mean_err[ii] = np.mean(error)
        max_err[ii] = np.max(error)

    trig_error[c, :] = np.array([N,
                                 np.mean(mean_err),
                                 np.std(mean_err),
                                 np.min(mean_err),
                                 np.max(mean_err),
                                 np.mean(max_err),
                                 np.std(max_err),
                                 np.min(max_err),
                                 np.max(max_err)])

    c += 1

plt.figure(num=1, figsize=[10, 6])

minerr = lagr_error[:, 1]-lagr_error[:, 3]
print minerr.shape
maxerr = lagr_error[:, 4]-lagr_error[:, 1]
print maxerr.shape
plt.errorbar(lagr_error[:, 0]+.1,
             lagr_error[:, 1],
             yerr=[minerr, maxerr])

minerr = leg_error[:, 1]-leg_error[:, 3]
maxerr = leg_error[:, 4]-leg_error[:, 1]
plt.errorbar(leg_error[:, 0]+.3,
             leg_error[:, 1],
             yerr=[minerr, maxerr])

minerr = spli_error[:, 1]-spli_error[:, 3]
maxerr = spli_error[:, 4]-spli_error[:, 1]
plt.errorbar(spli_error[:, 0]-.1,
             spli_error[:, 1],
             yerr=[minerr, maxerr])

minerr = trig_error[:, 1]-trig_error[:, 3]
maxerr = trig_error[:, 4]-trig_error[:, 1]
plt.errorbar(trig_error[:, 0]+.3,
             trig_error[:, 1],
             yerr=[minerr, maxerr])

# plt.legend([trig, lagr, spli, leg],
#            ["trigonometric", "lagrange", "spline", "legendre"])

# plt.axis([3.0, 21.0, -0.01, 0.07])
plt.title("Error in interpolation versus number of nodes")
plt.xlabel("N, number of interpolation nodes")
plt.ylabel("% mean error")

# plt.figure(num=1, figsize=[10, 6])

# print trig_error[:, 2]
# print trig_error[:, 2].shape

# trig, = plt.errorbar(trig_error[:, 0],
#                      trig_error[:, 1],
#                      yerr=trig_error[:, 2])
# lagr, = plt.errorbar(lagr_error[:, 0],
#                      lagr_error[:, 1],
#                      yerr=lagr_error[:, 2])
# spli, = plt.errorbar(spli_error[:, 0],
#                      spli_error[:, 1],
#                      yerr=spli_error[:, 2])
# leg, = plt.errorbar(leg_error[:, 0],
#                     leg_error[:, 1],
#                     yerr=leg_error[:, 2])

# plt.legend([trig, lagr, spli, leg],
#            ["trigonometric", "lagrange", "spline", "legendre"])

# plt.axis([3.0, 21.0, -0.01, 0.07])
# plt.title("Error in interpolation versus number of nodes")
# plt.xlabel("N, number of interpolation nodes")
# plt.ylabel("% mean error")

plt.figure(num=2, figsize=[10, 6])

trig, = plt.plot(trig_error[:, 0], trig_error[:, 1], "rx-")
lagr, = plt.plot(lagr_error[:, 0], lagr_error[:, 1], "gx-")
spli, = plt.plot(spli_error[:, 0], spli_error[:, 1], "bx-")
leg, = plt.plot(leg_error[:, 0], leg_error[:, 1], "kx-")

plt.legend([trig, lagr, spli, leg],
           ["trigonometric", "lagrange", "spline", "legendre"])

plt.title("Mean error in interpolation methods versus number of nodes")
plt.xlabel("N, number of interpolation nodes")
plt.ylabel("% mean error")

plt.figure(num=3, figsize=[10, 6])

trig, = plt.plot(trig_error[:, 0], trig_error[:, 5], "rx-")
lagr, = plt.plot(lagr_error[:, 0], lagr_error[:, 5], "gx-")
spli, = plt.plot(spli_error[:, 0], spli_error[:, 5], "bx-")
leg, = plt.plot(leg_error[:, 0], leg_error[:, 5], "kx-")

plt.legend([trig, lagr, spli, leg],
           ["trigonometric", "lagrange", "spline", "legendre"])

plt.title("Maximum error in interpolation methods versus number of nodes")
plt.xlabel("N, number of interpolation nodes")
plt.ylabel("% maximum error")


plt.show()
