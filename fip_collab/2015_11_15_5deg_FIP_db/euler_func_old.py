import numpy as np


def g2bunge(g):

    if np.abs(g[:, 2, 2] - 1) < .0001:
        Phi = 0
        phi1 = 0.5*np.arctan2(g[:, 0, 1], g[:, 0, 0])
        phi2 = phi1
    else:
        Phi = np.arccos(g[:, 2, 2])
        phi1 = np.arctan2(g[:, 2, 0]/np.sin(Phi), -g[:, 2, 1]/np.sin(Phi))
        phi2 = np.arctan2(g[:, 0, 2]/np.sin(Phi), g[:, 1, 2]/np.sin(Phi))

    return phi1, Phi, phi2


def bunge2g(phi1, Phi, phi2):
    # this has been cross-checked
    # only works for radians

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


def symhex():

    symhex = np.zeros([3, 3, 12])
    a = np.sqrt(3.)/2.

    # 1
    symhex[0, 0, 0] = 1
    symhex[1, 1, 0] = 1
    symhex[2, 2, 0] = 1
    # 2
    symhex[0, 0, 1] = -.5
    symhex[1, 1, 1] = -.5
    symhex[2, 2, 1] = 1
    symhex[0, 1, 1] = a
    symhex[1, 0, 1] = -a
    # 3
    symhex[0, 0, 2] = -.5
    symhex[1, 1, 2] = -.5
    symhex[2, 2, 2] = 1
    symhex[0, 1, 2] = -a
    symhex[1, 0, 2] = a
    # 4
    symhex[0, 0, 3] = .5
    symhex[1, 1, 3] = .5
    symhex[2, 2, 3] = 1
    symhex[0, 1, 3] = a
    symhex[1, 0, 3] = -a
    # 5
    symhex[0, 0, 4] = -1
    symhex[1, 1, 4] = -1
    symhex[2, 2, 4] = 1
    # 6
    symhex[0, 0, 5] = .5
    symhex[1, 1, 5] = .5
    symhex[2, 2, 5] = 1
    symhex[0, 1, 5] = -a
    symhex[1, 0, 5] = a
    # 7
    symhex[0, 0, 6] = -.5
    symhex[1, 1, 6] = .5
    symhex[2, 2, 6] = -1
    symhex[0, 1, 6] = -a
    symhex[1, 0, 6] = -a
    # 8
    symhex[0, 0, 7] = 1
    symhex[1, 1, 7] = -1
    symhex[2, 2, 7] = -1
    # 9
    symhex[0, 0, 8] = -.5
    symhex[1, 1, 8] = .5
    symhex[2, 2, 8] = -1
    symhex[0, 1, 8] = a
    symhex[1, 0, 8] = a
    # 10
    symhex[0, 0, 9] = .5
    symhex[1, 1, 9] = -.5
    symhex[2, 2, 9] = -1
    symhex[0, 1, 9] = a
    symhex[1, 0, 9] = a
    # 11
    symhex[0, 0, 10] = -1
    symhex[1, 1, 10] = 1
    symhex[2, 2, 10] = -1
    # 12
    symhex[0, 0, 11] = .5
    symhex[1, 1, 11] = -.5
    symhex[2, 2, 11] = -1
    symhex[0, 1, 11] = -a
    symhex[1, 0, 11] = -a

    return symhex
