# -*- coding: utf-8 -*-
"""
Created on Fri Aug 01 09:20:36 2014

@author: nhpnp3
"""

import numpy as np
import matplotlib.pyplot as plt

el = 21

field_pr = np.load("E11_fft_250cal.npy")
lin_field_pr = np.reshape(field_pr[:,:,:,100],el**3)


plt.close()

plt.subplot(411)
plt.plot(np.real(lin_field_pr),'k.')

plt.subplot(412)
plt.plot(np.imag(lin_field_pr),'b.')



field_ya = np.load("FE_results_fft_200cal.npy")
lin_field_ya = np.reshape(np.mean(field_ya, axis = 3),el**3)

plt.subplot(413)
plt.plot(np.real(lin_field_ya[1:]),'k.')

plt.subplot(414)
plt.plot(np.imag(lin_field_ya[1:]),'b.')