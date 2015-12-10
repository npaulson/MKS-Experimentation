import numpy as np


def et_back(x):

    et_ii = np.array([np.sqrt(2./3.)*np.cos(x-(np.pi/3.)),
                      np.sqrt(2./3.)*np.cos(x+(np.pi/3.)),
                      -np.sqrt(2./3.)*np.cos(x)])

    return et_ii

if __name__ == "__main__":

    theta = np.random.rand()*(np.pi/3)
    et_ii = et_back(theta)
    print theta*(180/np.pi)
    print et_ii
