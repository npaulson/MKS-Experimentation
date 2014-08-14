# -*- coding: utf-8 -*-
"""
Created on Fri Aug 01 09:20:36 2014

@author: nhpnp3
"""

import numpy as np
import matplotlib.pyplot as plt

el = 21

field_pr = np.load("E11_fft_5bc_test.npy")
lin_field_pr = np.reshape(field_pr[:,:,:,0],el**3)


plt.close()

plt.subplot(411)
plt.plot(np.real(lin_field_pr[1:]),'k.')
plt.title('Response with unstable BCs: real space')

plt.subplot(412)
plt.plot(np.imag(lin_field_pr[1:]),'b.')
plt.title('Response with unstable BCs: imaginary space')


#plt.subplot(211)
#plt.plot(np.absolute(lin_field_pr),'k.')


field_ya = np.load("FE_results_fft_200cal.npy")
lin_field_ya = np.reshape(field_ya[:,:,:,0],el**3)

plt.subplot(413)
plt.plot(np.real(lin_field_ya[1:]),'k.')
plt.title('Response with stable BCs: real space')

plt.subplot(414)
plt.plot(np.imag(lin_field_ya[1:]),'b.')
plt.title('Response with stable BCs: imaginary space')


E = np.load('E_5bc_test.npy')
print np.mean(E[:,:,0], axis = 0)



#plt.subplot(212)
#plt.plot(np.absolute(lin_field_ya[1:]),'b.')