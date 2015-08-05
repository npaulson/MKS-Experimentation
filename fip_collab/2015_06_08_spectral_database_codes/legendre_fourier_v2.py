import numpy as np
import numpy.polynomial.legendre as leg
import matplotlib.pyplot as plt


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

N = 200  # number of points in DFT
Ip = 10  # order of legendre polynomial
xi = -1.0  # start x value
xf = 1.0  # end x value
L = xf-xi  # range

xsamp = np.linspace(xi, xf, N)[:-1]
print xsamp

c = np.zeros(Ip+1)
c[Ip] = 1

ysamp = leg.legval(xsamp, c)
ysampFFT = np.fft.fft(ysamp)

xplt = np.linspace(xi, xf, 1000)
yactual = leg.legval(xplt, c)
yinterp = np.real(triginterp(ysampFFT, xplt-xplt[0], L))

plt.plot(xplt, yactual, 'b')
plt.plot(xplt, yinterp, 'r')

plt.show()
