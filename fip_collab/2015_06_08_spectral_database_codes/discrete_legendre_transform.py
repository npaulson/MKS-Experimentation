import numpy as np
import scipy.integrate as quad

def DLT_coeff(func, a, b, N):

    coeff_set = np.zeros(N+1)

    for kk in xrange(0, N+1):

        tmp = 0

        for ii in xrange(0, N+1):

            tmp += quad.fixed_quad(funcS,)

    coeff_set[kk] = 0.5*(2*kk)*tmp

    return coeff_set


def DLT_interpolate():