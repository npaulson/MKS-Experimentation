import numpy as np
import matplotlib.pyplot as plt
from constants import const
import h5py


def pltcheck(ns, set_id):

    C = const()

    """load the simulated and predicted responses"""
    f = h5py.File("responses.hdf5", 'r')
    r_sim = f.get('fip_%s' % set_id)[...]
    r_sim = r_sim.reshape((C['n_samp']))
    f.close()

    f = h5py.File('validation_%s.hdf5' % set_id, 'r')
    r_fit = f.get('r_fit')[...]
    f.close()

    r_sim = r_sim
    r_fit = r_fit

    """plot the prediction equal to simulation line"""
    plt.figure(num=6, figsize=[9, 8.5])

    minval = np.min([r_sim])
    maxval = np.max([r_sim])
    valrange = maxval-minval
    minval_ = minval - 0.5*valrange
    maxval_ = maxval + 0.5*valrange
    line = np.array([minval_, maxval_])

    plt.plot(line, line, 'k-')

    plt.plot(r_sim, r_fit,
             marker='o', markersize=3, color=[.7, .1, .1],
             linestyle='')

    minval_ = minval - 0.1*valrange
    maxval_ = maxval + 0.1*valrange
    plt.axis([minval_, maxval_, minval_, maxval_])

    plt.title("predicted versus simulated FIP")
    plt.xlabel("simulation")
    plt.ylabel("prediction")

    plt.xticks(rotation=20)
    plt.yticks(rotation=20)

    plt.show()


if __name__ == '__main__':

    C = const()

    ns = C['ns_val']
    set_id = C['set_id_val']
    pltcheck(ns, set_id)
