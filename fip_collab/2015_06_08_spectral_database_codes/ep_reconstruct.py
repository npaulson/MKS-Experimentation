import numpy as np
import matplotlib.pyplot as plt

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

plt.subplot(2, 1, 1)
plt.plot(et_norm[59:],ep[59:,0],'b')

plt.subplot(2, 1, 2)
plt.plot(et_norm[59:],I2[59:])


# create regularly spaced data for database
etvec = np.linspace(.006,.01,41)

# find the maximum percent deviation between etvec and et_norm  
et_err = 100*np.mean(np.abs((etvec-et_norm[59:])/etvec))
et_err = et_err

msg = "maximum %% devation in et_norm scales: %s%%" %et_err
print msg

etvecS = .0060
etvecE = .0141
N = 82
etvec_ = np.linspace(etvecS,etvecE,N+1)
tmp = ep[-1,0]
ep_ = np.hstack([ep[59:,0],ep[-1,0],np.flipud(ep[59:,0])]);

plt.figure(num=2, figsize=[7,5])

plt.plot(etvec_,ep_)

Yk = np.fft.fft(ep_[:-1])

L = etvecE - etvecS
xi = etvec_[:-1] - etvecS

# calculate the trigonometric interpolation at the locations in lvec
P = Yk[0]
for k in xrange(1,int(np.floor(N/2))):
    print [k, N-k]
    tmp1 = Yk[k]*np.exp((2*np.pi*1j*k*xi)/L)
    tmp2 = Yk[N-k]*np.exp((-2*np.pi*1j*k*xi)/L)
    P += tmp1 + tmp2
    
if N%2 ==0:
    print 'even'
    P += Yk[N/2]*np.cos((np.pi*N*xi)/L)
# end

P = P/N

plt.figure(num=2, figsize=[7, 5])

plt.plot(xi+etvecS,np.real(P),'r')

plt.show()