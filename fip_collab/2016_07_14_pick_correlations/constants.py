import time
import numpy as np


def const():

    C = {}

    """general constants"""
    C['path'] = '/gpfs/scratch1/3/nhpnp3/4_28_neig'
    C['wrt_file'] = 'log_%s.txt' % (time.strftime("%Y-%m-%d_h%H"))

    C['names_cal'] = ['Ac', 'BaTr', 'Di', 'Id', 'Od', 'Ra', 'Tr']
    C['set_id_cal'] = [s + '_cal' for s in C['names_cal']]
    C['strt_cal'] = [0, 0, 0, 0, 0, 0, 0]
    C['ns_cal'] = [30, 30, 30, 30, 30, 30, 30]
    C['dir_cal'] = C['names_cal']

    C['names_val'] = ['Ac', 'BaTr', 'Di', 'Id', 'Od', 'Ra', 'Tr',
                      'BaTrTr', 'Dd', 'DdTr', 'DiTr', 'OdTr']
    C['set_id_val'] = [s + '_val' for s in C['names_val']]
    C['strt_val'] = [30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]
    C['ns_val'] = [30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]
    C['dir_val'] = C['names_val']

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

    # """setA"""
    # H1 = C['H']  # ff.shape[0] = H1
    # H2 = C['H']  # ff.shape[1] = H2
    # cmax = H1*H2
    # cmat = np.unravel_index(np.arange(cmax), [H1, H2])
    # cmat = np.array(cmat).T

    # """setB"""
    # cmat = np.array([[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0]])

    # """setC"""
    # cmat = np.array([[0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1]])

    # """setD"""
    # cmat = np.array([[0, 0], [0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1]])

    # """setE"""
    # cmat = np.array([[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0],
    #                  [0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1]])

    # """setF"""
    # cmat = np.array([[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0],
    #                  [1, 1], [2, 1], [3, 1], [4, 1], [5, 1]])

    # """setG"""
    # cmat = np.array([[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0],
    #                  [1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [2, 2],
    #                  [3, 3], [4, 4], [5, 5]])

    # """setH"""
    # cmat = np.array([[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0],
    #                  [1, 1], [2, 2], [3, 3], [4, 4], [5, 5]])

    """setI"""
    cmat = np.array([[0, 0], [1, 0], [1, 1], [2, 0], [2, 1], [2, 2],
                     [3, 0], [3, 1], [3, 2], [3, 3], [4, 0], [4, 1],
                     [4, 2], [4, 3], [4, 4], [5, 0], [5, 1], [5, 2],
                     [5, 3], [5, 4], [5, 5]])

    # """set4"""
    # cmat = []
    # for ii in xrange(C['H']):
    #     cmat.append([ii, ii])
    # cmat = np.array(cmat)

    # """set5"""
    # cmat = []
    # for ii in xrange(C['H']):
    #     cmat.append([0, ii])
    # for ii in xrange(1, C['H']):
    #     cmat.append([1, ii])
    # cmat = np.array(cmat)

    C['cmat'] = cmat
    C['cmax'] = cmat.shape[0]

    C['el'] = 21
    C['vmax'] = 21
    C['n_pc_tot'] = 150
    C['ev_lvl'] = 99.5

    C['n_pc_max'] = 60
    C['n_poly_max'] = 1

    return C
