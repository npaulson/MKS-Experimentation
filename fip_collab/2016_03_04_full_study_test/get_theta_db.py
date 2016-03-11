import numpy as np


def theta2eig(x):

    et_ii = np.array([np.sqrt(2./3.)*np.cos(x-(np.pi/3.)),
                      np.sqrt(2./3.)*np.cos(x+(np.pi/3.)),
                      -np.sqrt(2./3.)*np.cos(x)])
    return et_ii


if __name__ == '__main__':

    th_vec = np.arange(0, 60, 1.5)+0.75
    print "th_vec: %s" % str(th_vec)
    print "length(th_vec): %s" % th_vec.size
    th_vec = th_vec*(np.pi/180.)

    eigmat = np.zeros((th_vec.size, 3))

    for ii in xrange(th_vec.size):
        tmp = theta2eig(th_vec[ii])
        indx = np.argsort(np.abs(tmp))[::-1]
        eigmat[ii, :] = tmp[indx]

    print "vector of eigenvalues: "
    print eigmat

    np.savetxt("tensors.txt", eigmat)
