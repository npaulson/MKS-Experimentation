import numpy as np
import matplotlib.pyplot as plt
import h5py


def pltmap(ns_max, step):

    plt.figure(num=1, figsize=[10, 8])

    f = h5py.File("responses.hdf5", 'r')
    coefs = f.get('gamma_coefs')[...]
    f.close()

    shape = coefs[(step-2)::step, 0]  # alpha
    loc = coefs[(step-2)::step, 1]  # mu-sub-g
    scale = coefs[(step-2)::step, 2]  # sigma-sub-g
    r2 = coefs[(step-2)::step, 3]

    fipax = np.arange(step-1, ns_max+1, step)

    plt.subplot(411)

    plt.plot(fipax, shape, 'k.-')
    plt.xlabel("number of SVEs")
    plt.ylabel("$\\alpha$")
    plt.axis([1., 500., .6, 1.0])
    plt.grid(True)

    plt.subplot(412)

    plt.plot(fipax, np.log(loc), 'k.-')
    plt.xlabel("number of SVEs")
    plt.ylabel("$ln(\mu_g)$")
    plt.axis([1., 500., -15, -14])
    plt.grid(True)

    plt.subplot(413)

    plt.plot(fipax, np.log(scale), 'k.-')
    plt.xlabel("number of SVEs")
    plt.ylabel("$ln(\sigma_g)$")
    plt.axis([1., 500., -15, -14])
    plt.grid(True)

    plt.subplot(414)

    plt.plot(fipax, r2, 'k.-')
    plt.xlabel("number of SVEs")
    plt.ylabel("$r^2$")
    # plt.axis([1., 500., .985, 1.00])
    plt.grid(True)

    plt.tight_layout()

if __name__ == '__main__':
    ns_max = 500
    step = 20
    pltmap(ns_max, step)
    plt.show()
