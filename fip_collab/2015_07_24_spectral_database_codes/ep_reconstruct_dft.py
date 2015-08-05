import numpy as np
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


# load raw data
et_norm = np.load('et_norm.npy')
# et = np.load('et.npy')
ep = np.load('ep.npy')
# sig = np.load('sig.npy')
# I1 = np.load('I1.npy')
# I2 = np.load('I2.npy')
# I3 = np.load('I3.npy')

# plot functions of interest
plt.figure(num=1, figsize=[10, 6])

# specify the range of the dependent variable of interest
yvar = ep[:, 0]

# the following vector closely matches that of et_norm
xvec = np.linspace(.0001, .0100, 100)
# find the maximum percent deviation between etvec and et_norm
et_err = 100*np.mean(np.abs((xvec-et_norm)/xvec))

msg = "maximum %% devation in et_norm scales: %s%%" % et_err
print msg

# plot the original dependent variable data versus the normalized total strain
# quantity
plt.plot(xvec[59:96], yvar[59:96], 'bx')

# prepare mirrored versions of the x, y axis data vectors

# step is sampling interval for the dependent variable
step = 4

# mp is a point that is inserted between the original samples
# and the mirrored samples to smooth out the representation
mp = yvar[96-1] + step*(yvar[96-1]-yvar[96-2])

# rvec_ is the modified vector of samples including the mirrored and interted
# points
rvec_ = np.hstack([yvar[59:96:step], mp, mp, np.flipud(yvar[59:96:step])])[:-1]
N = len(rvec_)
print N
# etvecS is the starting normalized total strain
etvecS = .0060
# etvecE is the terminal normalized total strain
etvecE = etvecS + N*step*0.0001
print etvecE
# etvec_ is the vector of normalized total strains associated with rvec_
etvec_ = np.linspace(etvecS, etvecE, N+1)[:-1]
# ep_ = np.hstack([ep[59:,0],ep[-1,0],np.flipud(ep[59:,0])])

plt.plot(etvec_, rvec_, 'bo')

Yk = np.fft.fft(rvec_)

# xi is the vector of total strains to be used as interpolation points with the
# spectral interpolation. Note that the strains are shifted so that the first
# is zero

# xi = np.linspace(etvecS, etvecE, 1000) - etvecS
xi = np.linspace(.0064, .0094, 1000) - etvecS

# L is the range of normalized total strain
L = etvecE - etvecS

# P is the vector of interpolated values associated with the vector xi
P = triginterp(Yk, xi, L)

plt.plot(xi+etvecS, np.real(P), 'r')
plt.xlabel("$|\epsilon^t|$")
plt.ylabel("$\epsilon_{11}^p$")
plt.title("$|\epsilon^t|$ vs. $\epsilon_{11}^p$ with Trigonometric Interpolation")

# calculate error in this approach based on sampled values
y4err_actual = yvar[63:96]
# x4err = np.linspace(.0064, .0096, len(y4err_actual)) - etvecS
x4err = et_norm[63:96] - etvecS
y4err_spline = triginterp(Yk, x4err, L)
error = 100*np.abs((y4err_spline - y4err_actual)/yvar[95])
print error
print 'mean error: %s%%' % np.mean(error)
print 'max error: %s%%' % np.max(error)

plt.show()
