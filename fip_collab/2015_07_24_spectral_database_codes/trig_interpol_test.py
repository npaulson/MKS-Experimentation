import numpy as np


def triginterp(ar_fft, xi, L):
    # calculate the trigonometric interpolation at the locations in xi

    P = 0
    N = ar_fft.shape[0]

    print N

    # kmax = int((N-1)/2.0)
    kmax = int(np.floor(N/2.))

    print kmax

    for l in xrange(-kmax, kmax+1):

        P += ar_fft[l] * \
          np.exp((2*np.pi*1j*(l)*xi[0])/L)

    return P/N


# def triginterp(ar_fft, xi, L):
#     # calculate the trigonometric interpolation at the locations in lvec
#     P = ar_fft[0]

#     N = len(ar_fft)

#     kmax = int(np.ceil(N/2.0))

#     for k in xrange(1, kmax):
#         print [k, N-k]
#         tmp1 = ar_fft[k]*np.exp((2*np.pi*1j*k*xi)/L)
#         tmp2 = ar_fft[N-k]*np.exp((-2*np.pi*1j*k*xi)/L)
#         P += tmp1 + tmp2

#     return P/N


# sample times for the function
Nd = 10
N = Nd-1
x_d = np.linspace(0, 2*np.pi, Nd)
L = np.max(x_d)-np.min(x_d)


def f(x1):

    val = -0.85*np.sin(x1+0.542) + \
          0.15*np.cos(2*x1)

    return val

[X1d] = np.meshgrid(x_d)

Zd = f(X1d)

# take the fft
f_d_fft = np.fft.fftn(Zd[:-1])

print f_d_fft

# point to interpolate:
pt = np.array([0.8])

# evaluate the function
f_eval = f(pt[0])

f_trig = triginterp(f_d_fft, pt, L)

print f_eval, f_trig
