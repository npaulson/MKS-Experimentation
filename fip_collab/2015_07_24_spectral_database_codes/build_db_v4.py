import numpy as np
import h5py
import leg_interp_func as lif

# initialize important variables

comp = "11"  # strain component of interest

n_phi1 = 72  # number of phi1 samples
n_Phi = 72  # number of Phi samples
n_phi2 = 72  # number of phi2 samples
n_theta = 13  # number of theta samples
n_tot = n_phi1 * n_Phi * n_phi2  # total number of orientations

a = .0064  # start of range for legendre interpolation
b = .0096  # end of range for legendre interpolation

# highest order legendre polynomial in the fourier representation
N = 10

maxerr = 0  # maximum % error seen for any et vs ep curve

# create file for pre-database outputs
f_nhp = h5py.File('coeff_extract.hdf5', 'w')
ep_set = f_nhp.create_dataset("ep_set",
                              (n_theta, n_phi1, n_Phi, n_phi2, N+1))

for tnum in xrange(n_theta):

    # Read Simulation info from "sim" file
    filename = 'sim_Ti64_tensor_%s.txt' % str(tnum+1).zfill(2)

    f = open(filename, "r")

    linelist = f.readlines()

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
    filename = 'Results_tensor_%s.hdf5' % str(tnum+1).zfill(2)
    f_mwp = h5py.File(filename, 'r')

    if tnum == 0:
        euler_set = f_nhp.create_dataset("euler_set", euler.shape)
        euler_set[...] = euler

    for ii in xrange(0, n_tot):

        test_id = 'sim%s' % str(ii+1).zfill(7)

        if ii % 10000 == 0:
            print tnum
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

        # check that this curve is represented well with legendre polynomial

        ep11 = ep[:, 0]

        nodes, weights, rootsamp = lif.get_nodes(et_norm, ep11, a, b, N)

        coeff_set = lif.get_coeff(nodes, weights, rootsamp, N)

        ytest = lif.get_interp(et_norm[63:96], coeff_set, a, b)

        # calculate error in this approach based on sampled values
        error = 100*np.abs((ep11[63:96] - ytest)/np.max(np.abs(ep11[63:96])))

        if np.max(error) > maxerr:
            print euler[ii, :]
            print np.mean(error)
            print np.max(error)
            maxerr = np.max(error)

            np.save("ep11.npy", ep11)
            np.save("et_norm.npy", et_norm)
            np.save("coeff_set.npy", coeff_set)
            # break
        # print euler[ii, :]
        # print np.mean(error)
        # print np.max(error)

        eindx = np.int16(np.round((180./(5.*np.pi))*euler[ii, :]))

        ep_set[tnum, eindx[0], eindx[1], eindx[2], :] = coeff_set

    f_mwp.close()
f_nhp.close()
