import numpy as np
from tables import *
import time

ns = 50
H = 1000
K = 40


Set1 = np.random.rand(ns, K, H)

print Set1.nbytes

print Set1.dtype

# print "first method"

# st = time.time()

# for sn in xrange(ns):
#     for k in xrange(K):
#         np.save('M_%s_%s' % (sn, k), Set1[sn, k, :])

# timeA = np.round(time.time() - st, 5)
# print "part A: elaspsed time: %s" % np.round(time.time() - st, 5)

# st = time.time()

# sum = 0
# for sn in xrange(ns):
#     for k in xrange(K):

#         temp = np.load('M_%s_%s.npy' % (sn, k))

#         sum += temp

# timeB = np.round(time.time() - st, 5)
# print "part B: elaspsed time: %s" % timeB

# print "total time for first method: %s" % (timeA + timeB)


# print "second method"

# st = time.time()

# for sn in xrange(ns):
#     np.save('M_%s' % sn, Set1[sn, :, :])

# timeA = np.round(time.time() - st, 5)
# print "part A: elaspsed time: %s" % np.round(time.time() - st, 5)

# st = time.time()

# sum = 0
# for sn in xrange(ns):
#     for k in xrange(K):

#         temp = np.load('M_%s.npy' % sn)

#         sum += temp[k, :]

# timeB = np.round(time.time() - st, 5)
# print "part B: elaspsed time: %s" % timeB

# print "total time for second method: %s" % (timeA + timeB)

print "third method"

st = time.time()

basefile = open_file("basefile.h5", mode="w", title="Test file")

group = basefile.create_group("/", 'data', 'data tables')

bigpiece = np.zeros([1, K, H])

print "\nbigpiece shape:"
print bigpiece.shape

bigpiece[0, :, :] = Set1[0, :, :]

# a = Float64Atom(shape=(0, K, H))
a = Float64Atom()

# bigarray[0, ...] = piece1

bigarr = basefile.create_earray(group, 'bigarray', a, (0, K, H))

bigarr.append(bigpiece)


bigpiece[0, :, :] = Set1[1, :, :]

bigarr.append(bigpiece)

basefile.close()

basefile = open_file("basefile.h5", mode="r", title="Test file")

print(basefile)

myarray = basefile.root.data.bigarray

read_myarray = myarray.read()

print read_myarray[0, :, :]

print read_myarray.shape

basefile.close()

print "part A: elaspsed time: %s" % np.round(time.time() - st, 5)
