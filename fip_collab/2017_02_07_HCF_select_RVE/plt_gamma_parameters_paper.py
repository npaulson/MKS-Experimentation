import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import h5py


def pltmap(ns_max, set_id):

    plt.figure(num=1, figsize=[8, 2.5])

    f = h5py.File("responses.hdf5", 'r')
    coefs = f.get('gamma_coefs')[...]
    f.close()

    alpha = coefs[:, 0]  # alpha
    loc = coefs[:, 1]  # mu-sub-g
    scale = coefs[:, 2]  # sigma-sub-g
    r2 = coefs[:, 3]

    c = cm.rainbow(np.linspace(0, .3, 3))[2]

    print np.arange(1, ns_max+1).shape
    print alpha.shape

    plt.subplot(131)

    plt.plot(np.arange(1, ns_max+1), np.log(loc), color=c,
             linestyle='-', marker='')
    plt.xlabel("number of SVEs", fontsize=13)
    plt.ylabel(r"$ln\left(\mu\right)$", fontsize=20)
    plt.axis([1., ns_max, -16.5, -13])
    plt.xticks(fontsize=12.5, rotation='90')
    plt.yticks(fontsize=12.5)
    plt.grid(True)

    plt.subplot(132)

    plt.plot(np.arange(1, ns_max+1), np.log(scale), color=c,
             linestyle='-', marker='')
    plt.xlabel("number of SVEs", fontsize=13)
    plt.ylabel(r"$ln\left(\sigma\right)$", fontsize=20)
    plt.axis([1., ns_max, -15.5, -14])
    plt.xticks(fontsize=12.5, rotation='90')
    plt.yticks(fontsize=12.5)
    plt.grid(True)

    plt.subplot(133)

    plt.plot(np.arange(1, ns_max+1), alpha, color=c,
             linestyle='-', marker='')
    plt.xlabel("number of SVEs", fontsize=13)
    plt.ylabel(r"$\alpha$", fontsize=20)
    plt.axis([1., ns_max, 0.6, 1.05])
    plt.xticks(fontsize=12.5, rotation='90')
    plt.yticks(fontsize=12.5)
    plt.grid(True)

    plt.tight_layout(w_pad=0.2)

if __name__ == '__main__':
    ns_max = 500
    set_id = "BaTrTr"
    pltmap(ns_max, set_id)
    plt.show()
