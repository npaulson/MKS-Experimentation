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

    t4 = np.sin(phi)
    t6 = np.sqrt(0.6e1)
    t8 = -t4 ** 2 * t6 / 0.4e1
    t5 = np.cos(phi)
    t7 = (-0.1e1 / 0.2e1*1j) * np.sqrt((1 + t5)) * np.sqrt((1 - t5)) * t5 * t6
    out_tvalues[0, :] = 1
    out_tvalues[1, :] = np.exp((-2*1j) * phi1) * t8
    out_tvalues[2, :] = np.exp((-1*1j) * phi1) * t7
    out_tvalues[3, :] = 0.3e1 / 0.2e1 * t5 ** 2 - 0.1e1 / 0.2e1
    out_tvalues[4, :] = np.exp((1j) * phi1) * t7
    out_tvalues[5, :] = np.exp((2*1j) * phi1) * t8

    return out_tvalues

if __name__ == '__main__':
    tvals = gsh(np.array([[.1], [.2], [.3]]))
    print tvals

