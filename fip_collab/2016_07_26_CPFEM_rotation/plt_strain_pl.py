import numpy as np
import matplotlib.pyplot as plt
import sys


def tensnorm(tensvec):
    return np.sqrt(np.sum(tensvec[:, 0:3]**2+2*tensvec[:, 3:]**2, 1))


if __name__ == '__main__':

    inc = np.int16(sys.argv[1])

    el = 21
    slc = 7

    filename = "Results_Ti64_Dream3D_ZdirLoad_210microns_9261el_AbqInp" +\
               "_PowerLaw_100inc_rotate_3_data_strain_pl_inc%s.txt" % str(inc)
    tmp = np.loadtxt(filename, skiprows=2)
    indx = np.argsort(tmp[:, 12])
    ep_raw = tmp[indx, 10]

    ep_raw = (ep_raw[0::8]+ep_raw[1::8]+ep_raw[2::8] +
              ep_raw[3::8]+ep_raw[4::8]+ep_raw[5::8] +
              ep_raw[6::8]+ep_raw[7::8])/8.

    en_pl = ep_raw.reshape((el, el, el))[slc, :, :]

    plt.figure(num=1, figsize=[4, 2.7])

    plt.imshow(en_pl, origin='lower',
               interpolation='none', cmap='plasma')
    plt.title("$\\vert\epsilon_{pl}\\vert$, step %s" % inc)
    plt.colorbar()

    plt.show()
