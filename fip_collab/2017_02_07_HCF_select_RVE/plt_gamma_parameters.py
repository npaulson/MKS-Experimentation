import numpy as np
import matplotlib.pyplot as plt
import h5py


def pltmap(ns_max, set_id):

    plt.figure(num=1, figsize=[10, 4])

    f = h5py.File("responses.hdf5", 'r')
    coefs = f.get('gamma_coefs')[...]
    f.close()

    alpha = coefs[:, 0]  # alpha
    loc = coefs[:, 1]  # mu-sub-g
    scale = coefs[:, 2]  # sigma-sub-g
    r2 = coefs[:, 3]

    plt.subplot(131)

    plt.plot(np.arange(1, ns_max+1), np.log(loc), 'b-')
    plt.xlabel("number of SVEs", fontsize=13)
    plt.ylabel(r"$ln(\tilde{\mu})$", fontsize=20)
    plt.axis([1., ns_max, -6.2, -4.4])
    plt.grid(True)

    plt.subplot(132)

    plt.plot(np.arange(1, ns_max+1), np.log(scale), 'b-')
    plt.xlabel("number of SVEs", fontsize=13)
    plt.ylabel(r"$ln(\tilde{\sigma})$", fontsize=20)
    plt.axis([1., ns_max, -8.0, -6.0])
    plt.grid(True)

    plt.subplot(133)

    plt.plot(np.arange(1, ns_max+1), r2, 'b-')
    plt.xlabel("number of SVEs", fontsize=13)
    plt.ylabel(r"$r^2$", fontsize=20)
    plt.axis([1., ns_max, 0.9, 1.00])
    plt.grid(True)

    plt.tight_layout()

if __name__ == '__main__':
    ns_max = 495
    set_id = "BaTrTr_cal"
    pltmap(ns_max, set_id)
    plt.show()
