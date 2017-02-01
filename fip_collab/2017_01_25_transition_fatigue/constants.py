import time
import numpy as np


def const():

    C = {}

    """general constants"""
    C['path'] = '/gpfs/scratch1/3/nhpnp3/4_28_neig'
    C['wrt_file'] = 'log_%s.txt' % (time.strftime("%Y-%m-%d_h%H"))

    C['sid'] = ['Ac', 'BaTr', 'Dd', 'Di', 'Id', 'Od',
                'Ra', 'Tr', 'BaTrTr', 'DdTr', 'DiTr', 'OdTr']
    C['sid_cal'] = ['Ac', 'BaTr', 'Di', 'Id', 'Od',
                    'Ra', 'Tr', 'BaTrTr', 'DiTr', 'OdTr']
    C['sid_val'] = ['Dd', 'DdTr']
    C['names'] = ['actual', 'basaltrans', 'doubledonut', 'dice',
                  'innerdonut', 'outerdonut', 'random', 'trans',
                  'BaTrTr', 'DdTr', 'DiTr', 'OdTr']
    C['direc'] = C['sid']

    C['strt'] = list(np.zeros(len(C['sid']), dtype='int16'))
    C['ns'] = list(265*np.ones(len(C['sid']), dtype='int16'))
    C['ns_cal'] = list(265*np.ones(len(C['sid_cal']), dtype='int16'))

    C['dir_resp'] = "response"

    C['H'] = 15  # max number of gsh functions
    C['alpha'] = 1.07  # shape parameter for gamma distribution

    # """set 1"""
    # H1 = C['H']  # ff.shape[0] = H1
    # H2 = C['H']  # ff.shape[1] = H2
    # cmax = H1*H2
    # cmat = np.unravel_index(np.arange(cmax), [H1, H2])
    # cmat = np.array(cmat).T

    # """set 2"""
    # H1 = C['H']  # ff.shape[0] = H1
    # H2 = 1  # ff.shape[1] = H2
    # cmax = H1*H2
    # cmat = np.unravel_index(np.arange(cmax), [H1, H2])
    # cmat = np.array(cmat).T

    # """set3"""
    # cmat = np.array([[0, 0], [1, 0], [2, 0], [3, 0],
    #                  [4, 0], [5, 0], [6, 0], [7, 0],
    #                  [8, 0], [1, 1], [2, 2], [3, 3],
    #                  [4, 4], [5, 5], [6, 6], [7, 7],
    #                  [8, 8]])

    # """set4"""
    # cmat = []
    # for ii in xrange(C['H']):
    #     cmat.append([ii, ii])
    # cmat = np.array(cmat)

    """set5"""
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
    C['n_samp'] = 150

    C['pcnt'] = .9995

    # C['n_pc_max'] = len(C['sid'])*2*C['n_pc_samp']-1
    C['n_pc_max'] = 15
    C['deg_max'] = 3

    return C
