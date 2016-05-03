import numpy as np
import itertools as it
import time


def const():

    C = {}

    """general constants"""
    C['path'] = '/gpfs/scratch1/3/nhpnp3/4_28_neig'
    C['wrt_file'] = 'log_%s.txt' % (time.strftime("%Y-%m-%d"))

    C['ns_cal'] = 2
    C['set_id_cal'] = 'cal'
    C['dir_cal'] = 'cal'

    C['ns_val'] = 2
    C['set_id_val'] = 'val'
    C['dir_val'] = 'val'

    C['H'] = 9
    C['el'] = 21
    C['step'] = 1
    C['ext'] = 3

    # cmax: number of neighbors considered
    C['cmax'] = C['ext']**3

    # xmax: total number of features for 2nd order regression
    C['xmax'] = 1+(C['H']*C['cmax'])+(C['H']*(C['cmax']**2))
    # # xmax: total number of features for 1st order regression
    # C['xmax'] = 1+(C['H']*C['cmax'])

    # n_samp: number of data points for regression
    C['n_samp'] = (C['ns_cal'])*(C['el']**3)

    """ """
    tmp = it.combinations_with_replacement(np.arange(C['xmax']), 2)
    C['Imat'] = np.array(list(tmp))
    C['ImatL'] = C['Imat'].shape[0]

    """for read_input_data"""
    C['XhX_njobs'] = 100
    C['XhX_mem'] = 8
    C['XhX_walltime'] = 2
    C['XhX_scriptname'] = 'get_XhX.py'
    C['XhX_output'] = 'XhX_%s.hdf5'

    return C
