import numpy as np
import matplotlib.pyplot as plt


def triginterp(s_list, f_list, xi, L, N):

    Pvec = f_list * \
        np.exp((2*np.pi*1j*s_list[:, 0]*xi[:, 0:1])/L)

    return np.real(np.sum(Pvec, 1)/N)


def mirror_inputs(yvar, a, ai, bi, st_i, st_e):
    """
    prepare mirrored versions of the x, y axis data vectors
    st_i: sampling interval from yvar
    """
    # mp is a point that is inserted between the original samples
    # and the mirrored samples to smooth out the representation
    mp = yvar[-1] + st_i*(yvar[-1]-yvar[-2])

    pre_range = np.arange(ai, bi+1, st_i)
    offset = bi - pre_range[-1]
    cur_range = pre_range + offset
    node_indx = cur_range - ai

    tmp = yvar[node_indx]

    # ynode is the modified vector of samples including the mirrored and
    # interted points
    ynode = np.hstack([tmp, mp, mp, tmp[::-1]])[:-1]

    N = len(ynode)

    # etvecS is the starting normalized total strain
    etvecS = a + offset*st_e
    # etvecE is the terminal normalized total strain
    etvecE = etvecS + N*st_i*st_e

    L = etvecE - etvecS

    # xnode is the vector of normalized total strains associated with ynode
    # xnode = np.arange(etvecS, etvecE-st_e, st_i*st_e)
    xnode = np.arange(etvecS, etvecE, st_i*st_e+1E-15)

    return xnode, ynode, etvecS, etvecE, N, L


def pretrig(xi, ynode, etvecS, N, L):

    Yk = np.fft.fft(ynode)

    # xi is the vector of total strains to be used as interpolation points
    # with the spectral interpolation. Note that the strains are shifted so
    # that the first is zero
    xi = xi[:, np.newaxis] - etvecS

    sh = Yk.shape
    sz = Yk.size

    # center the fft s.t. the 0th frequency is centered
    Yk = np.fft.fftshift(Yk)

    # find half of the range for each dimension in the fft
    kmax = np.int8(np.floor(np.array(sh)/2.))
    kmax = np.expand_dims(kmax, 1)

    # generate indices associated with the fft
    INDX = np.unravel_index(np.arange(sz), sh)
    # array containing indices associated with the fft
    INDX = np.transpose(np.array(INDX) - kmax)

    maxf = np.max(np.abs(Yk))  # amplitude of frequency with max amplitude

    # find the indices of fft frequencies with magnitudes greater than .25% of
    # the largest value of the fft
    gt_p25 = np.abs(Yk) > 0.0 * maxf

    s_list = INDX[gt_p25, :]
    f_list = Yk[gt_p25]

    P = triginterp(s_list, f_list, xi, L, N)

    return np.real(P)


if __name__ == "__main__":

    # load raw data
    et_norm = np.load('et_norm.npy')
    ep = np.load('ep.npy')

    a = .0060  # start of range for legendre interpolation
    b = .0100  # end of range for legendre interpolation

    st_i = 12
    st_e = 0.0001

    # the following vector closely matches that of et_norm
    etvec = np.arange(a, b + st_e, st_e)

    ai = np.int8(np.round(a/st_e))-1
    bi = np.int8(np.round(b/st_e))-1

    xvar = et_norm[ai:bi+1]
    yvar = ep[ai:bi+1, 0]

    [xnode, ynode, etvecS, etvecE, N, L] = \
        mirror_inputs(yvar, a, ai, bi, st_i, st_e)

    ytest = pretrig(xvar, ynode, etvecS, N, L)

    # calculate error in this approach based on sampled values
    error = 100*np.abs((yvar - ytest)/xvar)

    print "number of samples: %s" % N
    print "mean error: %s%%" % np.mean(error)
    print "maximum error: %s%%" % np.max(error)

    plt.figure(num=1, figsize=[10, 6])

    plt.plot(xvar, yvar, 'bx')

    print xnode.size
    print ynode.size

    plt.plot(xnode, ynode, 'bo')

    xplt = np.linspace(a, b, 150)
    yplt = pretrig(xplt, ynode, etvecS, N, L)
    plt.plot(xplt, yplt, 'r')

    plt.show()
