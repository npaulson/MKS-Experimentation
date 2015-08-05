import numpy as np
# import matplotlib.pyplot as plt
import h5py

n_phi1 = 120
n_Phi = 31
n_phi2 = 20
n_tot = n_phi1 * n_Phi * n_phi2

# Read Simulation info from "sim" file

filename = 'sim_Ti64_tensor_11.txt'

f = open(filename, "r")

linelist = f.readlines()

print linelist[0]
stmax = linelist[1].split()[4:7]

test_no = np.zeros([n_tot], dtype='int8')
euler = np.zeros([n_tot, 3])

for k in xrange(n_tot):
    temp_line = linelist[k+1]
    # test_no[k] = temp_line.split()[0]
    euler[k, :] = temp_line.split()[1:4]

f.close()

# print test_no[10]
print euler[10, :]

etvec = np.linspace(.006, .01, 41)

# Get data for all simulations

# open file containing Matthew's data
filename = 'Results_tensor_11.hdf5'
f_mwp = h5py.File(filename, 'r')

# create file for pre-database outputs
f_nhp = h5py.File('testwrite.hdf5', 'w')
realD = f_nhp.create_dataset("realD", (n_phi1, n_Phi, n_phi2, 41))

# for ii in xrange(n_tot):
for ii in xrange(2):

    test_id = 'sim%s' % str(ii+1).zfill(7)
    print test_id

    dset = f_mwp.get(test_id)

    """
    Column order in each dataset:
    time,...
    sig11,sig22,sig33,sig12,sig13,sig23...
    e11,e22,e33,e12,e13,e23
    ep11,ep22,ep33,ep12,ep13,ep23
    """

    et = dset[:, 7:13]
    ep = dset[:, 13:19]

    # check that et is traceless
    et_tr = et[:, 0] + et[:, 1] + et[:, 2]

    et_tr_max = np.max(np.abs(et_tr))

    if et_tr_max > 1E-4:
        print ii
        print et_tr_max

    # calculate the norm of et
    et_norm = np.sqrt(et[:, 0]**2 + et[:, 1]**2 + et[:, 2]**2 +
                      et[:, 3]**2 + et[:, 4]**2 + et[:, 5]**2)

    # check that et_norm is close enough to our approximation

    # find the maximum percent deviation between etvec and et_norm
    et_err = 100*np.max(np.abs((etvec-et_norm[59:])/etvec))
    et_err = et_err

    if et_err > 1:
        print ii
        msg = "maximum %% devation in et_norm scales: %s%%" % et_err
        print msg

    # calculate the invariants of the plastic strain

    # I1 = ep[:,0] + ep[:,1] + ep[:,2]
    I2 = ep[:, 0]*ep[:, 1] + ep[:, 1]*ep[:, 2] + ep[:, 2]*ep[:, 0] + \
        ep[:, 3]**2 + ep[:, 4]**2 + ep[:, 5]**2
    I3 = ep[:, 0]*ep[:, 1]*ep[:, 2] - \
        ep[:, 0]*ep[:, 5]**2 - ep[:, 1]*ep[:, 4]**2 - ep[:, 2]*ep[:, 3]**2 + \
        2*ep[:, 3]*ep[:, 4]*ep[:, 5]

    # for the first example only save I2

    eindx = np.int16(np.round((180./(3.*np.pi))*euler[ii, :]))

    realD[eindx[0], eindx[1], eindx[2], :] = I2[59:]

    # I1 = ep[:,0] + ep[:,1] + ep[:,2]
    # I2 = ep[:,0]*ep[:,1] + ep[:,1]*ep[:,2] + ep[:,2]*ep[:,0]
    # I3 = ep[:,0]*ep[:,1]*ep[:,2]

f_mwp.close()
f_nhp.close()

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
