import numpy as np
import time


def triginterp(s_list, f_list, xi, L, N):

    Pvec = f_list * \
        np.exp((2*np.pi*1j*s_list[:, 0]*xi[:, 0:1])/L) * \
        np.exp((2*np.pi*1j*s_list[:, 1]*xi[:, 1:2])/L)

    print Pvec.shape

    return np.real(np.sum(Pvec, 1)/(N**2))


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
N = 6

xst = 0
xfn = 2*np.pi

# get the fft
f_d_fft = get_fft(xst, xfn)

sh = f_d_fft.shape
sz = f_d_fft.size

# center the fft s.t. the 0th frequency is centered
f_d_fft = np.fft.fftshift(f_d_fft).reshape(sz)

# find half of the range for each dimension in the fft
kmax = np.int8(np.floor(np.array(sh)/2.))
kmax = np.expand_dims(kmax, 1)

# generate indices associated with the fft
INDX = np.unravel_index(np.arange(sz), sh)
# array containing indices associated with the fft
INDX = np.transpose(np.array(INDX) - kmax)

print INDX

maxf = np.max(np.abs(f_d_fft))  # amplitude of frequency with max amplitude

# find the indices of fft frequencies with magnitudes greater than .25% of
# the largest value of the fft
gt_p25 = np.abs(f_d_fft) > 0.0025 * maxf

s_list = INDX[gt_p25, :]
f_list = f_d_fft[gt_p25]

print s_list.shape
print f_list.shape

# point to interpolate:
pt = np.array([[1.4, 3.9], [0.1, 5.1], [0.5, 1.8]])

# evaluate the function
f_eval = f(pt[:, 0], pt[:, 1])

st = time.time()

L = xfn-xst
f_trig = triginterp(s_list, f_list, pt, L, N)

print (time.time() - st)
print f_eval, f_trig
