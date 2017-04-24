import numpy as np
import gsh_hex_tri_L0_16 as gsh
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

    phi1, phi, phi2 = np.meshgrid(phi1vec, phivec, phi2vec)

    euler = np.zeros([n_tot, 3], dtype='float64')
    euler[:, 0] = phi1.reshape(phi1.size)
    euler[:, 1] = phi.reshape(phi.size)
    euler[:, 2] = phi2.reshape(phi2.size)

    return euler, n_tot


def pre_surf(x1_, x2_, z_, inc):

    incr = inc*(np.pi/180.)

    n_x1 = np.unique(x1_).size
    n_x2 = np.unique(x2_).size

    x1 = np.zeros((n_x1, n_x2))
    x2 = np.zeros((n_x1, n_x2))
    z = np.zeros((n_x1, n_x2))

    for ii in xrange(len(z_)):

        x1_v = x1_[ii]
        x2_v = x2_[ii]
        z_v = z_[ii]

        x1_indx = np.int64(np.round((x1_v-0.5*incr)/incr))
        x2_indx = np.int64(np.round((x2_v-0.5*incr)/incr))

        x1[x1_indx, x2_indx] = x1_v
        x2[x1_indx, x2_indx] = x2_v
        z[x1_indx, x2_indx] = z_v

    return x1, x2, z


def integrate(l_tr_val, ind_bs):

    """Initialize the important constants"""

    phi1max = 360.  # max phi1 angle (deg) for integration domain
    phimax = 90.  # max phi angle (deg) for integration domain
    phi2max = 60.  # max phi2 angle (deg) for integration domain
    inc = 3.  # degree increment for euler angle generation
    l_tr_cal = 8  # truncation level in the l index for the GSH

    indxvec = gsh.gsh_basis_info()
    N_L_cal = np.sum(indxvec[:, 0] <= l_tr_cal)
    N_L_val = np.sum(indxvec[:, 0] <= l_tr_val)
    N_L = np.max([N_L_cal, N_L_val])

    euler, n_tot = euler_grid_center(inc, phi1max, phimax, phi2max)

    """Generate X"""
    X = gsh.gsh_eval(euler, np.arange(N_L))/(2*indxvec[:N_L, 0]+1)

    """Generate Y (test function)"""

    np.random.seed(141)

    normvec = (2*indxvec[:N_L, 0]+1)**3
    bval = (np.random.normal(scale=1.0, size=N_L_cal)**3)/normvec

    Y = np.zeros(n_tot, dtype='complex128')
    for ii in xrange(N_L_cal):
        Y += bval[ii]*X[:, ii]

    Y = Y.real

    """Perform the integration for the GSH coefficients"""
    coef = np.zeros(N_L_val, dtype='complex128')

    # domain_eul_sz is the integration domain in radians
    domain_sz = phi1max*phimax*phi2max*(np.pi/180.)**3
    # full_eul_sz is the size of euler space in radians
    full_sz = (2*np.pi)*(np.pi)*(2*np.pi)
    eul_frac = domain_sz/full_sz
    fzsz = 1./(eul_frac*8.*np.pi**2)
    bsz = domain_sz/n_tot

    for ii in xrange(N_L_val):

        l = indxvec[ii, 0]
        tmp = (2*l+1)*np.sum(Y*X[:, ii].conj()*np.sin(euler[:, 1]))*bsz*fzsz
        coef[ii] = tmp

    """check accuracy of GSH representation"""

    Y_gsh = np.zeros(n_tot, dtype='complex128')
    for ii in xrange(N_L_val):
        Y_gsh += coef[ii]*X[:, ii]

    Y_gsh = Y_gsh.real

    error_gsh = np.abs(Y_gsh - Y)

    print "\nGSH basis representation errors"
    print "mean error: %s" % np.mean(error_gsh)
    print "std of error: %s" % np.std(error_gsh)
    print "max error: %s" % np.max(error_gsh)

    """Perform the integration for the indicator basis coefficients"""
    n_p1_ind = phi1max/ind_bs
    n_P_ind = phimax/ind_bs
    n_p2_ind = phi2max/ind_bs

    ysum = np.zeros((n_p1_ind, n_P_ind, n_p2_ind))
    ycount = np.zeros((n_p1_ind, n_P_ind, n_p2_ind))

    N_ind = ysum.size

    ind_bs_r = ind_bs*np.pi/180.

    for ii in xrange(np.int64(n_tot)):
        eset = np.int64(np.floor(euler[ii, :]/ind_bs_r))
        ysum[eset[0], eset[1], eset[2]] += Y[ii]
        ycount[eset[0], eset[1], eset[2]] += 1

    y_integrate = ysum/ycount
    del ysum, ycount

    Y_ind = np.zeros(n_tot, dtype='float64')

    for ii in xrange(np.int64(n_tot)):
        eset = np.int64(np.floor(euler[ii, :]/ind_bs_r))
        Y_ind[ii] = y_integrate[eset[0], eset[1], eset[2]]
    del y_integrate

    """check accuracy of indicator function representation"""

    error_ind = np.abs(Y_ind - Y)

    print "\nindicator basis representation errors"
    print "mean error: %s" % np.mean(error_ind)
    print "std of error: %s" % np.std(error_ind)
    print "max error: %s" % np.max(error_ind)

    """ Plot the regression results """

    phi2_u = np.unique(euler[:, 2])

    ang_sel = euler[:, 2] == phi2_u[np.int64(len(phi2_u)/2.)]

    plt.figure(figsize=[8, 8])

    vmin = np.min([Y, Y_gsh, Y_ind])
    vmax = np.max([Y, Y_gsh, Y_ind])

    x1, x2, z = pre_surf(euler[ang_sel, 0], euler[ang_sel, 1],
                         Y[ang_sel], inc)

    plt.subplot(311)
    ax = plt.imshow(z.T, interpolation='none', cmap='magma',
                    vmin=vmin, vmax=vmax,
                    extent=[0, 2*np.pi, 0, np.pi/2.])
    plt.colorbar(ax)
    plt.title("Reference ODF slice")
    plt.xlabel("$\phi1$")
    plt.ylabel("$\Phi$")

    x1, x2, z = pre_surf(euler[ang_sel, 0], euler[ang_sel, 1],
                         Y_gsh[ang_sel], inc)

    plt.subplot(312)
    ax = plt.imshow(z.T, interpolation='none', cmap='magma',
                    vmin=vmin, vmax=vmax,
                    extent=[0, 2*np.pi, 0, np.pi/2.])
    plt.colorbar(ax)
    plt.title("ODF slice with %s GSH bases" % N_L_val)
    plt.xlabel("$\phi1$")
    plt.ylabel("$\Phi$")

    x1, x2, z = pre_surf(euler[ang_sel, 0], euler[ang_sel, 1],
                         Y_ind[ang_sel], inc)

    plt.subplot(313)
    ax = plt.imshow(z.T, interpolation='none', cmap='magma',
                    vmin=vmin, vmax=vmax,
                    extent=[0, 2*np.pi, 0, np.pi/2.])
    plt.colorbar(ax)
    plt.title("ODF slice with %s indicator bases" % N_ind)
    plt.xlabel("$\phi1$")
    plt.ylabel("$\Phi$")

    plt.show()
