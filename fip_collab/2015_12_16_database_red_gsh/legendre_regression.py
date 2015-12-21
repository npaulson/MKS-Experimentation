import numpy as np
import numpy.polynomial.legendre as leg
import itertools as it
import matplotlib.pyplot as plt
import h5py
import time
from mpl_toolkits.mplot3d import Axes3D


def real2comm(x, a, b):
    return 2*((x-a)/(b-a))-1


def comm2real(x, a, b):
    return 0.5*(x+1)*(b-a)+a


inc = 6
n_p1 = 360/inc  # number of phi1 samples for FZ
n_P = (90/inc)+1  # number of Phi samples for FZ
n_p2 = 60/inc  # number of phi2 samples for FZ
en = 0.0085

N_p1 = 25
N_p = 8
N_p2 = 8

f = h5py.File('var_extract.hdf5', 'r')
var_set = f.get('var_set')
print "var_set shape: %s" % str(var_set.shape)

# note that these angular variables are rescaled between -1 and 1

phi1_lt_pi = var_set[:, 0] < np.pi

phi1 = np.float64(var_set[phi1_lt_pi, 0])
phi = np.float64(var_set[phi1_lt_pi, 1])
phi2 = np.float64(var_set[phi1_lt_pi, 2])
Y = np.float64(var_set[phi1_lt_pi, 3])

f.close

# note that these angular variables are rescaled between -1 and 1
phi1_c = real2comm(phi1, 0, 2*np.pi)
phi_c = real2comm(phi, 0, np.pi/2.)
phi2_c = real2comm(phi2, 0, np.pi/3.)

""" Calculate X """

st = time.time()

cmax = N_p1*N_p*N_p2
print "cmax: %s" % cmax

X = np.zeros((phi1.shape[0], cmax), dtype='float64')

for ii in xrange(cmax):

    if np.mod(ii, 100) == 0:
        print ii

    [p, q, r] = np.unravel_index(ii, [N_p1, N_p, N_p2])

    p_vec = np.zeros(p+1)
    p_vec[p] = 1

    q_vec = np.zeros(q+1)
    q_vec[q] = 1

    r_vec = np.zeros(r+1)
    r_vec[r] = 1

    X[:, ii] = leg.legval(phi1_c, p_vec) * \
        leg.legval(phi_c, q_vec) * \
        leg.legval(phi2_c, r_vec)

print "basis evaluation complete: %ss" % np.round(time.time()-st, 3)

""" Calculate XhX """

tmp = it.combinations_with_replacement(np.arange(cmax), 2)
Imat = np.array(list(tmp))
ImatL = Imat.shape[0]

XhX = np.zeros((cmax, cmax), dtype='float64')

for I in xrange(ImatL):

    ii, jj = Imat[I, :]

    if np.mod(I, (cmax**2)/10) == 0:
        print I

    dotvec = np.dot(X[:, ii].conj(), X[:, jj])

    if ii == jj:
        XhX[ii, ii] = dotvec
    else:
        XhX[ii, jj] = dotvec
        XhX[jj, ii] = dotvec

print "rank(XhX): %s" % np.linalg.matrix_rank(XhX)

plt.figure(1)

plt.subplot(121)

ax = plt.imshow(np.real(XhX), origin='lower',
                interpolation='none', cmap='jet')
plt.title("real(XhX): GSH")
plt.colorbar(ax)

plt.subplot(122)

ax = plt.imshow(np.imag(XhX), origin='lower',
                interpolation='none', cmap='jet')
plt.title("imag(XhX): GSH")
plt.colorbar(ax)

plt.show()

""" Calculate XhY """

XhY = np.zeros(cmax, dtype='float64')

for ii in xrange(cmax):
    XhY[ii] = np.dot(X[:, ii].conj(), Y)

""" Perform the regression """

coeff = np.linalg.solve(XhX, XhY)
print "coefficients from regression: %s\n" % str(coeff)

""" Check the regression accuracy """

# Y_ is the set of predictions from the regression fit for the calibration
# data points
Y_ = np.zeros(Y.shape, dtype='float64')

for ii in xrange(cmax):
    [p, q, r] = np.unravel_index(ii, [N_p1, N_p, N_p2])

    p_vec = np.zeros(p+1)
    p_vec[p] = 1

    q_vec = np.zeros(q+1)
    q_vec[q] = 1

    r_vec = np.zeros(r+1)
    r_vec[r] = 1

    Y_ += coeff[ii] * \
        leg.legval(phi1_c, p_vec) * \
        leg.legval(phi_c, q_vec) * \
        leg.legval(phi2_c, r_vec)

print "min(Y): %s" % np.min(Y)
print "mean(Y): %s" % np.mean(Y)
print "max(Y): %s" % np.max(Y)
print "\n"

error = np.abs(np.real(Y_) - Y)

print "mean error: %s" % np.mean(error)
print "std of error: %s" % np.std(error)
print "max error: %s" % np.max(error)

""" Plot the regression results """

ang_vec = np.unique(phi2)
print ang_vec

ang_sel = phi2 == ang_vec[7]

fig = plt.figure(num=2, figsize=[10, 6])
ax = fig.add_subplot(111, projection='3d')

ax.scatter(phi1[ang_sel], phi[ang_sel], Y[ang_sel], c='b')
# ax.scatter(phi1[ang_sel], phi2[ang_sel], Y[ang_sel], c='b')


fig = plt.figure(num=3, figsize=[10, 6])
ax = fig.add_subplot(111, projection='3d')

ax.scatter(phi1[ang_sel], phi[ang_sel], Y_[ang_sel], c='r')
# ax.scatter(phi1[ang_sel], phi2[ang_sel], Y_[ang_sel], c='r')

plt.show()
