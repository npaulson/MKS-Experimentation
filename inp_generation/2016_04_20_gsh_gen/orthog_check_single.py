import numpy as np
import hex_0_16_real_alt as gsh
import sys


def WP(msg, filename):
    """
    Summary:
        This function takes an input message and a filename, and appends that
        message to the file. This function also prints the message
    Inputs:
        msg (string): the message to write and print.
        filename (string): the full name of the file to append to.
    Outputs:
        both prints the message and writes the message to the specified file
    """
    fil = open(filename, 'a')
    print msg
    fil.write(msg)
    fil.write('\n')
    fil.close()


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

if __name__ == '__main__':

    """Initialize important variables"""

    ii = np.int64(sys.argv[1])
    jj = np.int64(sys.argv[2])

    indxvec = gsh.gsh_basis_info()

    N_L = indxvec.shape[0]
    # N_L = 7

    phi1max = 360
    phimax = 90
    phi2max = 60

    # domain_sz is the integration domain in radians
    domain_sz = phi1max*phimax*phi2max*(np.pi/180.)**3
    # euler_sz is the size of euler space in radians
    euler_sz = (2*np.pi)*(np.pi)*(2*np.pi)

    inc = 3.

    """Retrieve Euler angle set"""

    euler, n_tot = euler_grid_center(inc, phi1max, phimax, phi2max)

    """Perform the orthogonality check"""

    euler_frac = domain_sz/euler_sz
    print "integration domains per euler space: %s" % str(1./euler_frac)

    fzsz = 1./(euler_frac*8.*np.pi**2)
    bsz = domain_sz/n_tot

    print "bsz: %s" % bsz
    print "n_tot: %s" % n_tot

    print "basis A: %s" % str(indxvec[ii, :])
    print "basis B: %s" % str(indxvec[jj, :])

    bA = np.squeeze(gsh.gsh_eval(euler, [ii]))
    bB = np.squeeze(gsh.gsh_eval(euler, [jj]))

    l = indxvec[jj, 1]
    tmp = (1./(2.*l+1.)) * \
        np.sum(bA*bB.conj()*np.sin(euler[:, 1]))*bsz*fzsz

    print "results of check A and B: %s\n" % tmp
