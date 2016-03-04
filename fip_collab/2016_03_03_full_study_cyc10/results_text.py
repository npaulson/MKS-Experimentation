# -*- coding: utf-8 -*-
"""
Created on Wed Oct 01 13:52:33 2014

@author: nhpnp3
"""

import time
import numpy as np
import functions as rr
import h5py


def results(el, ns, set_id, step, typ, comp, newID, traID, nfac):

    """specify the file to write messages to"""
    wrt_file = 'results_step%s_%s%s_%s.txt' % \
               (step, ns, set_id, time.strftime("%Y-%m-%d_h%Hm%M"))

    f = h5py.File("ref_%s%s_s%s.hdf5" % (ns, set_id, step), 'r')

    print f.keys()

    euler = f.get('euler')[...].reshape(ns, 3, el, el, el)
    traSET = f.get('%s%s_%s' % (traID, comp, typ))[...]
    newSET = f.get('%s%s_%s' % (newID, comp, typ))[...]
    f.close()

    error_calc(el, ns, traSET, newSET, typ, comp, nfac, wrt_file)

    maxindx = np.unravel_index(np.argmax(np.abs(traSET - newSET)),
                               traSET.shape)
    maxresp = traSET[maxindx]
    maxMKS = newSET[maxindx]
    maxdiff = (np.abs(traSET - newSET)[maxindx])

    print '\nindices of max error:'
    print maxindx
    print '\nreference response at max error:'
    print maxresp
    print '\nMKS response at max error:'
    print maxMKS
    print '\nmaximum difference in response:'
    print maxdiff
    print euler[maxindx[0], :, maxindx[1], maxindx[2], maxindx[3]]


def error_calc(el, ns, traSET, newSET, typ, comp, nfac, wrt_file):

    """MEAN ABSOLUTE STRAIN ERROR (MASE)"""
    max_diff_all = np.zeros(ns)
    for sn in xrange(ns):
        max_diff_all[sn] = np.amax(np.abs(traSET[sn, ...]-newSET[sn, ...]))

    """DIFFERENCE MEASURES"""
    mean_diff_meas = np.mean(np.abs(traSET-newSET))/nfac
    std_diff_meas = np.std(np.abs(traSET-newSET))/nfac
    mean_max_diff_meas = np.mean(max_diff_all)/nfac
    max_diff_meas_all = np.amax(np.abs(traSET-newSET))/nfac

    msg = 'Mean voxel difference over all microstructures'\
        ' (divided by normalizing factor), %s%s: %s' \
        % (typ, comp, mean_diff_meas)
    rr.WP(msg, wrt_file)
    msg = 'standard deviation of difference over all microstructures'\
        ' (divided by normalizing factor), %s%s: %s' \
        % (typ, comp, std_diff_meas)
    rr.WP(msg, wrt_file)
    msg = 'Average Maximum voxel difference per microstructure'\
        ' (divided by normalizing factor), %s%s: %s' \
        % (typ, comp, mean_max_diff_meas)
    rr.WP(msg, wrt_file)
    msg = 'Maximum voxel difference in all microstructures '\
        '(divided by normalizing factor), %s%s: %s' \
        % (typ, comp, max_diff_meas_all)
    rr.WP(msg, wrt_file)

    """STANDARD STATISTICS"""
    msg = 'Average, %s%s, Traditional Approach: %s' \
        % (typ, comp, np.mean(traSET))
    rr.WP(msg, wrt_file)
    msg = 'Average, %s%s, New Approach: %s' \
        % (typ, comp, np.mean(newSET))
    rr.WP(msg, wrt_file)
    msg = 'Standard deviation, %s%s, Traditional Approach: %s' \
        % (typ, comp, np.std(traSET))
    rr.WP(msg, wrt_file)
    msg = 'Standard deviation, %s%s, New Approach: %s' \
        % (typ, comp, np.std(newSET))
    rr.WP(msg, wrt_file)

    traSET_min = np.mean(np.amin(traSET.reshape([el**3, ns]), axis=0))
    newSET_min = np.mean(np.amin(newSET.reshape([el**3, ns]), axis=0))

    traSET_max = np.mean(np.amax(traSET.reshape([el**3, ns]), axis=0))
    newSET_max = np.mean(np.amax(newSET.reshape([el**3, ns]), axis=0))

    msg = 'Mean minimum, %s%s, Traditional Approach: %s' \
        % (typ, comp, traSET_min)
    rr.WP(msg, wrt_file)
    msg = 'Mean minimum, %s%s, New Approach: %s' \
        % (typ, comp, newSET_min)
    rr.WP(msg, wrt_file)
    msg = 'Mean maximum, %s%s, Traditional Approach: %s' \
        % (typ, comp, traSET_max)
    rr.WP(msg, wrt_file)
    msg = 'Mean maximum, %s%s, New Approach: %s' \
        % (typ, comp, newSET_max)
    rr.WP(msg, wrt_file)


if __name__ == '__main__':
    el = 21
    ns = 100
    set_id = 'val'
    step = 5

    # """parameters to plot strain field"""
    # typ = 'epsilon_t'
    # comp = '11'
    # newID = 'rmks'
    # traID = 'r'
    # nfac = 0.00747

    """parameters to plot fips"""
    typ = 'fip'
    comp = ''
    newID = 'fip'
    traID = 'fipmks'
    nfac = 1.0

    results(el, ns, set_id, step, typ, comp, newID, traID, nfac)
