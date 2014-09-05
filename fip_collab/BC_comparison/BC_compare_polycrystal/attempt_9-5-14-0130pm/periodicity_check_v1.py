# -*- coding: utf-8 -*-
"""
Created on Fri Aug 01 09:20:36 2014

@author: nhpnp3
"""

import numpy as np
import matplotlib.pyplot as plt

el = 21

mined = np.load("FE_results_fft_1test.npy")
mined_lin = np.reshape(mined,el**3)

plt.close()

plt.subplot(411)
plt.plot(np.real(mined_lin[1:]),'k.')
plt.title('MINED fftn frequency response: real space')

plt.subplot(412)
plt.plot(np.imag(mined_lin[1:]),'b.')
plt.title('MINED fftn frequency response: imaginary space')


#plt.subplot(211)
#plt.plot(np.absolute(lin_field_pr),'k.')


goali = np.load("dat2.npy")
goali_lin = np.reshape(np.fft.fftn(goali,axes=[0,1,2]),el**3)

plt.subplot(413)
plt.plot(np.real(goali_lin[1:]),'k.')
plt.title('GOALI fftn frequency response: real space')

plt.subplot(414)
plt.plot(np.imag(goali_lin[1:]),'b.')
plt.title('GOALI fftn frequency response: imaginary space')




#plt.subplot(212)
#plt.plot(np.absolute(lin_field_ya[1:]),'b.')