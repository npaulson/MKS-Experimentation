import numpy as np
# import matplotlib.pyplot as plt
import h5py

n_phi1 = 120
n_Phi = 31
n_phi2 = 20
n_tot = n_phi1 * n_Phi * n_phi2   

# Read Simulation info from "sim" file

filename = 'sim_Ti64_tensor_01.txt'

f = open(filename, "r")

linelist = f.readlines()

print linelist[0]
stmax = linelist[1].split()[4:7]

test_no = np.zeros([n_tot], dtype='int8')
euler = np.zeros([n_tot, 3])

for k in xrange(n_tot):
    temp_line = linelist[k+1]
    test_no[k] = temp_line.split()[0]
    euler[k,:] = temp_line.split()[1:4]

f.close()

print test_no[10]
print euler[10,:]

# Get data for specific simulation

ii = 10000

filename = 'Results_tensor_01.hdf5'

f = h5py.File(filename, 'r')

test_id = 'sim%s' % str(test_no[ii]).zfill(7)

print test_id

dset = f.get(test_id)

"""
Column order in each dataset:
time,...
sig11,sig22,sig33,sig12,sig13,sig23...
e11,e22,e33,e12,e13,e23
ep11,ep22,ep33,ep12,ep13,ep23
"""

time = dset[:,0]
sig = dset[:, 1:7]
et = dset[:, 7:13]
ep = dset[:,13:19]

et_norm = np.sqrt(et[:, 0]**2 + et[:, 1]**2 + et[:, 2]**2 +
                 et[:, 3]**2 + et[:, 4]**2 + et[:, 5]**2)

I1 = ep[:,0] + ep[:,1] + ep[:,2]
I2 = ep[:,0]*ep[:,1] + ep[:,1]*ep[:,2] + ep[:,2]*ep[:,0] + \
     ep[:,3]**2 + ep[:,4]**2 + ep[:,5]**2
I3 = ep[:,0]*ep[:,1]*ep[:,2] - \
     ep[:,0]*ep[:,5]**2 - ep[:,1]*ep[:,4]**2 - ep[:,2]*ep[:,3]**2 +\
     2*ep[:,3]*ep[:,4]*ep[:,5]  

np.save('et',et)
np.save('ep',ep)
np.save('sig',sig)
np.save('et_norm',et_norm)
np.save('I1',I1)
np.save('I2',I2)
np.save('I3',I3)

# I1 = ep[:,0] + ep[:,1] + ep[:,2]
# I2 = ep[:,0]*ep[:,1] + ep[:,1]*ep[:,2] + ep[:,2]*ep[:,0]
# I3 = ep[:,0]*ep[:,1]*ep[:,2] 

stmax = et[-1, :]

print stmax
# print et_norm

print I1[95:]
print I2[95:]
print I3[95:]

print ep[95:,0]
print ep[95:,1]
print ep[95:,2]

tmp = et_norm - np.roll(et_norm, 1)
tmp = tmp[1:]
print np.mean(tmp)
print np.std(tmp)

# # Plot the stress strain curve for the 11 component
# plt.figure(num=1, figsize=[7, 5])

# plt.plot(et[:, 0], sig[:, 0])

# plt.xlabel("$\epsilon^t_11$")
# plt.ylabel("$\sigma_11$ (MPa)")
# plt.title("Stress-strain curve")

# # Plot the plastic strain versus total strain
# plt.figure(num=2, figsize=[7, 5])

# plt.plot(et[:, 0], ep[:, 0])

# plt.xlabel("$\epsilon^t_11$")
# plt.ylabel("$\epsilon^p_11$")
# plt.title("$\epsilon^t_11$ vs. $\epsilon^p_11$")