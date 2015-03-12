#

# Calculate_Stress_from_Strain_MKS.py

#

# Written by Matthew Priddy on February 19, 2015

#

from sys import *

from string import *

from math import *

from pylab import *

from random import *

from numpy import *

import itertools

from numpy import tensordot as td

import matplotlib

#matplotlib.use('PDF')

import linecache

import time

from matplotlib import pyplot as plt

from scipy import optimize



def Gmatrix(phi1, phi0, phi2):

    g = zeros((3,3))



    g[0,0] =  ( cos(phi1) * cos(phi2) ) - ( sin(phi1) * sin(phi2) * cos(phi0) )

    g[0,1] =  ( sin(phi1) * cos(phi2) ) + ( cos(phi1) * sin(phi2) * cos(phi0) )

    g[0,2] =  ( sin(phi2) * sin(phi0) )

    g[1,0] = -( cos(phi1) * sin(phi2) ) - ( sin(phi1) * cos(phi2) * cos(phi0) )

    g[1,1] = -( sin(phi1) * sin(phi2) ) + ( cos(phi1) * cos(phi2) * cos(phi0) )

    g[1,2] =  ( cos(phi2) * sin(phi0) )

    g[2,0] =  ( sin(phi1) * sin(phi0) )

    g[2,1] = -( cos(phi1) * sin(phi0) )

    g[2,2] =  ( cos(phi0) )



    return g



def Bmatrix(p00, p11, p22, p01, p02, p12):

    B = zeros((3,3))



    B[0,0] = p00

    B[0,1] = p01

    B[0,2] = p02

    B[1,0] = p01

    B[1,1] = p11

    B[1,2] = p12

    B[2,0] = p02

    B[2,1] = p12

    B[2,2] = p22



    return B



def Cijkl_dot_dot_Skl(C,S):

# Vij = Cijkl*Skl

# Technically written as Vij = Cijkl*Slk, but Skl is symmetric in this work

    value = zeros((3,3))

    for i in range(3):

        for j in range(3):

            for k in range(3):

                for l in range(3):

                    value[i,j] = value[i,j] + C[i,j,k,l] * S[k,l]

    return value



def calc_Cijkl_from_Cij(Cij):

    ## ij or kl: 11 22 33 23 31 12 32 13 21

    ## m  or n :  1  2  3  4  5  6  7  8  9

    # Theory of dislocations, pg. 34.

    Cijkl = zeros((3,3,3,3))

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

                    Cijkl[i,j,k,l] = Cij[ia,ib]

    return Cijkl





elements = 21*21*21





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

Cij = zeros((6,6))

Cij[0,0] = C11; Cij[1,1] = C11

Cij[0,1] = C12; Cij[1,0] = C12

Cij[0,2] = C13; Cij[1,2] = C13; Cij[2,0] = C13; Cij[2,1] = C13

Cij[2,2] = C33

Cij[3,3] = C44; Cij[4,4] = C44

Cij[5,5] = C66



# Determine the 3x3x3x3 Stiffness matrix

Cijkl = calc_Cijkl_from_Cij(Cij)



# (1) Extract various values for use in this code

# (a) Extract the Euler angles for each element



euler_file = open(f6_EulerAngles,'r')

file_contents = euler_file.readlines()



euler = zeros((elements, 3))



for i in range(1+2,elements+3):

    data1 = linecache.getline(f6_EulerAngles,i,module_globals=None)

    data1 = data1.split()

    euler[i-3,0] = float(data1[1])

    euler[i-3,1] = float(data1[2])

    euler[i-3,2] = float(data1[3])



# Total Strain

NumCycles = 3

strn_t00_el = zeros((elements, 2*NumCycles + 1)); strn_t11_el = zeros((elements, 2*NumCycles + 1)); strn_t22_el = zeros((elements, 2*NumCycles + 1))



for i in range(0,elements):

    R = Gmatrix(euler[i,0], euler[i,1], euler[i,2]).T



    for count in range(0,2 * NumCycles):



        strain_0 = Bmatrix(strn_t00_el[i,count], strn_t11_el[i,count], strn_t22_el[i,count], strn_t01_el[i,count], strn_t02_el[i,count], strn_t12_el[i,count])

        stress_0_from_strain = Cijkl_dot_dot_Skl(rotT(R.T, Cijkl),strain_0)
