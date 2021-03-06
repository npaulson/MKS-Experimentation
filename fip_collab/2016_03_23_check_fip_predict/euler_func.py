import numpy as np


def g2bunge(g):

    LTT = np.abs(np.abs(g[..., 2, 2]) - 1) < 1E-8

    print '# of g: %s' % g.shape[0]
    print "# of Phi close n*pi: %s" % np.sum(LTT)

    # print "number of orientations with Phi close to zero: %s" % np.sum(LTT)

    """
    # use this block if you want phi1 == phi2
    phi1_LTT = 0.5*np.arctan2(g[..., 0, 1], g[..., 0, 0])
    phi2_LTT = phi1_LTT
    """
    # use this block if you want phi2 == 0
    phi1_LTT = np.arctan2(g[..., 0, 1], g[..., 0, 0])
    phi2_LTT = np.zeros(phi1_LTT.shape)

    Phi = (LTT == 0)*np.arccos(g[..., 2, 2])+LTT

    phi1 = np.arctan2(g[..., 2, 0]/np.sin(Phi), -g[..., 2, 1]/np.sin(Phi))
    phi1 = (LTT == 0)*phi1 + LTT*phi1_LTT

    phi2 = np.arctan2(g[..., 0, 2]/np.sin(Phi), g[..., 1, 2]/np.sin(Phi))
    phi2 = (LTT == 0)*phi2 + LTT*phi2_LTT

    Phi = Phi - LTT

    """
    #this block is for the non-vectorized form
    if np.abs(g[..., 2, 2]) - 1 < .0001:
        Phi = 0
        phi1 = 0.5*np.arctan2(g[..., 0, 1], g[..., 0, 0])
        phi2 = phi1
    else:
        Phi = np.arccos(g[..., 2, 2])
        phi1 = np.arctan2(g[..., 2, 0]/np.sin(Phi), -g[..., 2, 1]/np.sin(Phi))
        phi2 = np.arctan2(g[..., 0, 2]/np.sin(Phi), g[..., 1, 2]/np.sin(Phi))
    """

    euler = np.zeros((phi1.size, 3))
    euler[:, 0] = phi1
    euler[:, 1] = Phi
    euler[:, 2] = phi2

    return euler


def bunge2g(euler):
    # this has been cross-checked
    # only works for radians

    phi1 = euler[:, 0]
    Phi = euler[:, 1]
    phi2 = euler[:, 2]

    g = np.zeros([phi1.shape[0], 3, 3])

    g[..., 0, 0] = np.cos(phi1)*np.cos(phi2) - \
        np.sin(phi1)*np.sin(phi2)*np.cos(Phi)

    g[..., 0, 1] = np.sin(phi1)*np.cos(phi2) + \
        np.cos(phi1)*np.sin(phi2)*np.cos(Phi)

    g[..., 0, 2] = np.sin(phi2)*np.sin(Phi)

    g[..., 1, 0] = -np.cos(phi1)*np.sin(phi2) - \
        np.sin(phi1)*np.cos(phi2)*np.cos(Phi)

    g[..., 1, 1] = -np.sin(phi1)*np.sin(phi2) + \
        np.cos(phi1)*np.cos(phi2)*np.cos(Phi)

    g[..., 1, 2] = np.cos(phi2)*np.sin(Phi)

    g[..., 2, 0] = np.sin(phi1)*np.sin(Phi)

    g[..., 2, 1] = -np.cos(phi1)*np.sin(Phi)

    g[..., 2, 2] = np.cos(Phi)

    return g


# def check_euler_op(euler):

#     symop = symhex()

#     g_test = bunge2g(euler)
#     euler_test = g2bunge(g_test)
#     euler_test += 2*np.pi*np.array(euler_test < 0)

#     for ii in xrange(euler.shape[0]):
#         iseq = np.all(np.isclose(euler[ii, :], euler_test[ii, :]))
#         if not iseq:
#             print "\neuler: %s" % str(euler[ii, :])
#             phi1phi2 = np.array([euler[ii, 0]+euler[ii, 2],
#                                  euler[ii, 0]-euler[ii, 2]])
#             print "phi1 +- phi2 for euler: %s" % str(phi1phi2)
#             print "euler_test: %s" % str(euler_test[ii, :])

#     g_test2 = bunge2g(euler_test)
#     gsymm = np.einsum(symop)

#         isgeq = False

#         for ii in xrange(symop.shape[0]):

#             gtmp = bunge2g(euler_test[ii, :][None, :])

#             g_symm = np.dot(symop[ii, ...], gtmp)
#             if np.all(np.isclose(gtmp, g_symm)):
#                 isgeq = True

#         if not isgeq:
#             print "g != g_test"


def symhex():

    symhex = np.zeros([12, 3, 3])
    a = np.sqrt(3.)/2.

    # 0
    symhex[0, 0, 0] = 1
    symhex[0, 1, 1] = 1
    symhex[0, 2, 2] = 1
    # 1
    symhex[1, 0, 0] = -.5
    symhex[1, 1, 1] = -.5
    symhex[1, 2, 2] = 1
    symhex[1, 0, 1] = a
    symhex[1, 1, 0] = -a
    # 2
    symhex[2, 0, 0] = -.5
    symhex[2, 1, 1] = -.5
    symhex[2, 2, 2] = 1
    symhex[2, 0, 1] = -a
    symhex[2, 1, 0] = a
    # 3
    symhex[3, 0, 0] = .5
    symhex[3, 1, 1] = .5
    symhex[3, 2, 2] = 1
    symhex[3, 0, 1] = a
    symhex[3, 1, 0] = -a
    # 4
    symhex[4, 0, 0] = -1
    symhex[4, 1, 1] = -1
    symhex[4, 2, 2] = 1
    # 5
    symhex[5, 0, 0] = .5
    symhex[5, 1, 1] = .5
    symhex[5, 2, 2] = 1
    symhex[5, 0, 1] = -a
    symhex[5, 1, 0] = a
    # 6
    symhex[6, 0, 0] = -.5
    symhex[6, 1, 1] = .5
    symhex[6, 2, 2] = -1
    symhex[6, 0, 1] = -a
    symhex[6, 1, 0] = -a
    # 7
    symhex[7, 0, 0] = 1
    symhex[7, 1, 1] = -1
    symhex[7, 2, 2] = -1
    # 8
    symhex[8, 0, 0] = -.5
    symhex[8, 1, 1] = .5
    symhex[8, 2, 2] = -1
    symhex[8, 0, 1] = a
    symhex[8, 1, 0] = a
    # 9
    symhex[9, 0, 0] = .5
    symhex[9, 1, 1] = -.5
    symhex[9, 2, 2] = -1
    symhex[9, 0, 1] = a
    symhex[9, 1, 0] = a
    # 10
    symhex[10, 0, 0] = -1
    symhex[10, 1, 1] = 1
    symhex[10, 2, 2] = -1
    # 11
    symhex[11, 0, 0] = .5
    symhex[11, 1, 1] = -.5
    symhex[11, 2, 2] = -1
    symhex[11, 0, 1] = -a
    symhex[11, 1, 0] = -a

    return symhex
