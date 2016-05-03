# -*- coding: utf-8 -*-
"""
Created on Wed Oct 01 13:52:33 2014

@author: nhpnp3
"""

import numpy as np
import functions as rr
import h5py


def results(el, ns, set_id, step, typ, comp, comp_app, wrt_file, wrt_file2):

    f = h5py.File("data.hdf5", 'r')
    dset_name = '%s%s_fem_%s%s_s%s' % (typ, comp, ns, set_id, step)
    r_fem = f.get(dset_name)[...]
    dset_name = '%s%s_mks_%s%s_s%s' % (typ, comp, ns, set_id, step)
    r_mks = f.get(dset_name)[...]

    dset_name = '%s%s_fem_%s%s_s%s' % (typ, comp_app, ns, set_id, step)
    r_app = f.get(dset_name)[...]
    nfac = r_app.mean()
    del r_app

    f.close()

    error_calc(el, ns, set_id, r_fem, r_mks, typ,
               comp, nfac, wrt_file, wrt_file2)


def error_calc(el, ns, set_id, r_fem, r_mks, typ,
               comp, nfac, wrt_file, wrt_file2):

    err = np.abs(r_fem-r_mks)

    # MEAN ABSOLUTE STRAIN ERROR (MASE)
    max_diff_all = np.amax(err, axis=(1, 2, 3))

    # DIFFERENCE MEASURES
    mean_diff_meas = 100*err.mean()/nfac
    std_diff_meas = 100*err.std()/nfac
    mean_max_diff_meas = 100*max_diff_all.mean()/nfac
    max_diff_meas_all = 100*max_diff_all.max()/nfac

    msg = 'Mean voxel difference over all microstructures'\
        ' (divided by nfac), %s%s: %s%%' \
        % (typ, comp, mean_diff_meas)
    rr.WP(msg, wrt_file)
    msg = 'standard deviation of difference over all microstructures'\
        ' (divided by nfac), %s%s: %s%%' \
        % (typ, comp, std_diff_meas)
    rr.WP(msg, wrt_file)
    msg = 'Average Maximum voxel difference per microstructure'\
        ' (divided by nfac), %s%s: %s%%' \
        % (typ, comp, mean_max_diff_meas)
    rr.WP(msg, wrt_file)
    msg = 'Maximum voxel difference in all microstructures '\
        '(divided by nfac), %s%s: %s%%' \
        % (typ, comp, max_diff_meas_all)
    rr.WP(msg, wrt_file)

    msg = '%s    %s%s    %s    %s    %s    %s' % (set_id, typ, comp, ns,
                                                  mean_diff_meas,
                                                  mean_max_diff_meas,
                                                  max_diff_meas_all)
    rr.WP(msg, wrt_file2)

    # STANDARD STATISTICS
    msg = 'Average, %s%s, FEM: %s' % (typ, comp, r_fem.mean())
    rr.WP(msg, wrt_file)
    msg = 'Average, %s%s, MKS: %s' % (typ, comp, r_mks.mean())
    rr.WP(msg, wrt_file)
    msg = 'Standard deviation, %s%s, FEM: %s' \
        % (typ, comp, r_fem.std())
    rr.WP(msg, wrt_file)
    msg = 'Standard deviation, %s%s, MKS: %s' \
        % (typ, comp, r_mks.std())
    rr.WP(msg, wrt_file)

    r_fem_min = np.amin(r_fem, axis=(1, 2, 3)).mean()
    r_mks_min = np.amin(r_mks, axis=(1, 2, 3)).mean()
    r_fem_max = np.amax(r_fem, axis=(1, 2, 3)).mean()
    r_mks_max = np.amax(r_mks, axis=(1, 2, 3)).mean()

    msg = 'Mean minimum, %s%s, FEM: %s' % (typ, comp, r_fem_min)
    rr.WP(msg, wrt_file)
    msg = 'Mean minimum, %s%s, MKS: %s' % (typ, comp, r_mks_min)
    rr.WP(msg, wrt_file)
    msg = 'Mean maximum, %s%s, FEM: %s' % (typ, comp, r_fem_max)
    rr.WP(msg, wrt_file)
    msg = 'Mean maximum, %s%s, MKS: %s' % (typ, comp, r_mks_max)
    rr.WP(msg, wrt_file)

if __name__ == '__main__':
    el = 21
    ns = 100
    set_id = 'val'
    step = 1
    typ = 'epsilon'
    comp = '11'
    comp_app = '11'
    wrt_file = 'test1.txt'
    wrt_file2 = 'test2.txt'
    results(el, ns, set_id, step, typ, comp, comp_app, wrt_file, wrt_file2)
