import numpy as np
from tables import *
import time

# to run this file type the following in the command prompt:
# $ python -m memory_profiler chunk_test_v2.py

ns = 50
H = 30000
K = 40

# @profile
def method1(Set1):

    print "\nfirst method"

    st = time.time()

    # open HDF5 file
    basefile = open_file("basefile.h5", mode="w", title="Test file")

    # create a group one level below root called data
    group = basefile.create_group("/", 'data', 'data tables')

    # define the datatype for our array
    a = Float64Atom()

    # initialize an array in the level below group where the first dimension is
    # extendable
    bigarr = basefile.create_earray(group, 'bigarray', a, (0, K, H))

    # begin to populate array
    for sn in xrange(ns):
        chunk = np.expand_dims(Set1[sn, :, :], axis=0)
        bigarr.append(chunk)
        del chunk

    # close the HDF5 file
    basefile.close()

    timeA = np.round(time.time() - st, 5)
    print "part A: elaspsed time: %s" % timeA

    st = time.time()

    # reopen the file
    basefile = open_file("basefile.h5", mode="r", title="Test file")

    # # show the directory structure of the file
    # print(basefile)

    # define an object for the array
    myarray = basefile.root.data.bigarray

    sum = 0

    for k in xrange(K):
        tmp = np.sum(myarray[:, k, :], axis=0)
        sum += tmp
        del tmp

    print sum[:10]

    basefile.close()

    timeB = np.round(time.time() - st, 5)
    print "part B: elaspsed time: %s" % timeB
    print "total time for first method: %s" % (timeA + timeB)


# @profile
def method2(Set1):

    print "\nsecond method"

    st = time.time()

    # open HDF5 file
    basefile = open_file("basefile2.h5", mode="w", title="Test file")

    # create a group one level below root called data
    group = basefile.create_group("/", 'data', 'data tables')

    # define the datatype for our array
    a = Float64Atom()

    filters = Filters(complevel=5, complib='zlib')

    # initialize an array in the level below group where the first dimension is
    # extendable
    bigarr = basefile.create_carray(group,
                                    'bigarray',
                                    a,
                                    (ns, K, H),
                                    filters=filters)

    # begin to populate array
    for sn in xrange(ns):
        bigarr[sn, :, :] = Set1[sn, :, :]

    # close the HDF5 file
    basefile.close()

    timeA = np.round(time.time() - st, 5)
    print "part A: elaspsed time: %s" % timeA

    st = time.time()

    # reopen the file
    basefile = open_file("basefile2.h5", mode="r", title="Test file")

    # # show the directory structure of the file
    # print(basefile)

    # define an object for the array
    myarray = basefile.root.data.bigarray

    sum = 0

    for k in xrange(K):
        tmp = np.sum(myarray[:, k, :], axis=0)
        sum += tmp
        del tmp

    print sum[:10]

    basefile.close()

    timeB = np.round(time.time() - st, 5)
    print "part B: elaspsed time: %s" % timeB
    print "total time for second method: %s" % (timeA + timeB)


if __name__ == "__main__":

    Set1 = np.random.rand(ns, K, H)

    setsz = int(Set1.nbytes)/(10.**6)
    print "Set1 is %s Mb in size with data type %s" % (setsz,
                                                       Set1.dtype)

    method2(Set1)

