import numpy as np
import h5py

n_phi1 = 72
n_Phi = 72
n_phi2 = 72
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
    euler[k, :] = temp_line.split()[1:4]

f.close()

etvec = np.linspace(.0001, .0100, 100)

# Get data for all simulations

# open file containing Matthew's data
filename = 'Results_tensor_01.hdf5'
f_mwp = h5py.File(filename, 'r')

# create file for pre-database outputs
f_nhp = h5py.File('tensor_01.hdf5', 'w')
ep_set = f_nhp.create_dataset("ep_set", (n_phi1, n_Phi, n_phi2, 100))
euler_set = f_nhp.create_dataset("euler_set", euler.shape)
euler_set[:, :] = euler

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
    et_err = 100*np.abs((etvec-et_norm)/etvec)

    print et_norm
    print etvec
    print et_err
    print dset[:, 0]
    print dset[:, 1]

    if np.max(et_err) > 1:
        print ii
        msg = "maximum %% devation in et_norm scales: %s%%" % np.max(et_err)
        print msg

    eindx = np.int16(np.round((180./(5.*np.pi))*euler[ii, :]))

    ep_set[eindx[0], eindx[1], eindx[2], :] = ep[:, 0]

f_mwp.close()
f_nhp.close()
