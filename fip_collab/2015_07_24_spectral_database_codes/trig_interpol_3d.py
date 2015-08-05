import numpy as np


def triginterp(ar_fft, xi, L):
    # calculate the trigonometric interpolation at the locations in lvec
    P = ar_fft[0, 0, 0]

    N = ar_fft.shape[0]

    kmax = int(np.ceil(N/2.0))+1

    print kmax

    for l in xrange(1, kmax):

        print [l, N-l]

        for m in xrange(1, kmax):
            for n in xrange(1, kmax):

                tmp1 = ar_fft[l, m, n] * \
                    np.exp((2*np.pi*1j*l*xi[0])/L) * \
                    np.exp((2*np.pi*1j*m*xi[1])/L) * \
                    np.exp((2*np.pi*1j*n*xi[2])/L)
                tmp2 = ar_fft[N-l, N-m, N-n] * \
                    np.exp((-2*np.pi*1j*l*xi[0])/L) * \
                    np.exp((-2*np.pi*1j*m*xi[1])/L) * \
                    np.exp((-2*np.pi*1j*n*xi[2])/L)

                P += tmp1 + tmp2

    return P/(N**3)


# sample times for the function
Nd = 100
N = Nd-1
x_d = np.linspace(0, 2*np.pi, Nd)
L = np.max(x_d)-np.min(x_d)


def f(x1, x2, x3):

    val = -0.85*np.sin(x1+0.542) + \
          0.15*np.cos(2.0*x1) + \
          0.5*np.sin(x2) + \
          0.23*np.cos(x3-0.442)

    return val

[X1d, X2d, X3d] = np.meshgrid(x_d, x_d, x_d)

Zd = f(X1d, X2d, X3d)

# take the fft
f_d_fft = np.fft.fftn(Zd[:-1, :-1, :-1])

# point to interpolate:
pt = np.array([0.8, 6.1, 2.2])

# evaluate the function
f_eval = f(pt[0], pt[1], pt[2])

f_trig = triginterp(f_d_fft, pt, L)

print f_eval, f_trig
