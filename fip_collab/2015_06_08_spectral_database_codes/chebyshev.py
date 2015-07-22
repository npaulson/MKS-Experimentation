import numpy as np


def chebyshev_nodes(a, b, n):
    kk = np.arange(1, n+1)
    xk = 0.5*(a+b)+0.5*(b-a)*np.cos(((2*kk - 1)*np.pi)/(2*n))

    return xk
