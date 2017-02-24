import time
import numpy as np


def const():

    C = {}

    """general constants"""
    C['wrt_file'] = 'log_%s.txt' % (time.strftime("%Y-%m-%d_h%H"))

    C['sid'] = ['Ac', 'BaTr', 'Di', 'Dd', 'Id', 'Od',
                'Ra', 'Tr', 'BaTrTr', 'DdTr', 'DiTr', 'OdTr']

    C['names_plt'] = ['A', 'B', 'C', 'H', 'D',
                      'E', 'F', 'G', 'I', 'J', 'K', 'L']
    C['sid_cal'] = ['Ac', 'BaTr', 'Di', 'Dd', 'Id', 'Od',
                    'Ra', 'Tr', 'BaTrTr', 'DiTr', 'OdTr']
    C['sid_val'] = ['DdTr']
    C['names'] = ['actual', 'basaltrans', 'dice', 'doubledonut',
                  'innerdonut', 'outerdonut', 'random', 'trans',
                  'BaTrTr', 'DdTr', 'DiTr', 'OdTr']

    C['strt'] = list(np.zeros(len(C['sid']), dtype='int16'))
    C['ns'] = list(200*np.ones(len(C['sid']), dtype='int16'))
    C['ns_cal'] = list(200*np.ones(len(C['sid_cal']), dtype='int16'))

    C['deuler'] = 'euler'
    C['dfip'] = 'fip'

    C['H'] = 6  # max number of gsh functions

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
    C['n_pc_tot'] = np.sum(C['ns_cal'])

    """number of subclusters to select"""
    C['n_sc'] = 20
    """number of points to sample for each subcluster"""
    C['n_samp'] = 100

    C['pcnt'] = .999

    C['fmax'] = 200
    C['n_pc_max'] = 10
    C['deg_max'] = 2

    return C
