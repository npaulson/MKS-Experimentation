import numpy as np


def g2bunge(g):

    LTT = np.abs(np.abs(g[..., 2, 2]) - 1) < 1E-8

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

    return phi1, Phi, phi2


def bunge2g(phi1, Phi, phi2):
    # this has been cross-checked
    # only works for radians

    # g = np.zeros([phi1.shape[0], 3, 3])
    shp = phi1.shape
    g = np.zeros(list(shp)+[3, 3])

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


def symcub():

    symcub = np.zeros([24, 3, 3])

    # 0
    symcub[0, 0, 0] = 1
    symcub[0, 1, 1] = 1
    symcub[0, 2, 2] = 1
    # 1
    symcub[1, 0, 2] = 1
    symcub[1, 1, 0] = 1
    symcub[1, 2, 1] = 1
    # 2
    symcub[2, 0, 1] = 1
    symcub[2, 1, 2] = 1
    symcub[2, 2, 0] = 1
    # 3
    symcub[3, 0, 1] = -1
    symcub[3, 1, 2] = 1
    symcub[3, 2, 0] = -1
    # 4
    symcub[4, 0, 1] = -1
    symcub[4, 1, 2] = -1
    symcub[4, 2, 0] = 1
    # 5
    symcub[5, 0, 1] = 1
    symcub[5, 1, 2] = -1
    symcub[5, 2, 0] = -1
    # 6
    symcub[6, 0, 2] = -1
    symcub[6, 1, 0] = 1
    symcub[6, 2, 1] = -1
    # 7
    symcub[7, 0, 2] = -1
    symcub[7, 1, 0] = -1
    symcub[7, 2, 1] = 1
    # 8
    symcub[8, 0, 2] = 1
    symcub[8, 1, 0] = -1
    symcub[8, 2, 1] = -1
    # 9
    symcub[9, 0, 0] = -1
    symcub[9, 1, 1] = 1
    symcub[9, 2, 2] = -1
    # 10
    symcub[10, 0, 0] = -1
    symcub[10, 1, 1] = -1
    symcub[10, 2, 2] = 1
    # 11
    symcub[11, 0, 0] = 1
    symcub[11, 1, 1] = -1
    symcub[11, 2, 2] = -1
    # 12
    symcub[12, 0, 2] = -1
    symcub[12, 1, 1] = -1
    symcub[12, 2, 0] = -1
    # 13
    symcub[13, 0, 2] = 1
    symcub[13, 1, 1] = -1
    symcub[13, 2, 0] = 1
    # 14
    symcub[14, 0, 2] = 1
    symcub[14, 1, 1] = 1
    symcub[14, 2, 0] = -1
    # 15
    symcub[15, 0, 2] = -1
    symcub[15, 1, 1] = 1
    symcub[15, 2, 0] = 1
    # 16
    symcub[16, 0, 0] = -1
    symcub[16, 1, 2] = -1
    symcub[16, 2, 1] = -1
    # 17
    symcub[17, 0, 0] = 1
    symcub[17, 1, 2] = -1
    symcub[17, 2, 1] = 1
    # 18
    symcub[18, 0, 0] = 1
    symcub[18, 1, 2] = 1
    symcub[18, 2, 1] = -1
    # 19
    symcub[19, 0, 0] = -1
    symcub[19, 1, 2] = 1
    symcub[19, 2, 1] = 1
    # 20
    symcub[20, 0, 1] = -1
    symcub[20, 1, 0] = -1
    symcub[20, 2, 2] = -1
    # 21
    symcub[21, 0, 1] = 1
    symcub[21, 1, 0] = -1
    symcub[21, 2, 2] = 1
    # 22
    symcub[22, 0, 1] = 1
    symcub[22, 1, 0] = 1
    symcub[22, 2, 2] = -1
    # 23
    symcub[23, 0, 1] = -1
    symcub[23, 1, 0] = 1
    symcub[23, 2, 2] = 1

    return symcub


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
