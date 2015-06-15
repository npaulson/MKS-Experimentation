# -*- coding: utf-8 -*-
"""
@author: nhpnp3
"""

import functions as rr
import numpy as np

# N_en is the order of the highest order Legendre Polynomial for the Discrete Legendre Transform (DLT)
N_en = 5

# initialize the real space database
DB = np.zeros([N_en,21,120,31,20])

# LegPoly(n,x) evaluates the Legendre Polynomial of order n for the array X (and returns an array of the same size as X)
LegPoly() =

F()

for kk = range(N_en):

	tmp_sum = np.zeros(DB.shape)

	for nn = range(N_en):

		XIn = DB(nn,...)

		summand = ()/LegPoly()

		tmp_sum

	F(kk) = ((2*kk+1)/(N_en**2))
	
DB_dlt = 

# perform FFT on angular axes (theta,phi1,Phi and phi2, all periodic)
DB_fft_dlt = np.fft.fftn(DB, axes=[1, 2, 3, 4])
