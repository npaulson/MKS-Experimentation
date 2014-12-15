# -*- coding: utf-8 -*-
"""
Created on Thu Nov 13 15:24:50 2014

modified for 

@author: nhpnp3
"""

from stiffness_calculator_v3 import stiffness_calc
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import scipy.io as sio

base = 3

phi1vec = np.linspace(0,2*np.pi,12*base)
#Phivec = np.arccos(np.linspace(0,1,3*base))
Phivec = np.linspace(0,np.pi,6*base)
phi2vec = np.linspace(0,np.pi/3,2)

[phi1,Phi,phi2] = np.meshgrid(phi1vec,Phivec,phi2vec)

phi1 = np.swapaxes(phi1,0,1)
Phi = np.swapaxes(Phi,0,1)
phi2 = np.swapaxes(phi2,0,1)


start = time.time()

plt.close('all')

fig = plt.figure(num=1, figsize=plt.figaspect(1))
ax3D = fig.add_subplot(111, projection='3d')
p3d = ax3D.scatter(phi1[:],Phi[:],phi2[:])
plt.title('Binning of the Hexagonal-Triclinic Fundamental Zone')
ax3D.set_xlabel("$\phi1$")
ax3D.set_ylabel("$\Phi$")
ax3D.set_zlabel("$\phi2$")
ax3D.set_xlim3d(0, 2*np.pi)
ax3D.set_ylim3d(0, np.pi)
ax3D.set_zlim3d(0, np.pi/3)

end = time.time()
timeE = np.round(end - start,3)
print 'plotting time: %s seconds' %timeE


start = time.time()

CsM = np.zeros([phi1.size,6,6])

for cc in xrange(phi1.size):
    [p1,P,p2] = np.unravel_index(cc,phi1.shape)
    
    [Cs,CsM[cc,...]] = stiffness_calc([phi1vec[p1],Phivec[P],phi2vec[p2]])    
 

   
end = time.time()
timeE = np.round(end - start,3)
print 'stiffness evaluation: %s seconds' %timeE    
    

start = time.time()

orilist_old = range(CsM.shape[0])
orilist_new = range(CsM.shape[0])

unique_list1 = []
unique_list2 = []

for cc in xrange(CsM.shape[0]):
    
    if np.any(np.array(orilist_old) == cc) == False:
        continue

    for dd in orilist_old:

#        if np.allclose(CsM[cc,...],CsM[dd,...], rtol=1E-15):           
        if np.allclose(CsM[cc,...],CsM[dd,...], rtol=1E-10):           
            orilist_new.remove(dd)
            unique_list1.append(dd)
            unique_list2.append(cc)
    
    orilist_old = list(orilist_new)

end = time.time()
timeE = np.round(end - start,3)
print 'locate duplicates: %s seconds' %timeE  


uniqueCC = np.unique(unique_list2)
uniquephiindx = np.unravel_index(uniqueCC,phi1.shape)

uniquephi1 = phi1vec[uniquephiindx[0]]
uniquePhi = Phivec[uniquephiindx[1]]
uniquephi2 =  phi2vec[uniquephiindx[2]]

start = time.time()

fig = plt.figure(num=2, figsize=plt.figaspect(1))
ax3D = fig.add_subplot(111, projection='3d')
p3d = ax3D.scatter(uniquephi1,uniquePhi,uniquephi2)
plt.title('Orientations with Unique Stiffness Matrices in the Hexagonal-Triclinic Fundamental Zone')
ax3D.set_xlabel("$\phi1$")
ax3D.set_ylabel("$\Phi$")
ax3D.set_zlabel("$\phi2$")
ax3D.set_xlim3d(0, 2*np.pi)
ax3D.set_ylim3d(0, np.pi)
ax3D.set_zlim3d(0, np.pi/3)

end = time.time()
timeE = np.round(end - start,3)
print 'plotting time: %s seconds' %timeE


eulers = np.unravel_index(range(phi1.size),phi1.shape)

eulervec = np.zeros([phi1.size,3])
eulervec[:,0] = phi1vec[eulers[0]]
eulervec[:,1] = Phivec[eulers[1]]
eulervec[:,2] = phi2vec[eulers[2]]

sio.savemat('orientation_large',{'unique_list1':unique_list1,'unique_list2':unique_list2,'phi1vec':phi1vec,'Phivec':Phivec,'phi2vec':phi2vec,'eulervec':eulervec})
