import numpy as np
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

phi1max = 360
phimax = 90
phi2max = 90
thetamax = 60

d2r = np.pi/180.

inc = 10.

"""Retrieve Euler angle set for regular gridding"""

euler, n_tot = euler_grid_center(inc, phi1max, phimax, phi2max)

"""Tack on some extra orientations where Phi==0"""

n_extra = 10

euler_extra = np.zeros((n_extra, 3))
euler_extra[:, 0] = (2.*np.pi) * np.random.rand(n_extra)
euler_extra[:, 1] = 0
euler_extra[:, 2] = (np.pi/2.) * np.random.rand(n_extra)

euler = np.vstack([euler, euler_extra])

n_tot += n_extra

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

print "n_tot: %s" % n_tot
print "euler_sym.shape: %s" % str(euler_sym.shape)

"""output symmetric euler angles to .txt file"""
esh = euler_sym.shape

euler_sym_lin = np.zeros((np.prod(esh[:2]), 3))

c = 0
for ii in xrange(esh[1]):
    for jj in xrange(esh[0]):
        euler_sym_lin[c, :] = euler_sym[jj, ii, :]
        c += 1

np.savetxt("euler_sym.txt", euler_sym_lin)

print np.squeeze(euler_sym[:, 0, :])
print euler_sym_lin[:24, :]

"""generate set of thetas"""
theta = np.linspace(0, 60, 7)
n_theta = theta.size
print "theta: %s" % str(theta)
theta = theta*d2r

theta_sym = np.zeros((6, n_theta))

theta_sym[0, :] = theta
theta_sym[1, :] = (120*d2r)-theta
theta_sym[2, :] = (120*d2r)+theta
theta_sym[3, :] = (2*120*d2r)-theta
theta_sym[4, :] = (2*120*d2r)+theta
theta_sym[5, :] = (3*120*d2r)-theta

"""output symmetric thetas to .txt file"""

theta_sym_lin = np.zeros((n_theta*6,))

c = 0
for ii in xrange(n_theta):
    for jj in xrange(6):
        theta_sym_lin[c] = theta_sym[jj, ii]
        c += 1

np.savetxt("theta_sym.txt", theta_sym_lin)

print theta_sym[:, 1]
print theta_sym_lin[6:12]
