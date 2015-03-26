# This script demonstrates that the generation of the microstucture function
# is not consistent between methods

import numpy as np


def mf_v1(micr, el, ns, Hi, order):

    if order == 1:
        H = Hi
        m = micr

    if order == 2:

        hs = np.array([[1, 1], [0, 0], [1, 0], [0, 1]])
        vec = np.array([[1, 0], [1, 1], [1, 2]])

        H = hs.shape[0] * vec.shape[0]

        k = 0
        m = np.zeros([ns, H, el, el, el])
        for hh in xrange(hs.shape[0]):
            for t in xrange(vec.shape[0]):
                a1 = micr[:, hs[hh, 0], ...]
                a2 = np.roll(micr[:, hs[hh, 1], ...], vec[t, 0], vec[t, 1])
                m[:, k, ...] = a1 * a2
                k = k + 1

    return m, H


def mf_v2(micr, el, Hi, order):

    if order == 1:
        H = Hi
        m = micr

    if order == 2:

        hs = np.array([[1, 1], [0, 0], [1, 0], [0, 1]])
        vec = np.array([[1, 0], [1, 1], [1, 2]])

        H = hs.shape[0] * vec.shape[0]

        k = 0
        m = np.zeros([H, el, el, el])
        for hh in xrange(hs.shape[0]):
            for t in xrange(vec.shape[0]):
                a1 = micr[hs[hh, 0], ...]
                a2 = np.roll(micr[hs[hh, 1], ...], vec[t, 0], vec[t, 1])
                m[k, ...] = a1 * a2
                k = k + 1

    return m, H

pre_micr = np.load('pre_msf_200calRpc.npy')
el = 21
ns = 2
Hi = 2
order = 2

print pre_micr.shape

# make MSF version 1

[micr, H] = mf_v1(pre_micr[0:2, ...], el, 2, Hi, order)

micrA = micr[0, ...]

M = np.fft.fftn(micr, axes=[2, 3, 4]).reshape([2, H, el**3])

print "msf version 1 for frequencies 0 and 1\n"
print M[0, :, 0]
print "\n"
print M[0, :, 1]
print "\n"

del micr, H, M

# make MSF version 2

[micr, H] = mf_v2(pre_micr[0, ...], el, Hi, order)

micrB = micr

M = np.fft.fftn(micr, axes=[1, 2, 3]).reshape([H, el**3])

print "msf version 2 for frequencies 0 and 1\n"
print M[:, 0]
print "\n"
print M[:, 1]
print "\n"

del micr, H, M

print np.array_equal(micrA, micrB)
