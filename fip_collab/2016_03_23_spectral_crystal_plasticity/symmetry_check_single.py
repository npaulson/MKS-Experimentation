import time
import sys
import numpy as np
import gsh_cub_tri_L0_16 as gsh
import euler_func as ef


"""Initialize important variables"""

indxvec = gsh.gsh_basis_info()

N_L = indxvec.shape[0]
print "N_L = %s" % N_L
# N_L = 10

phi1max = 360
phimax = 90
phi2max = 90

inc = 10.

"""Retrieve Euler angle set"""

p1 = np.float32(sys.argv[1])
P = np.float32(sys.argv[2])
p2 = np.float32(sys.argv[3])
Leval = np.int16(sys.argv[4])

euler = np.array([[p1, P, p2]])
n_tot = 1

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

print "maximum error: %s" % error.max()

print "coefficient magnitude closest to zero: %s" % str(np.abs(X).min())

print np.round(X[:, 0, Leval], 5)
# print X[:, 0, Leval]