import numpy as np
import itertools as it
import matplotlib.pyplot as plt
import h5py
import time


inc = 3
n_th = (60/inc)+1  # number of theta samples for FZ
n_p1 = 360/inc  # number of phi1 samples for FZ
n_P = (90/inc)+1  # number of Phi samples for FZ
n_p2 = 60/inc  # number of phi2 samples for FZ
en = 0.0085

phi1max = 2*np.pi
phimax = np.pi/2.
phi2max = np.pi/3.

N_L = 21
L_th = 2.*np.pi/3.

sub2rad = inc*np.pi/180.

phi1 = np.int64(np.random.rand()*n_p1)*sub2rad
phi = np.int64(np.random.rand()*n_P)*sub2rad
phi2 = np.int64(np.random.rand()*n_p2)*sub2rad
angvec = np.array([phi1, phi, phi2])

print "random euler angles: %s" % str(angvec)

f = h5py.File('var_extract_total.hdf5', 'r')
var_set = f.get('var_set')[...]
print "var_set shape: %s" % str(var_set.shape)
f.close

eulvec = (var_set[:, 1] == phi1) * \
         (var_set[:, 2] == phi) * \
         (var_set[:, 3] == phi2) * \
         (var_set[:, 4] == en)

print np.sum(eulvec)

thvec = var_set[eulvec, 0]

Y = var_set[eulvec, -1]

""" Calculate X """

st = time.time()

X = np.zeros((n_th, N_L), dtype='float64')

for ii in xrange(N_L):
    X[:, ii] = np.cos(2*np.pi*ii*thvec/L_th)

print "basis evaluation complete: %ss" % np.round(time.time()-st, 3)

""" Calculate XhX """

tmp = it.combinations_with_replacement(np.arange(N_L), 2)
Imat = np.array(list(tmp))
ImatL = Imat.shape[0]

XhX = np.zeros((N_L, N_L), dtype='float64')

for I in xrange(ImatL):

    ii, jj = Imat[I, :]

    dotvec = np.dot(X[:, ii], X[:, jj])

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

""" Calculate XhY """

XhY = np.zeros(N_L, dtype='float64')

for ii in xrange(N_L):
    XhY[ii] = np.dot(X[:, ii], Y)

""" Perform the regression """

coeff = np.linalg.solve(XhX, XhY)
# print "coefficients from regression: %s\n" % str(coeff)

""" Check the regression accuracy """

# Y_ is the set of predictions from the regression fit for the calibration
# data points
Y_ = np.dot(coeff, X.T)

print "min(Y): %s" % np.min(Y)
print "mean(Y): %s" % np.mean(Y)
print "max(Y): %s" % np.max(Y)
print "\n"

error = np.abs(Y_.real - Y)

print "mean error: %s" % np.mean(error)
print "std of error: %s" % np.std(error)
print "max error: %s" % np.max(error)

""" Plot the regression results """

plt.figure(num=2, figsize=[10, 6])

plt.plot(thvec, Y, 'bo')
plt.plot(thvec, Y_, 'rx')

""" Employ more points to get smoother curve """
thplt = np.linspace(0, n_th*sub2rad, 150)
Yplt = np.zeros(thplt.shape, dtype='float64')
for ii in xrange(N_L):
    Yplt += coeff[ii]*np.cos(2*np.pi*ii*thplt/L_th)
plt.plot(thplt, Yplt, 'r-')

plt.title('FIP vs. theta, euler angles: %s' % str(angvec))
plt.xlabel('theta (radians)')
plt.ylabel('FIP parameter value')

plt.show()
