import time
import numpy as np


def const():

    C = {}

    """general constants"""
    C['path'] = '/gpfs/scratch1/3/nhpnp3/4_28_neig'
    C['wrt_file'] = 'log_%s.txt' % (time.strftime("%Y-%m-%d_h%H"))

    C['names_cal'] = ['actual', 'basaltrans', 'dice',
                      'innerdonut', 'outerdonut', 'random',
                      'trans']
    C['set_id_cal'] = [s + '_cal' for s in C['names_cal']]
    C['strt_cal'] = [0, 0, 0, 0, 0, 0, 0]
    C['ns_cal'] = [10, 10, 10, 10, 10, 10, 10]
    C['dir_cal'] = C['names_cal']

    C['names_val'] = ['actual', 'basaltrans', 'dice',
                      'innerdonut', 'outerdonut', 'random',
                      'trans', 'doubledonut']
    C['set_id_val'] = [s + '_val' for s in C['names_val']]
    C['strt_val'] = [10, 10, 10, 10, 10, 10, 10, 10]
    C['ns_val'] = [10, 10, 10, 10, 10, 10, 10, 10]
    C['dir_val'] = C['names_val']

    C['dir_resp'] = "response"

    # """set 1"""
    # H1 = 9  # ff.shape[0] = H1
    # H2 = 9  # ff.shape[1] = H2
    # cmax = H1*H2
    # cmat = np.unravel_index(np.arange(cmax), [H1, H2])
    # cmat = np.array(cmat).T

    # """set 2"""
    # H1 = 9  # ff.shape[0] = H1
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
    # cmat = np.array([[1, 1], [2, 2], [3, 3], [4, 4],
    #                  [5, 5], [6, 6], [7, 7], [8, 8]])

    """set5"""
    cmat = np.array([[0, 0], [1, 0], [2, 0], [3, 0],
                     [4, 0], [5, 0], [6, 0], [7, 0],
                     [8, 0], [1, 1], [2, 1], [3, 1],
                     [4, 1], [5, 1], [6, 1], [7, 1],
                     [8, 1]])

    C['cmat'] = cmat
    C['cmax'] = cmat.shape[0]

    C['H'] = 9  # max number of gsh functions
    C['el'] = 21
    C['vmax'] = 21
    C['n_pc_tot'] = np.array(C['ns_cal']).sum()

    C['n_pc_max'] = 30
    C['n_poly_max'] = 1

    return C
