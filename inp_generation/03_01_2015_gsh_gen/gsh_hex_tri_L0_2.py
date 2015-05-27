import numpy as np


def gsh(e_angles):

    phi1 = e_angles[0, :]
    phi = e_angles[1, :]
    phi2 = e_angles[2, :]

    zvec = np.abs(phi) < 10e-17
    zvec = zvec.astype(int)
    randvec = np.round(np.random.rand(zvec.shape[0]))
    randvecopp = np.ones(zvec.shape[0]) - randvec
    phi += (1e-7)*zvec*(randvec - randvecopp)

    out_tvalues = np.zeros([6, e_angles.shape[1]], dtype = 'complex128')

    out_tvalues[0, :] = 1

    return out_tvalues

if __name__ == '__main__':
    tvals = gsh(np.array([[.1], [.2], [.3]]))
    print tvals

