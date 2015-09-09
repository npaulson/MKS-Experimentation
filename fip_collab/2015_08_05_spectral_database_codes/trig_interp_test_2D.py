import numpy as np
import time
import itertools as it


def triginterp(ar_fft, xi, L):
    # calculate the trigonometric interpolation at the locations in lvec

    N = ar_fft.shape[0]

    kmax = int(np.floor(N/2.))

    # get sequence of indices for l and m
    tmp = np.arange(-kmax, kmax+1)

    # get all unique permutations for set of 2 indices
    indvec = np.array(list(it.product(tmp, repeat=2)))

    # find indices less than 0, sum along rows
    tmp = np.sum(np.int8(indvec < 0), 1)

    # identify even numbers
    conjind = tmp % 2

    reguind = 1 - conjind

    tmp = ar_fft[np.abs(indvec[:, 0]), np.abs(indvec[:, 1])]

    freqvec = reguind*tmp + np.conj(conjind*tmp)

    Pvec = freqvec * \
        np.exp((2*np.pi*1j*indvec[:, 0]*xi[0])/L) * \
        np.exp((2*np.pi*1j*indvec[:, 1]*xi[1])/L)

    return np.sum(Pvec)/(N**2)


def triginterp_old(ar_fft, xi, L):
    # calculate the trigonometric interpolation at the locations in lvec
    P = 0

    N = ar_fft.shape[0]

    kmax = int(np.floor(N/2.))

    for l in xrange(-kmax, kmax+1):
        for m in xrange(-kmax, kmax+1):

            freqval = ar_fft[np.abs(l), np.abs(m)]

            if l < 0:
                freqval = np.conj(freqval)
            if m < 0:
                freqval = np.conj(freqval)

            P += freqval * \
                np.exp((2*np.pi*1j*l*xi[0])/L) * \
                np.exp((2*np.pi*1j*m*xi[1])/L)

    return P/(N**2)


def f(x1, x2):

    val = -0.85*np.sin(x1+0.542) + \
          0.15*np.cos(2.0*x1) + \
          0.5*np.sin(x2)

    return val


# sample times for the function
N = 99
xst = 0
xfn = 2*np.pi
L = xfn-xst
x_d = np.linspace(xst, xfn, N+1)[:-1]

[X1d, X2d] = np.meshgrid(x_d, x_d)

Zd = f(X2d, X1d)

# take the fft
f_d_fft = np.fft.fftn(Zd)

# point to interpolate:
pt = np.array([2.4, 3.9])

# evaluate the function
f_eval = f(pt[0], pt[1])

st = time.time()

f_trig = triginterp(f_d_fft, pt, L)

print (time.time() - st)

print f_eval, f_trig
