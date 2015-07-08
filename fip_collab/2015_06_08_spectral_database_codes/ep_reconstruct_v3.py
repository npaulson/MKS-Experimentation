import numpy as np
import matplotlib.pyplot as plt


def triginterp(Yk,xi,L):
	# calculate the trigonometric interpolation at the locations in lvec
	P = Yk[0]

	N = len(Yk)

	if N%2 ==0:
	    print 'even'
	    P += Yk[N/2]*np.cos((np.pi*N*xi)/L)
	    kmax = int(N/2.0)
	else:
		kmax = int(np.ceil(N/2.0))

	for k in xrange(1,kmax):
	    print [k, N-k]
	    tmp1 = Yk[k]*np.exp((2*np.pi*1j*k*xi)/L)
	    tmp2 = Yk[N-k]*np.exp((-2*np.pi*1j*k*xi)/L)
	    P += tmp1 + tmp2

	return P/N


# load raw data
et_norm = np.load('et_norm.npy')
et = np.load('et.npy')
ep = np.load('ep.npy')
sig = np.load('sig.npy')
I1 = np.load('I1.npy')
I2 = np.load('I2.npy')
I3 = np.load('I3.npy')

# plot functions of interest
plt.figure(num=1, figsize=[7, 5])

# specify the range of the dependent variable of interest
# rvec = ep[59:,2]
rvec = I3[59:]

# the following vector closely matches that of et_norm
etvec = np.linspace(.006,.01,41)

# find the maximum percent deviation between etvec and et_norm  
et_err = 100*np.mean(np.abs((etvec-et_norm[59:])/etvec))
et_err = et_err

msg = "maximum %% devation in et_norm scales: %s%%" %et_err
print msg

plt.figure(num=1, figsize=[7,5])
# plot the original dependent variable data versus the normalized total strain quantity
plt.plot(etvec,rvec)

# prepare mirrored versions of the x, y axis data vectors

# step is sampling interval for the dependent variable
step = 2

# mp is a point that is inserted between the original samples
# and the mirrored samples to smooth out the representation
mp = rvec[-1] + step*(rvec[-1]-rvec[-2])

# rvec_ is the modified vector of samples including the mirrored and interted points
rvec_ = np.hstack([rvec[0::step],mp,mp,np.flipud(rvec[0::step])])[:-1]
N = len(rvec_)
print N
# etvecS is the starting normalized total strain
etvecS = .0060
# etvecE is the terminal normalized total strain
etvecE = etvecS + N*step*0.0001
print etvecE
# etvec_ is the vector of normalized total strains associated with rvec_
etvec_ = np.linspace(etvecS,etvecE,N+1)[:-1]
# ep_ = np.hstack([ep[59:,0],ep[-1,0],np.flipud(ep[59:,0])])

plt.plot(etvec_,rvec_,'ro')

Yk = np.fft.fft(rvec_)

# xi is the vector of total strains to be used as interpolation points with the
# spectral interpolation. Note that the strains are shifted so that the first is zero
xi = np.linspace(etvecS,etvecE,1000) - etvecS
# L is the range of normalized total strain
L = etvecE - etvecS
# P is the vector of interpolated values associated with the vector xi
P = triginterp(Yk,xi,L)

plt.plot(xi+etvecS,np.real(P),'m')
plt.show()