import time
import numpy as np


def const():

    C = {}

    """general constants"""
    C['wrt_file'] = 'log_%s.txt' % (time.strftime("%Y-%m-%d_h%H"))
    C['set_id'] = ['Ac', 'BaTr', 'Di', 'Id', 'Od',
                   'Ra', 'Tr', 'Dd', 'BaTrTr', 'DdTr', 'DiTr', 'OdTr']
    C['names'] = ['A', 'B', 'C', 'D',
                  'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
    C['strt'] = list(np.zeros(len(C['set_id']), dtype='int16'))
    C['ns'] = list(100*np.ones(len(C['set_id']), dtype='int16'))
    C['dir_resp'] = "response"
    C['direc'] = C['set_id']
    C['el'] = 21

    return C
