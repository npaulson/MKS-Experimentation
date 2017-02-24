import numpy as np
import matplotlib.pyplot as plt
import h5py


def pltmap(ns_max, set_id):

    plt.figure(num=1, figsize=[12, 4])

    f = h5py.File("responses.hdf5", 'r')
    coefs = f.get('gamma_coefs')[...]
    f.close()

    alpha = coefs[:, 0]  # alpha
    loc = coefs[:, 1]  # mu-sub-g
    scale = coefs[:, 2]  # sigma-sub-g
    r2 = coefs[:, 3]

    print np.arange(1, ns_max+1).shape
    print alpha.shape

    plt.subplot(141)

    plt.plot(np.arange(1, ns_max+1), np.log(loc), 'b-')
    plt.xlabel("number of SVEs", fontsize=13)
    plt.ylabel(r"$ln(\tilde{\mu})$", fontsize=20)
    plt.axis([1., ns_max, -14.5, -12.5])
    plt.grid(True)

    plt.subplot(142)

    plt.plot(np.arange(1, ns_max+1), np.log(scale), 'b-')
    plt.xlabel("number of SVEs", fontsize=13)
    plt.ylabel(r"$ln(\tilde{\sigma})$", fontsize=20)
    plt.axis([1., ns_max, -16, -13.5])
    plt.grid(True)

    plt.subplot(143)

    plt.plot(np.arange(1, ns_max+1), alpha, 'b-')
    plt.xlabel("number of SVEs", fontsize=13)
    plt.ylabel(r"$\alpha$", fontsize=20)
    plt.axis([1., ns_max, 0.6, 1.05])
    plt.grid(True)

    plt.subplot(144)

    plt.plot(np.arange(1, ns_max+1), r2, 'b-')
    plt.xlabel("number of SVEs", fontsize=13)
    plt.ylabel(r"$r^2$", fontsize=20)
    plt.axis([1., ns_max, 0.8, 1.05])
    plt.grid(True)

    plt.tight_layout()

if __name__ == '__main__':
    ns_max = 500
    set_id = "BaTrTr"
    pltmap(ns_max, set_id)
    plt.show()
