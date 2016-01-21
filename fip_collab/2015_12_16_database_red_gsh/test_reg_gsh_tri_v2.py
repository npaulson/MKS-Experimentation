import numpy as np
import gsh_tri_tri_L0_13 as gsh
import itertools as it
import matplotlib.pyplot as plt
import time

n_tot = 2000000
N_L = 10

phi1 = np.random.rand(n_tot)*2*np.pi
phi = np.random.rand(n_tot)*np.pi
phi2 = np.random.rand(n_tot)*2*np.pi

emat = np.zeros((n_tot, 3))
emat[:, 0] = phi1
emat[:, 1] = phi
emat[:, 2] = phi2

""" Calculate X """

st = time.time()

X = gsh.gsh_eval(emat, np.arange(N_L))

print "basis evaluation complete: %ss" % np.round(time.time()-st, 3)


""" Generate Y """

bvec = [0, 1, 3, 7, 9]
bval = [5., 3., .2, .2, .3]

Y = np.zeros(phi1.shape, dtype='complex128')

for ii in xrange(len(bvec)):
    Y += bval[ii]*X[:, bvec[ii]]

print np.mean(Y.real)
print np.mean(Y.imag)
print np.std(Y.imag)

""" Calculate XhX """

tmp = it.combinations_with_replacement(np.arange(N_L), 2)
Imat = np.array(list(tmp))
ImatL = Imat.shape[0]

XhX = np.zeros((N_L, N_L), dtype='complex128')

for I in xrange(ImatL):

    ii, jj = Imat[I, :]

    dotvec = np.dot(X[:, ii].conj(), X[:, jj])
    # dotvec = np.sum(X[:, ii].conj()*X[:, jj]*np.sin(phi))

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

XhY = np.zeros(N_L, dtype='complex128')

for ii in xrange(N_L):
    XhY[ii] = np.dot(X[:, ii].conj(), Y)
    # XhY[ii] = np.sum(X[:, ii].conj()*Y*np.sin(phi))


""" Perform the regression """

coeff = np.linalg.solve(XhX, XhY)
print "coefficients from regression: %s\n" % coeff

""" Check the regression accuracy """

# Y_ is the set of predictions from the regression fit for the calibration
# data points
Y_ = np.dot(coeff, X.T)

print "min(Y): %s" % np.min(Y)
print "mean(Y): %s" % np.mean(Y)
print "max(Y): %s" % np.max(Y)
print "std(Y): %s" % np.std(Y)
print "\n"

error = np.abs(Y_.real - Y.real)

print "mean error: %s" % np.mean(error)
print "std of error: %s" % np.std(error)
print "max error: %s" % np.max(error)
