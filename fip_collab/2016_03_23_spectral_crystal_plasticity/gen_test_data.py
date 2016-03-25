import numpy as np
import gsh_cub_tri_L0_16 as gsh
import db_functions as fn
import constants
import h5py


def gen():

    C = constants.const()

    filename = 'log_gen_test_data.txt'

    inc2rad = C['inc']*np.pi/180.

    """get the test euler angle set"""

    thetavec = (np.arange(C['n_th'])+0.5)*inc2rad
    phi1vec = (np.arange(C['n_p1'])+0.5)*inc2rad
    phivec = (np.arange(C['n_P'])+0.5)*inc2rad
    phi2vec = (np.arange(C['n_p2'])+0.5)*inc2rad

    phi1, phi, phi2 = np.meshgrid(phi1vec, phivec, phi2vec)

    phi1 = phi1.reshape(phi1.size)
    phi = phi.reshape(phi.size)
    phi2 = phi2.reshape(phi2.size)

    angles = np.zeros([C['n_tot'], 4], dtype='float64')

    for ii in xrange(C['n_th']):
        ii_stt = ii*C['n_eul']
        ii_end = ii_stt+C['n_eul']
        angles[ii_stt:ii_end, 0] = thetavec[ii]
        angles[ii_stt:ii_end, 1] = phi1
        angles[ii_stt:ii_end, 2] = phi
        angles[ii_stt:ii_end, 3] = phi2

    """Generate test Y"""

    bvec = np.random.randint(low=0, high=C['cmax'], size=(5))
    bvec[0] = 0
    bvec = np.unique(bvec)

    bval = np.random.randint(low=1, high=10, size=bvec.size)

    msg = "bvec: %s" % str(bvec)
    fn.WP(msg, filename)
    msg = "bval: %s" % str(bval)
    fn.WP(msg, filename)

    cmat = np.unravel_index(np.arange(C['cmax']), C['N_tuple'])
    cmat = np.array(cmat).T

    Y = np.zeros((C['n_tot']), dtype='complex128')

    for ii in xrange(bvec.size):
        p, q = cmat[bvec[ii], :]

        tmpgsh = gsh.gsh_eval(angles[:, 1:4], [p])
        tmpcos = np.cos(q*np.pi*angles[:, 0]/C['L_th'])

        Y += bval[ii]*np.squeeze(tmpgsh)*tmpcos

    alldata = np.zeros((C['n_tot'], 14), dtype='complex128')
    alldata[:, :4] = angles
    alldata[:, 4] = Y

    f1 = h5py.File(C['combineread_output'], 'w')
    f1.create_dataset("var_set", data=alldata)
    f1.close()


if __name__ == '__main__':
    gen()
