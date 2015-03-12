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

# these values are from Matthew's vtk file
# sigval = Bmatrix(8.545240E2, 4.153528E2, 4.502432E2, 2.739572E0, 5.980331E0,
#                  -4.844964E0)
# epstest = Bmatrix(4.880218E-3, 1.563865E-4, -5.075973E-5, -6.266308E-5,
#                   6.025747E-5, 6.866434E-4)
# euler = np.array([[1.601652E2, 6.406010E1, 7.075200E0]])

# these values are from a single integration pt. from my .dat files (Abaqus LE)
sigval = Bmatrix(-20.94, 13.65, 2.983, 4.643, -3.312, -7.015)
epstest = Bmatrix(-2.5311E-4, 2.0856E-4, 3.2522E-5, 1.2395E-4, -6.6646E-5,
                  -1.4115E-4)
euler = np.array([[322.1053, 18.1949, 0]])


print sigval

g = bungemtrx(euler, 0)
g = g[0, ...]


# [Cs, CsM2] = sc.stiffness_calc(euler[0, :]*(np.pi/180))
# print CsM2
# print np.einsum('...kl,kl', Cs, epstest)


# use matrix form

print 'eps sf'
print epstest

eps_cf = np.einsum('ik,jl,kl', g, g, epstest)

print 'eps cf'
print eps_cf

eps_cf_lin = np.array([eps_cf[0, 0],
                       eps_cf[1, 1],
                       eps_cf[2, 2],
                       2*eps_cf[1, 2],
                       2*eps_cf[0, 2],
                       2*eps_cf[0, 1]])

# sig_cf_lin = np.dot(Cij, eps_cf_lin)
sig_cf_lin = np.einsum('ij,j', Cij, eps_cf_lin)


sig_cf = Bmatrix(sig_cf_lin[0],
                 sig_cf_lin[1],
                 sig_cf_lin[2],
                 sig_cf_lin[5],
                 sig_cf_lin[4],
                 sig_cf_lin[3])

sig_sf = np.einsum('ki,lj,kl', g, g, sig_cf)

print 'sig_sf'
print sig_sf


eps_lin = np.array([epstest[0, 0],
                    epstest[1, 1],
                    epstest[2, 2],
                    2*epstest[1, 2],
                    2*epstest[0, 2],
                    2*epstest[0, 1]])

print np.dot(Cij, eps_lin)
