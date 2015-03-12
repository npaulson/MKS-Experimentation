# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 20:20:42 2014

@author: Noah
"""

import numpy as np
import time

n = 1000
m = 25
R = np.random.rand(n, m)

# # Save each row of R in '.npy' format
# start = time.time()
# for ii in range(len(R[:, 0])):
#     filename = 'R_%s' % ii
#     np.save(filename, R[ii, :])
#     b = np.load(filename + '.npy')
#     if ii == 0:
#         print b
# end = time.time()
# timeE = np.round((end - start), 5)
# print "time to save each row in '.npy' format: %s seconds" % timeE


@profile
def save_txt_w_numpy():
    # Save each row of R in '.txt' format using numpy
    start = time.time()
    for ii in range(len(R[:, 0])):
        filename = 'R_%s' % ii
        np.savetxt(filename, R[ii, :])
    end = time.time()
    timeE = np.round((end - start), 5)
    print "time to save each row in '.txt' format: %s seconds" % timeE

# # Save each row of R in '.txt' format by opening and writing individually
# start = time.time()
# for ii in range(len(R[:, 0])):
#     filename = 'R_%s' % ii
#     f = open(filename, 'a')
#     # for jj in xrange(len(R[0, :])):
#     #     f.write(str(R[ii, jj]) + '\n')

#     wrtstr = ''
#     for jj in xrange(R.shape[1]):
#         if jj == R.shape[1]:
#             wrtstr += str(R[ii, jj]) + '\n'
#         else:
#             wrtstr += str(R[ii, jj]) + ' '

#     f.write(wrtstr)

#     f.close()

#     f = open(filename, 'r')
#     linelist = f.readlines()

#     b = np.zeros([len(R[0, :])])

#     # for jj in xrange(len(R[0, :])):
#     #     b[jj] = linelist[jj]

#     b = linelist[0].split()

#     if ii == 0:
#         print b
#     f.close()

# end = time.time()
# timeE = np.round((end - start), 5)
# print "time to save each row in '.txt' format: %s seconds" % timeE


# def keep_open():
#     # The task is append each value in the vector T (of length n) to a file
#     # matching its index for m randomly generated T's.
#     f = []

#     for ii in xrange(n):
#         filename = 'R_%s' % ii
#         f.append(open(filename, 'a'))

#     for jj in xrange(m):

#         T = np.random.rand(n)

#         for ii in xrange(n):
#             filename = 'R_%s' % ii
#             f[ii].write(str(T[ii]) + '\n')

#     for ii in xrange(n):
#         f[ii].close()


# def closed():
#     c = 0
#     for jj in xrange(m):

#         T = np.random.rand(n)

#         for ii in xrange(n):
#             c += 1
#             filename = 'Rr_%s' % c
#             f = open(filename, 'a')
#             f.write(str(T[ii]) + '\n')
#             f.close()

if __name__ == "__main__":
    st = time.time()
    save_txt_w_numpy()
    print "elapsed time: %s" % (time.time() - st)
