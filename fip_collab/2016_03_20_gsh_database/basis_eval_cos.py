import numpy as np
import db_functions as fn
import h5py
import constants


def calculate():

    C = constants.const()

    filename = 'Xcalc_log_cos.txt'

    """ Load info from collected simulation info file """

    f = h5py.File(C['combineread_output'], 'r')
    var_set = f.get('var_set')
    theta = np.sort(np.unique(var_set[:, 0]))
    et_norm = np.sort(np.unique(var_set[:, 4]))
    f.close

    f = h5py.File(C['basis_eval_cos'], 'a')

    """Evalute the cosine basis functions for theta"""

    for q in xrange(C['N_q']):

        vec = np.cos(q*np.pi*theta/C['L_th'])

        set_id = 'q_%s' % str(q).zfill(5)
        f.create_dataset(set_id, data=vec)
        fn.WP(set_id, filename)

    """Evalute the cosine basis functions for en"""

    for r in xrange(C['N_r']):

        vec = np.cos(r*np.pi*(et_norm-C['a'])/C['L_en'])

        set_id = 'r_%s' % str(r).zfill(5)
        f.create_dataset(set_id, data=vec)
        fn.WP(set_id, filename)

    f.close()

if __name__ == '__main__':
    calculate()
