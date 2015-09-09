import numpy as np
import time


def triginterp(s_list, f_list, xi, L, N):

    Pvec = f_list * \
        np.exp((2*np.pi*1j*s_list[:, 0]*xi[0])/L) * \
        np.exp((2*np.pi*1j*s_list[:, 1]*xi[1])/L)

    return np.sum(Pvec)/(N**2)


def f(x1, x2):

    val = -0.85*np.sin(x1+0.542) + \
          0.15*np.cos(2.0*x1) + \
          0.5*np.sin(x2)

    return val


def get_fft(xst, xfn):

    x_d = np.linspace(xst, xfn, N+1)[:-1]

    [X1d, X2d] = np.meshgrid(x_d, x_d)

    Zd = f(X2d, X1d)

    # take the fft
    f_d_fft = np.fft.fftn(Zd)

    return f_d_fft


# sample times for the function
N = 5

kmax = int(np.floor(N/2.))

xst = 0
xfn = 2*np.pi

f_d_fft = get_fft(xst, xfn)

print f_d_fft

# point to interpolate:
pt = np.array([1.4, 3.9])

# evaluate the function
f_eval = f(pt[0], pt[1])

st = time.time()

L = xfn-xst

Pvec = 0

for k in xrange(N):
    for l in xrange(N):

        print k-kmax, l-kmax

        Pvec += f_d_fft[k-kmax, l-kmax] * \
            np.exp((2*np.pi*1j*(k-kmax)*pt[0])/L) * \
            np.exp((2*np.pi*1j*(l-kmax)*pt[1])/L)

f_trig = Pvec/(N**2)

print (time.time() - st)

print f_eval, f_trig
