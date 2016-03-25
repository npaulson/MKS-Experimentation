import numpy as np


def bunge2g(euler):
    # this has been cross-checked
    # only works for radians

    phi1 = euler[0]
    Phi = euler[1]
    phi2 = euler[2]

    g = np.zeros([3, 3])

    g[0, 0] = np.cos(phi1)*np.cos(phi2) - \
        np.sin(phi1)*np.sin(phi2)*np.cos(Phi)

    g[0, 1] = np.sin(phi1)*np.cos(phi2) + \
        np.cos(phi1)*np.sin(phi2)*np.cos(Phi)

    g[0, 2] = np.sin(phi2)*np.sin(Phi)

    g[1, 0] = -np.cos(phi1)*np.sin(phi2) - \
        np.sin(phi1)*np.cos(phi2)*np.cos(Phi)

    g[1, 1] = -np.sin(phi1)*np.sin(phi2) + \
        np.cos(phi1)*np.cos(phi2)*np.cos(Phi)

    g[1, 2] = np.cos(phi2)*np.sin(Phi)

    g[2, 0] = np.sin(phi1)*np.sin(Phi)

    g[2, 1] = -np.cos(phi1)*np.sin(Phi)

    g[2, 2] = np.cos(Phi)

    return g


def g2bunge(g):

    if np.abs(np.abs(g[2, 2]) - 1) < 1E-8:
        print "gimble lock warning"
        Phi = 0
        phi1 = np.arctan2(g[0, 1], g[0, 0])/2
        phi2 = phi1
    else:
        Phi = np.arccos(g[2, 2])
        phi1 = np.arctan2(g[2, 0]/np.sin(Phi), -g[2, 1]/np.sin(Phi))
        phi2 = np.arctan2(g[0, 2]/np.sin(Phi), g[1, 2]/np.sin(Phi))

    return np.array([phi1, Phi, phi2])


if __name__ == '__main__':

    tmp = 2*np.random.random((3, 3))-1
    tmp = 0.5*(np.dot(tmp.T, tmp)-np.identity(3))

    vals, vecs = np.linalg.eigh(tmp)

    esort = np.argsort(np.abs(vals))[::-1]

    print "g1_orig:"
    print vecs

    vals = vals[esort]
    print "eigenvalues: %s" % str(vals)

    g1 = vecs[:, esort]
    print "g1:"
    print g1

    print "det(g1):"
    detg1 = np.linalg.det(g1)
    print detg1

    g2 = g1
    if detg1 < 0:
        g2[:, 2] = -g1[:, 2]

    print "g2:"
    print g2

    print "det(g2):"
    print np.linalg.det(g2)

    print "reconstructed matrix of eigenvalues:"
    print np.round(np.dot(np.dot(g2.T, tmp), g2), 6)

    # print "reconstructed tmp"
    # tmp_recon = np.zeros((3, 3))
    # print np.round(np.dot(np.dot(), vecs), 6)

    euler2 = g2bunge(g2)

    print "euler2:"
    print euler2

    g3 = bunge2g(euler2)

    print "g3:"
    print g3
