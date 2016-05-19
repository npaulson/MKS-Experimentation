import numpy as np
import itertools as it
import time


def const():

    C = {}

    """general constants"""
    C['path'] = '/gpfs/scratch1/3/nhpnp3/4_28_neig'
    C['wrt_file'] = 'log_%s.txt' % (time.strftime("%Y-%m-%d"))

    C['ns_cal'] = 10
    C['strt_cal'] = 40
    C['set_id_cal'] = 'cal'
    C['dir_cal'] = 'cal'

    C['ns_val'] = 2
    C['strt_val'] = 2
    C['set_id_val'] = 'val'
    C['dir_val'] = 'val'

    C['H'] = 2
    C['el'] = 21
    C['step'] = 1
    C['ext'] = 5

    # cmax: number of neighbors considered
    C['cmax'] = C['ext']**3

    # # xmax: total number of features for 1st order regression
    # C['xmax'] = 1+(C['H']*C['cmax'])
    # # xmax: total number of features for 2nd order regression
    # C['xmax'] = 1+(C['H']*C['cmax'])+(C['H']*(C['cmax']**2))

    # tmp = it.combinations_with_replacement(np.arange(C['xmax']), 2)
    # C['Imat'] = np.array(list(tmp))
    # C['ImatL'] = C['Imat'].shape[0]

    return C
