# -*- coding: utf-8 -*-
"""
Created on Wed Oct 01 13:52:33 2014

@author: nhpnp3
"""

import numpy as np
import functions as rr
import tables as tb


def results(el, ns, set_id, step, typ, comp, spri, ii, wrt_file, wrt_file2):

    # open reference HDF5 file
    base = tb.open_file("ref_%s%s_s%s.h5" % (ns, set_id, step),
                        mode="r")
    response = base.get_node('/%s_%s' % (typ, spri), 'r%s' % comp)

    r_fem = response.r_fem[...]
    # close the HDF5 file
    base.close()

    # open reference HDF5 file
    base = tb.open_file("gsh_try_%s%s_s%s.h5" % (ns, set_id, step),
                        mode="r")
    response = base.get_node('/%s_%s' % (typ, spri), 'r%s' % comp)

    r_mks = response.r_mks[...]
    # close the HDF5 file
    base.close()

    nfac = 0.00747

    error_calc(el, ns, r_fem, r_mks, typ, comp, spri, nfac, ii, wrt_file, wrt_file2)


def error_calc(el, ns, r_fem, r_mks, typ, comp, spr, nfac, ii, wrt_file, wrt_file2):

    # MEAN ABSOLUTE STRAIN ERROR (MASE)
    max_diff_all = np.zeros(ns)
    for sn in xrange(ns):
        max_diff_all[sn] = np.amax(abs(r_fem[sn, ...]-r_mks[sn, ...]))

    # DIFFERENCE MEASURES
    mean_diff_meas = (np.mean(abs(r_fem-r_mks))/nfac)*100
    std_diff_meas = (np.std(abs(r_fem-r_mks))/nfac)*100
    mean_max_diff_meas = (np.mean(max_diff_all)/nfac)*100
    max_diff_meas_all = (np.amax(abs(r_fem-r_mks))/nfac)*100

    msg = 'Mean voxel difference over all microstructures'\
        ' (divided by applied strain), %s_%s%s: %s%%' \
        % (typ, spr, comp, mean_diff_meas)
    rr.WP(msg, wrt_file)
    msg = 'standard deviation of difference over all microstructures'\
        ' (divided by applied strain), %s_%s%s: %s%%' \
        % (typ, spr, comp, std_diff_meas)
    rr.WP(msg, wrt_file)
    msg = 'Average Maximum voxel difference per microstructure'\
        ' (divided by applied strain), %s_%s%s: %s%%' \
        % (typ, spr, comp, mean_max_diff_meas)
    rr.WP(msg, wrt_file)
    msg = 'Maximum voxel difference in all microstructures '\
        '(divided by applied strain), %s_%s%s: %s%%' \
        % (typ, spr, comp, max_diff_meas_all)
    rr.WP(msg, wrt_file)

    msg = '%s    %s    %s    %s' % (ii, mean_diff_meas, mean_max_diff_meas,
                                    max_diff_meas_all)
    rr.WP(msg, wrt_file2)

    # STANDARD STATISTICS
    msg = 'Average, %s_%s%s, FEM: %s' % (typ, spr, comp, np.mean(r_fem))
    rr.WP(msg, wrt_file)
    msg = 'Average, %s_%s%s, MKS: %s' % (typ, spr, comp, np.mean(r_mks))
    rr.WP(msg, wrt_file)
    msg = 'Standard deviation, %s_%s%s, FEM: %s' \
        % (typ, spr, comp, np.std(r_fem))
    rr.WP(msg, wrt_file)
    msg = 'Standard deviation, %s_%s%s, MKS: %s' \
        % (typ, spr, comp, np.std(r_mks))
    rr.WP(msg, wrt_file)

    r_fem_min = np.mean(np.amin(r_fem.reshape([el**3, ns]), axis=0))
    r_mks_min = np.mean(np.amin(r_mks.reshape([el**3, ns]), axis=0))

    r_fem_max = np.mean(np.amax(r_fem.reshape([el**3, ns]), axis=0))
    r_mks_max = np.mean(np.amax(r_mks.reshape([el**3, ns]), axis=0))

    msg = 'Mean minimum, %s_%s%s, FEM: %s' % (typ, spr, comp, r_fem_min)
    rr.WP(msg, wrt_file)
    msg = 'Mean minimum, %s_%s%s, MKS: %s' % (typ, spr, comp, r_mks_min)
    rr.WP(msg, wrt_file)
    msg = 'Mean maximum, %s_%s%s, FEM: %s' % (typ, spr, comp, r_fem_max)
    rr.WP(msg, wrt_file)
    msg = 'Mean maximum, %s_%s%s, MKS: %s' % (typ, spr, comp, r_mks_max)
    rr.WP(msg, wrt_file)

if __name__ == '__main__':
    results(21, 398, 'val', 5, 4, 'epsilon', '23', 't_b')
