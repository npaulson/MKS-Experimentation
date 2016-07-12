import time
import numpy as np
import hex_0_7_real_alt as gsh
import matplotlib.pyplot as plt


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

N_L = indxvec.shape[0]
print "N_L = %s" % N_L
#N_L = 100

phi1max = 360
phimax = 90
phi2max = 60

# domain_sz is the integration domain in radians
domain_sz = phi1max*phimax*phi2max*(np.pi/180.)**3
# euler_sz is the size of euler space in radians
euler_sz = (2*np.pi)*(np.pi)*(2*np.pi)

inc = 10.

"""Retrieve Euler angle set"""

euler, n_tot = euler_grid_center(inc, phi1max, phimax, phi2max)

"""Calculate X"""

st = time.time()

X = gsh.gsh_eval(euler, np.arange(N_L))

print "basis evaluation complete: %ss" % np.round(time.time()-st, 3)
print "size of X: %sgb" % np.str(X.nbytes/(1E9))

"""Perform the orthogonality check"""

inner_mat = np.zeros((N_L, N_L), dtype='complex128')

euler_frac = domain_sz/euler_sz
print "integration domains per euler space: %s" % str(1./euler_frac)

fzsz = 1./(euler_frac*8.*np.pi**2)
bsz = domain_sz/n_tot
print "bsz: %s" % bsz
print "n_tot: %s" % n_tot

for ii in xrange(N_L):

    print "ii = %s" % ii

    for jj in xrange(ii, N_L):

        l = indxvec[jj, 0]
        tmp = (1./(2.*l+1.)) * \
            np.sum(X[:, ii]*X[:, jj].conj()*np.sin(euler[:, 1]))*bsz*fzsz

        if ii == jj:
            inner_mat[ii, ii] = tmp
        else:
            inner_mat[ii, jj] = tmp
            inner_mat[jj, ii] = tmp

"""Plot a colormap for function orthogonality"""

plt.figure(num=1, figsize=[12, 9])

dmin_ = np.abs(inner_mat.real.min())
dmax_ = np.abs(inner_mat.real.max())
dbound = np.array([dmin_, dmax_]).max()
dmin = -dbound
dmax = dbound

ax = plt.imshow(inner_mat.real,
                origin='lower',
                interpolation='none',
                cmap='seismic',
                vmin=dmin,
                vmax=dmax)

plt.colorbar(ax)
plt.title("Numerical othogonality check for the cubic GSH functions")
plt.xlabel("basis function index")
plt.ylabel("basis function index")
plt.show()
