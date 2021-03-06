import numpy as np
import time
import itertools as it


def triginterp(s_list, f_list, xi, L, N):

    # find indices less than 0, sum along rows
    tmp = np.sum(np.int8(s_list < 0), 1)

    # identify even numbers
    conjind = tmp % 2

    reguind = 1 - conjind

    f_list_f = reguind*f_list + np.conj(conjind*f_list)

    Pvec = f_list_f * \
        np.exp((2*np.pi*1j*s_list[:, 0]*xi[0])/L) * \
        np.exp((2*np.pi*1j*s_list[:, 1]*xi[1])/L)

    return np.sum(Pvec)/(N**2)


def get_indices(s_list, f_list, N):

    kmax = int(np.floor(N/2.))

    # get array of possible combinations of negative and positive subscripts
    tmp = np.vstack([s_list, s_list*np.array([-1., -1.])])
    tmp = np.vstack([tmp, s_list*np.array([1., -1.])])
    b_s_list = np.vstack([tmp, s_list*np.array([-1., 1.])])

    b_s_list = b_s_list + kmax

    b_f_list = np.hstack([f_list, f_list, f_list, f_list])

    # get index associated with tuple of subscripts
    b_i_list = np.ravel_multi_index([np.int64(b_s_list[:, 0]),
                                     np.int64(b_s_list[:, 1])],
                                    [N+1, N+1])

    # get the unique indices
    s_i_list, s_i_list_i = np.unique(b_i_list, return_index=True)

    # get back the unique subscripts
    tmp1, tmp2 = np.unravel_index(s_i_list, (N+1, N+1))

    s_s_list = np.vstack([tmp1, tmp2]).T - kmax

    s_f_list = b_f_list[s_i_list_i]

    return s_s_list, s_f_list


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

    return f_d_fft, X1d, X2d


# sample times for the function
N = 4

xst = 0
xfn = 2*np.pi

kmax = int(np.floor(N/2.))

f_d_fft, X1d, X2d = get_fft(xst, xfn)

fft_lin = f_d_fft.reshape(N*N)
X1d_lin = X1d.reshape(N*N)
X2d_lin = X2d.reshape(N*N)

sindx = np.argsort(np.abs(fft_lin))  # order the fft by smallest to largest
sindx = np.flipud(sindx)  # flip order

fft_lin = fft_lin[sindx]  # reorder the fft by magnitude

# find the values of the fft with magnitudes greater than .25% of
# the largest value of the fft
gt_p25 = np.abs(fft_lin) > 0.0025 * np.abs(fft_lin[0])
fft_ext = np.sum(gt_p25) # extent of the relevant ffts

print fft_lin
print gt_p25
print fft_ext






# # get sequence of indices for l and m
# tmp = np.arange(0, kmax+1)

# # get all unique permutations for set of 2 indices
# s_list = np.array(list(it.product(tmp, repeat=2)))

# f_d_fft = get_fft(xst, xfn)
# f_list = f_d_fft[s_list[:, 0], s_list[:, 1]]

# # find indices to sort f_list from largest to smallest frequencies
# sindx = np.argsort(np.abs(f_list))
# sindx = np.flipud(sindx)

# # sort s_list and f_list
# s_list = s_list[sindx, :]
# f_list = f_list[sindx]

# # discard low amplitude frequencies and generate the final lists
# s_s_list, s_f_list = get_indices(s_list[:5, :], f_list[:5], N)




# # point to interpolate:
# pt = np.array([1.4, 3.9])

# # evaluate the function
# f_eval = f(pt[0], pt[1])

# st = time.time()

# L = xfn-xst
# f_trig = triginterp(s_s_list, s_f_list, pt, L, N)

# print (time.time() - st)

# print f_eval, f_trig
