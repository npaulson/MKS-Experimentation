import numpy as np
import matplotlib.pyplot as plt
import h5py


def pltmap(ns_max, set_id):

    plt.figure(num=1, figsize=[10, 8])

    f = h5py.File("responses.hdf5", 'r')
    coefs = f.get('gamma_coefs')[...]
    f.close()

    shape = coefs[:, 0]  # alpha
    loc = coefs[:, 1]  # mu-sub-g
    scale = coefs[:, 2]  # sigma-sub-g
    r2 = coefs[:, 3]

    plt.subplot(411)

    plt.plot(np.arange(1, ns_max+1), shape, 'b-')
    plt.xlabel("number of SVEs")
    plt.ylabel("$\\alpha$")
    plt.axis([1., 500., .6, 1.0])

    plt.subplot(412)

    plt.plot(np.arange(1, ns_max+1), loc, 'b-')
    plt.xlabel("number of SVEs")
    plt.ylabel("$\mu_g$")
    # plt.axis([1., 500., 3.5e-7, 5.5e-7])
    plt.axis([1., 500., 2.5e-7, 4.5e-7])

    plt.subplot(413)

    plt.plot(np.arange(1, ns_max+1), scale, 'b-')
    plt.xlabel("number of SVEs")
    plt.ylabel("$\sigma_g$")
    # plt.axis([1., 500., 2.5e-7, 4.5e-7])
    plt.axis([1., 500., 1.5e-7, 3.5e-7])

    plt.subplot(414)

    plt.plot(np.arange(1, ns_max+1), r2, 'b-')
    plt.xlabel("number of SVEs")
    plt.ylabel("$r^2$")
    plt.axis([1., 500., .985, 1.00])
    plt

if __name__ == '__main__':
    ns_max = 500
    set_id = "random_cal"
    pltmap(ns_max, set_id)
    plt.show()
