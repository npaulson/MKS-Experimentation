import numpy as np
import db_functions as fn
import h5py
import time
import constants_old


def calculate():

    C = constants_old.const()

    filename = 'Xcalc_log_cos.txt'

    """ Load info from collected simulation info file """

    f = h5py.File(C['combineread_output'], 'r')
    var_set = f.get('var_set')

    theta = var_set[:, 0]

    f.close

    f = h5py.File(C['Xcalccos_output'], 'a')

    """Evalute the cosine basis functions for theta"""

    st = time.time()

    for q in xrange(C['N_q']):

        vec = np.cos(q*np.pi*theta/C['L_th'])

        set_id = 'q_%s' % str(q).zfill(5)
        f.create_dataset(set_id, data=vec)
        fn.WP(set_id, filename)

    msg = "Cosine basis evaluation for theta complete: %ss" \
        % np.round(time.time()-st, 3)
    fn.WP(msg, filename)

    f.close()

if __name__ == '__main__':
    calculate()
