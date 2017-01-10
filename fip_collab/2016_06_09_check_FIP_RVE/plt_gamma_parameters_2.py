import numpy as np
import matplotlib.pyplot as plt
import h5py


def pltmap(ns_max, step):

    plt.figure(num=1, figsize=[7, 3])

    f = h5py.File("responses.hdf5", 'r')
    coefs = f.get('gamma_coefs')[...]
    f.close()

    loc = np.log(coefs[(step-2)::step, 1])  # mu-sub-g
    scale = np.log(coefs[(step-2)::step, 2])  # sigma-sub-g

    fipax = np.arange(step-1, ns_max+1, step)

    plt.subplot(121)

    plt.plot(fipax, loc, 'k.-')
    plt.xlabel("number of SVEs", fontsize='large')
    plt.ylabel("$ln(\mu_g)$", fontsize='large')
    plt.axis([1., 500., loc.mean()-.5, loc.mean()+.5])
    plt.grid(True)

    plt.subplot(122)

    plt.plot(fipax, scale, 'k.-')
    plt.xlabel("number of SVEs", fontsize='large')
    plt.ylabel("$ln(\sigma_g)$", fontsize='large')
    plt.axis([1., 500., scale.mean()-.5, scale.mean()+.5])
    plt.grid(True)

    plt.tight_layout()

if __name__ == '__main__':
    ns_max = 500
    step = 20
    pltmap(ns_max, step)
    plt.show()
