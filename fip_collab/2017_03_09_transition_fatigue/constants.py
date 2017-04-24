import time
import numpy as np


def const():

    C = {}

    """general constants"""
    C['ncld'] = 300

    C['wrt_file'] = 'log_%s.txt' % (time.strftime("%Y-%m-%d_h%H"))

    C['sid'] = ['A', 'B', 'C', 'D',
                'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
    C['sid_cal'] = ['A', 'B', 'C', 'D',
                    'E', 'F', 'G', 'H', 'I', 'K', 'L']
    C['sid_val'] = ['J']

    C['strt'] = list(np.zeros(len(C['sid']), dtype='int16'))
    C['ns'] = list(C['ncld']*np.ones(len(C['sid']), dtype='int16'))
    C['ns_cal'] = list(C['ncld']*np.ones(len(C['sid_cal']), dtype='int16'))

    C['H'] = 41  # max number of gsh functions

    """select the 2-pt spatial correlations"""
    cmat = []
    for ii in xrange(C['H']):
        cmat.append([0, ii])
    for ii in xrange(1, C['H']):
        cmat.append([1, ii])
    cmat = np.array(cmat)

    C['cmat'] = cmat
    C['cmax'] = cmat.shape[0]

    C['el'] = 21
    C['vmax'] = 21
    # C['n_pc_tot'] = np.sum(C['ns_cal'])
    C['n_pc_tot'] = 100

    """number of subclusters to select"""
    C['n_sc'] = 20
    """number of points to sample for each subcluster"""
    C['n_samp'] = 150
    C['alpha'] = 1.15

    C['pcnt'] = .999

    C['fmax'] = 200
    C['n_pc_max'] = 25
    C['deg_max'] = 2
    # C['n_pc_max'] = 10
    # C['deg_max'] = 3

    return C
