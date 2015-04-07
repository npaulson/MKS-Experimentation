# -*- coding: utf-8 -*-
"""
Created on Fri May 23 14:25:50 2014

This script predicts the FE response of a set of microstructures designated by
a specific set-ID using a previously calibrated MKS

@author: nhpnp3
"""

import time
import numpy as np
import functions as rr
import tables as tb
# import matplotlib.pyplot as plt


def validation_zero_pad(el_cal, el_val, ns_cal, ns_val, H, set_id_cal,
                        set_id_val, wrt_file):

    start = time.time()

    # ZERO-PAD THE INFLUENCE COEFFICIENTS

    # open reference HDF5 file
    base_ref = tb.open_file("ref_%s%s.h5" % (ns_cal, set_id_cal), mode="r")
    # assign data to array
    pre_specinfc = base_ref.root.infl_coef.specinfc[...]
    # close HDF5 file
    base_ref.close()

    pre_specinfc = np.reshape(pre_specinfc, [H, el_cal, el_cal, el_cal])
    pre_specinfc = np.fft.ifftn(
        pre_specinfc, [el_cal, el_cal, el_cal], [1, 2, 3])

    # h_comp = 0
    # plt.figure(num=1, figsize=[12, 8])
    # dmin = np.amin(pre_specinfc[h_comp, 0, :, :].real)
    # dmax = np.amax(pre_specinfc[h_comp, 0, :, :].real)

    # plt.subplot(221)
    # ax = plt.imshow(pre_specinfc[h_comp, 0, :, :].real, origin='lower',
    #                 interpolation='none',
    #                 cmap='jet', vmin=dmin, vmax=dmax)
    # plt.colorbar(ax)
    # plt.title('original influence coefficients')

    pre_specinfc = np.fft.fftshift(pre_specinfc, axes=[1, 2, 3])

#    edgeHvec = pre_specinfc[0,0,0,:]

    # plt.subplot(222)
    # slc = np.floor(0.5 * el_cal).astype(int)
    # ax = plt.imshow(pre_specinfc[h_comp, slc, :, :].real, origin='lower',
    #                 interpolation='none',
    #                 cmap='jet', vmin=dmin, vmax=dmax)
    # plt.colorbar(ax)
    # plt.title('centered influence coefficients')

    specinfc_pad = np.zeros([H, el_val, el_val, el_val], dtype='complex64')

#    for h in xrange(H):
#        specinfc_pad[:,:,:,h] = edgeHvec[h]

    el_gap = int(0.5 * (el_val - el_cal))
    el_end = el_val - el_gap
    specinfc_pad[:, el_gap:el_end, el_gap:el_end, el_gap:el_end] = pre_specinfc
    del pre_specinfc

    # plt.subplot(223)
    # slc = np.floor(0.5 * el_val).astype(int)
    # ax = plt.imshow(specinfc_pad[h_comp, slc, :, :].real, origin='lower',
    #                 interpolation='none',
    #                 cmap='jet', vmin=dmin, vmax=dmax)
    # plt.colorbar(ax)
    # plt.title('padded/centered influence coefficients')

    specinfc_pad = np.fft.ifftshift(specinfc_pad, axes=[1, 2, 3])

    # plt.subplot(224)
    # ax = plt.imshow(specinfc_pad[h_comp, 0, :, :].real, origin='lower',
    #                 interpolation='none',
    #                 cmap='jet', vmin=dmin, vmax=dmax)
    # plt.colorbar(ax)
    # plt.title('padded influence coefficients')

    specinfc = np.fft.fftn(specinfc_pad, axes=[1, 2, 3])

    # PERFORM THE PREDICTION PROCEDURE

    # open HDF5 file
    base_D = tb.open_file("D_%s%s.h5" % (ns_val, set_id_val), mode="r")
    # define an object for the array
    M_all = base_D.root.msf.M_all

    r_mks = np.zeros([ns_val, el_val, el_val, el_val])

    for sn in xrange(ns_val):

        M = M_all[sn, ...]

        M = M.reshape([H, el_val, el_val, el_val])

        tmp = np.sum(np.conjugate(specinfc) * M, 0)
        # tmp = np.sum(np.conjugate(specinfc) * M, 1)

        del M

        r_mks[sn, ...] = np.fft.ifftn(tmp, [el_val, el_val, el_val],
                                      [0, 1, 2]).real

        del tmp

    # close calibration HDF5 file
    base_D.close()

    # open reference HDF5 file
    base_ref = tb.open_file("ref_%s%s.h5" % (ns_val, set_id_val), mode="a")
    # make reference to the desired node
    group = base_ref.root.epsilon
    # save the MKS total strain prediction
    base_ref.create_array(group,
                          'r_mks',
                          r_mks,
                          'repsonse field as predicted by the MKS')

    # now we want to calculate the MKS predicted plastic strain by
    # subtracting the FEM elastic strain from the MKS predicted total strain

    # first we have to retrieve the FEM total strain fields
    r_fem_t = group.r_fem[...]
    # now we find the group for the FEM plastic strain
    group = base_ref.root.epsilon_p
    # next we retrieve the FEM plastic strain
    r_fem_p = group.r_fem[...]
    # now we calculate the MKS plastic strain field
    r_mks_p = r_mks - (r_fem_t - r_fem_p)
    # now we save the MKS plastic strain field
    base_ref.create_array(group,
                          'r_mks',
                          r_mks_p,
                          'repsonse field as predicted by the MKS')

    # close HDF5 file
    base_ref.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = 'validation performed: %s seconds' % timeE
    rr.WP(msg, wrt_file)
