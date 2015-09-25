import numpy as np
import h5py
import leg_interp_func as lif


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

                freqval = ar_fft[np.abs(k), np.abs(l), np.abs(m), np.abs(n)]

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

# initialize important variables:
a = .0064  # start of range for legendre interpolation
b = .0096  # end of range for legendre interpolation

# tst_indx are the input values for the database interpolation with the
# following order: [theta, phi1, Phi, phi2, norm(et)]
# each row is for a single interpolation point
tst_indx = np.array([[.1, .2, .3, .4, .0070],
                     [.2, .4, .6, .8, .0075]])




yplt = lif.get_interp(et_val, coeff_set, a, b)