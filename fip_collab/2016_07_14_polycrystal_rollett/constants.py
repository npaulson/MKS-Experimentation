import time
import numpy as np


def const():

    C = {}

    """general constants"""
    C['path'] = '/gpfs/pace1/project/me-kalidindi/shared/Ti64_spatial_stats'
    C['wrt_file'] = 'log_%s.txt' % (time.strftime("%Y-%m-%d_h%H"))

    C['names'] = [r'equiaxed, 15% $\alpha$',
                  r'equiaxed, 30% $\alpha$',
                  r'equiaxed, 40% $\alpha$',
                  r'equiaxed, 50% $\alpha$',
                  r'equiaxed, 60% $\alpha$',
                  r'equiaxed, 65% $\alpha$',
                  r'rolled (x-dir), 15% $\alpha$',
                  r'rolled (x-dir), 30% $\alpha$',
                  r'rolled (x-dir), 40% $\alpha$',
                  r'rolled (x-dir), 50% $\alpha$',
                  r'rolled (x-dir), 60% $\alpha$',
                  r'rolled (x-dir), 65% $\alpha$',
                  r'rolled (z-dir), 15% $\alpha$',
                  r'rolled (z-dir), 30% $\alpha$',
                  r'rolled (z-dir), 40% $\alpha$',
                  r'rolled (z-dir), 50% $\alpha$',
                  r'rolled (z-dir), 60% $\alpha$',
                  r'rolled (z-dir), 65% $\alpha$']

    C['set_id'] = ['equi15', 'equi30', 'equi40',
                   'equi50', 'equi60', 'equi65',
                   'rollx15', 'rollx30', 'rollx40',
                   'rollx50', 'rollx60', 'rollx65',
                   'rollz15', 'rollz30', 'rollz40',
                   'rollz50', 'rollz60', 'rollz65']

    C['dir_micr'] = "microstructure"
    C['dir_resp'] = "response"

    C['H_cub'] = 23
    C['H_hex'] = 41
    C['H'] = C['H_cub'] + C['H_hex']

    cmat = []
    for ii in xrange(C['H']):
        cmat.append([0, ii])
    for ii in xrange(1, C['H']):
        cmat.append([1, ii])
    for ii in xrange(2, C['H']):
        cmat.append([ii, ii])
    cmat = np.array(cmat)

    # print cmat

    C['cmat'] = cmat
    C['cmax'] = cmat.shape[0]

    C['el'] = 225
    C['vmax'] = 81
    C['n_pc_tot'] = 17

    C['n_pc_max'] = C['n_pc_tot']
    C['n_poly_max'] = 1

    C['read_njobs'] = 12
    C['read_mem'] = 10
    C['read_walltime'] = 1
    C['read_scriptname'] = 'get_euler.py'

    C['rotate_njobs'] = 6
    C['rotate_mem'] = 5
    C['rotate_walltime'] = 1
    C['rotate_scriptname'] = 'rotate_micr.py'

    C['corr_njobs'] = 18
    C['corr_mem'] = 40
    C['corr_walltime'] = 1
    C['corr_scriptname'] = 'correlate.py'

    return C
