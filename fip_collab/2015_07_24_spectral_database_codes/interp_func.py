import numpy as np


def triginterp(Yk, xi, L):
    # calculate the trigonometric interpolation at the locations in lvec
    P = Yk[0]

    N = len(Yk)

    if N % 2 == 0:
        print 'even'
        P += Yk[N/2]*np.cos((np.pi*N*xi)/L)
        kmax = int(N/2.0)
    else:
        kmax = int(np.ceil(N/2.0))

    for k in xrange(1, kmax):
        print [k, N-k]
        tmp1 = Yk[k]*np.exp((2*np.pi*1j*k*xi)/L)
        tmp2 = Yk[N-k]*np.exp((-2*np.pi*1j*k*xi)/L)
        P += tmp1 + tmp2

    return P/N
