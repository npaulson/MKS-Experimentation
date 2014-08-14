# -*- coding: utf-8 -*-
"""
Created on Fri Aug 01 09:20:36 2014

@author: nhpnp3
"""

import numpy as np
import matplotlib.pyplot as plt

el = 21

field_pr = np.load("E11_fft_250cal.npy")
lin_field_pr = np.reshape(field_pr[:,:,:,0],el**3)

plt.close()

plt.subplot(211)
plt.plot(np.real(lin_field_pr[10:]),'k.')
plt.title('Response with unstable BCs: real space')

plt.subplot(212)
plt.plot(np.imag(lin_field_pr[10:]),'b.')
plt.title('Response with unstable BCs: imaginary space')