import numpy as np


def triginterp(ar_fft, xi, L):
    # calculate the trigonometric interpolation at the locations in lvec
    P = 0

    N = ar_fft.shape[0]

    # kmax = int((N-1)/2.0)
    kmax = int(np.floor(N/2.))

    print kmax

    for l in xrange(-kmax, kmax+1):
        for m in xrange(-kmax, kmax+1):
            for n in xrange(-kmax, kmax+1):

                freqval = ar_fft[np.abs(l), np.abs(m), np.abs(n)]

                if l < 0:
                    freqval = np.conj(freqval)
                if m < 0:
                    freqval = np.conj(freqval)
                if n < 0:
                    freqval = np.conj(freqval)

                P += freqval * \
                    np.exp((2*np.pi*1j*l*xi[0])/L) * \
                    np.exp((2*np.pi*1j*m*xi[1])/L) * \
                    np.exp((2*np.pi*1j*n*xi[2])/L)

    return P/(N**3)


def f(x1, x2, x3):

    val = -0.85*np.sin(x1+0.542) + \
          0.15*np.cos(2.0*x1) + \
          0.5*np.sin(x2) + \
          0.23*np.cos(x3-0.442)

    return val


# sample times for the function
N = 9
xst = 0
xfn = 2*np.pi
L = xfn-xst
x_d = np.linspace(xst, xfn, N+1)[:-1]

[X1d, X2d, X3d] = np.meshgrid(x_d, x_d, x_d)

Zd = f(X2d, X1d, X3d)

# take the fft
f_d_fft = np.fft.fftn(Zd)

# point to interpolate:
pt = np.array([0.8, 6.1, 2.2])

# evaluate the function
f_eval = f(pt[0], pt[1], pt[2])

f_trig = triginterp(f_d_fft, pt, L)

print f_eval, f_trig
