import numpy as np
import time
import itertools as it


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

xst = 0
xfn = 2*np.pi

kmax = int(np.floor(N/2.))

f_d_fft = get_fft(xst, xfn)

# print np.abs(f_d_fft)

# maxf = np.max(np.abs(f_d_fft.reshape(N**2)))

# print maxf

# # find the indices of fft frequencies with magnitudes greater than .25% of
# # the largest value of the fft
# gt_p25 = np.abs(f_d_fft) > 0.0025 * maxf

# print gt_p25

# xvec = np.arange(N)

# X1, X2 = np.meshgrid(xvec, xvec)

# s_list = np.transpose(np.vstack([X1[gt_p25], X2[gt_p25]])) - kmax
# f_list = f_d_fft[gt_p25]

# print s_list[:, 0]
# print s_list[:, 1]
# print f_list


l1 = np.unravel_index(np.arange(N*N), [N, N])
s_list = np.transpose(np.vstack([l1[0], l1[1]])) - kmax
# s_list = np.transpose(np.vstack([X2.reshape(N*N), X1.reshape(N*N)])) - kmax
f_list = f_d_fft[s_list[:, 0], s_list[:, 1]]

print s_list
print f_list

# point to interpolate:
pt = np.array([1.4, 3.9])

# evaluate the function
f_eval = f(pt[0], pt[1])

st = time.time()

L = xfn-xst
f_trig = triginterp(s_list, f_list, pt, L, N)

print (time.time() - st)

print f_eval, f_trig
