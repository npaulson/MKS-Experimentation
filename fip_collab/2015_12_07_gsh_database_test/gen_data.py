import numpy as np


def testfunc(x):
    # return -.75*np.cos(x)+.25*np.cos(4*x)
    return np.cos(0.5*x)**10


L = np.pi

N = 100  # number of samples
xsamp = np.linspace(0, L, N)  # x samples
ysamp = testfunc(xsamp)  # function value


