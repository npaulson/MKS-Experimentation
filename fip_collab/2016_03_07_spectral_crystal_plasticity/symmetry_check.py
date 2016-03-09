import time
import numpy as np
import gsh_cub_tri_L0_16 as gsh
import matplotlib.pyplot as plt
import euler_func as ef


def euler_grid_center(inc, phi1max, phimax, phi2max):

    n_p1 = (phi1max/inc)  # number of phi1 samples for FZ
    n_P = (phimax/inc)  # number of Phi samples for FZ
    n_p2 = (phi2max/inc)  # number of phi2 samples for FZ

    n_tot = n_p1*n_P*n_p2

    inc2rad = inc*np.pi/180.

    phi1vec = (np.arange(n_p1)+0.5)*inc2rad
    phivec = (np.arange(n_P)+0.5)*inc2rad
    phi2vec = (np.arange(n_p2)+0.5)*inc2rad

    print phi1vec.min()
    print phi1vec.max()

    print phivec.min()
    print phivec.max()

    print phi2vec.min()
    print phi2vec.max()

    phi1, phi, phi2 = np.meshgrid(phi1vec, phivec, phi2vec)

    euler = np.zeros([n_tot, 3], dtype='float64')
    euler[:, 0] = phi1.reshape(phi1.size)
    euler[:, 1] = phi.reshape(phi.size)
    euler[:, 2] = phi2.reshape(phi2.size)

    return euler, n_tot


"""Initialize important variables"""

indxvec = gsh.gsh_basis_info()

# N_L = indxvec.shape[0]
# print "N_L = %s" % N_L
N_L = 10

phi1max = 360
phimax = 90
phi2max = 90

inc = 10.

"""Retrieve Euler angle set"""

euler, n_tot = euler_grid_center(inc, phi1max, phimax, phi2max)

"""Perform the symmetry check"""

symop = ef.symcub()
n_sym = symop.shape[0]
print "number of symmetry operators: %s" % n_sym

euler_sym = np.zeros((n_sym, n_tot, 3))

g_orig = ef.bunge2g(euler[:, 0], euler[:, 1], euler[:, 2])

# find the symmetric equivalents to the euler angle within the FZ
for sym in xrange(n_sym):
    op = symop[sym, ...]

    # g_sym: array of orientation matrices transformed with a
    # symmetry operator
    g_sym = np.einsum('ik,...kj', op, g_orig)

    tmp = np.array(ef.g2bunge(g_sym)).transpose()

    if sym == 0:
        print "g_sym shape: %s" % str(g_sym.shape)
        print "tmp shape: %s" % str(tmp.shape)

    del g_sym
    euler_sym[sym, ...] = tmp
    del tmp

# make sure all of the euler angles within the appropriate
# ranges (eg. not negative)
print "initial: euler angles less than zero: %s" % np.sum(euler_sym < 0)
lt = euler_sym < 0.0
euler_sym += 2*np.pi*lt
print "final: euler angles less than zero: %s" % np.sum(euler_sym < 0)

"""Calculate the GSH coefficients for each symmetric zone"""

st = time.time()

X = gsh.gsh_eval(euler_sym, np.arange(1, N_L))

print "basis evaluation complete: %ss" % np.round(time.time()-st, 3)
print "size of X: %sgb" % str(X.nbytes/(1E9))
print "X shape: %s" % str(X.shape)

"""Error check the GSH coefficients in terms of symmetry"""

error = np.zeros((n_sym-1, n_tot, N_L - 1))

for sym in xrange(n_sym-1):
    error[sym, ...] = np.abs(np.real(X[0, ...]) - np.real(X[sym, ...]))

print "coefficient magnitude closest to zero: %s" % str(np.abs(X).min())

"""Plot histogram for coefficient magnitude"""

plt.figure(num=1, figsize=[10, 10])

plt.subplot(211)
plt.hist(X.real.reshape(X.size), 20)
plt.title("histogram of the real parts of GSH coefficients")
plt.xlabel("real part of coefficient")
plt.ylabel("count")

plt.subplot(212)
plt.hist(X.imag.reshape(X.size), 20)
plt.title("histogram of the imaginary parts of GSH coefficients")
plt.xlabel("imaginary part of coefficient")
plt.ylabel("count")

"""Plot histogram for coefficient errors"""

plt.figure(num=2, figsize=[10, 5])

plt.hist(error.reshape(error.size), 20)
plt.title("histogram of the GSH symmetry errors")
plt.xlabel("abs(orig-symm)")
plt.ylabel("count")

plt.show()
