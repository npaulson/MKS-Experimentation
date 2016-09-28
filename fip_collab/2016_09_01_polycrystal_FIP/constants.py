import time
import numpy as np


def const():

    C = {}

    """general constants"""
    C['path'] = '/gpfs/scratch1/3/nhpnp3/4_28_neig'
    C['wrt_file'] = 'log_%s.txt' % (time.strftime("%Y-%m-%d_h%H"))

    C['sid'] = ['Ac', 'BaTr', 'Di', 'Dd', 'Id', 'Od',
                'Ra', 'Tr', 'BaTrTr', 'DdTr', 'DiTr', 'OdTr']
    C['names'] = ['actual', 'basaltrans', 'dice', 'doubledonut',
                  'innerdonut', 'outerdonut', 'random', 'trans',
                  'BaTrTr', 'DdTr', 'DiTr', 'OdTr']

    tmp = [s + 'A' for s in C['sid']] + \
          [s + 'B' for s in C['sid']]
    C['sid_split'] = list(np.sort(tmp))

    C['strt'] = list(np.zeros(len(C['sid']), dtype='int16'))
    C['ns'] = list(200*np.ones(len(C['sid']), dtype='int16'))
    C['ns_split'] = list(100*np.ones(len(C['sid_split']), dtype='int16'))

    C['dir_resp'] = "response"

    C['H'] = 6  # max number of gsh functions

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
    C['n_pc_tot'] = np.sum(C['ns'])

    C['pcnt'] = .995

    C['n_pc_max'] = len(C['sid_split'])-1
    C['deg_max'] = 2

    return C
