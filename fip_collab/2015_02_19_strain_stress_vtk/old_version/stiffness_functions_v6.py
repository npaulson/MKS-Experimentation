# -*- coding: utf-8 -*-
"""
Created on Thu Feb 05 15:06:31 2015

@author: nhpnp3
"""

import numpy as np
import stiffness_calc as sc
import time


def bungemtrx(euler, israd):
    # this has been cross-checked

    if israd != 1:
        euler = euler * (np.pi/180)

    phi1 = euler[:, 0]
    Phi = euler[:, 1]
    phi2 = euler[:, 2]

    g = np.zeros([euler.shape[0], 3, 3])

    g[:, 0, 0] = np.cos(phi1)*np.cos(phi2) - \
        np.sin(phi1)*np.sin(phi2)*np.cos(Phi)

    g[:, 0, 1] = np.sin(phi1)*np.cos(phi2) + \
        np.cos(phi1)*np.sin(phi2)*np.cos(Phi)

    g[:, 0, 2] = np.sin(phi2)*np.sin(Phi)

    g[:, 1, 0] = -np.cos(phi1)*np.sin(phi2) - \
        np.sin(phi1)*np.cos(phi2)*np.cos(Phi)

    g[:, 1, 1] = -np.sin(phi1)*np.sin(phi2) + \
        np.cos(phi1)*np.cos(phi2)*np.cos(Phi)

    g[:, 1, 2] = np.cos(phi2)*np.sin(Phi)

    g[:, 2, 0] = np.sin(phi1)*np.sin(Phi)

    g[:, 2, 1] = -np.cos(phi1)*np.sin(Phi)

    g[:, 2, 2] = np.cos(Phi)

    return g


def Bmatrix(p00, p11, p22, p01, p02, p12):
    # function written by Matthew Priddy 2/19/2015

    B = np.zeros([3, 3])

    B[0, 0] = p00
    B[0, 1] = p01
    B[0, 2] = p02
    B[1, 0] = p01
    B[1, 1] = p11
    B[1, 2] = p12
    B[2, 0] = p02
    B[2, 1] = p12
    B[2, 2] = p22

    return B


def calc_Cijkl_from_Cij(Cij):
    # function written by Matthew Priddy 2/19/2015

    # ij or kl: 11 22 33 23 31 12 32 13 21
    # m  or n :  1  2  3  4  5  6  7  8  9

    # Theory of dislocations, pg. 34.

    # this needs to be cross checked

    Cijkl = np.zeros((3, 3, 3, 3))

    ia = 0
    ib = 0

    for i in range(3):
        for j in range(3):

            ia = i

            if (i != j):
                ia = 6-i-j

            for k in range(3):
                for l in range(3):
                    ib = k

                    if (k != l):
                        ib = 6-k-l
                    Cijkl[i, j, k, l] = Cij[ia, ib]

    return Cijkl


def rotate_tensor_order4(Cmnop, g):
    # Cijkl' = Qim Qjn Qko Qlp Cmnop
    # this has been cross checked

    Cs = np.einsum('im, jn, ko, lp, mnop', g, g, g, g, Cmnop)

    return Cs


# (1c) Extract the material constants from the .inp files
# This should be automated, but for now we can hard code the input parameters

C11 = 172832.50
C12 = 97910.060
C13 = 73432.550
C33 = 192308.10
C44 = 49700.000
C66 = 0.5 * (C11 - C12)
shear_mod = (C44 * C66) ** 0.5

# For HCP crystal structures (e.g. Titanium)

Cij = np.zeros((6, 6))

Cij[0, 0] = C11
Cij[1, 1] = C11
Cij[0, 1] = C12
Cij[1, 0] = C12
Cij[0, 2] = C13
Cij[1, 2] = C13
Cij[2, 0] = C13
Cij[2, 1] = C13
Cij[2, 2] = C33
Cij[3, 3] = C44
Cij[4, 4] = C44
Cij[5, 5] = C66

sigma_actual = Bmatrix(8.545240E2, 4.153528E2, 4.502432E2, 2.739572E0,
                       5.980331E0, -4.844964E0)
epsilon = Bmatrix(4.880218E-3, 1.563865E-4, -5.075973E-5, -6.266308E-5,
                  6.025747E-5, 6.866434E-4)
euler = np.array([[1.601652E2, 6.406010E1, 7.075200E0]])

print "euler angles from .vtk:"
print euler
print "strain from .vtk:"
print epsilon


g = bungemtrx(euler, 0)
g = g[0, ...]


Cijkl = calc_Cijkl_from_Cij(Cij)

Cijkl_ = rotate_tensor_order4(Cijkl, g.T)

sigma_result = np.einsum('...kl,kl', Cijkl_, epsilon)

print "stress from .vtk:"
print sigma_actual

print "calculated stress:"
print sigma_result
