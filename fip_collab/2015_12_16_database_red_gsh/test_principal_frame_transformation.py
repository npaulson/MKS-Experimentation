import numpy as np
from numpy import linalg as LA


def gen_test_tensor():

    """ generate a random 3x3 matrix with values ranging from -1 to 1. This
    represents some deformation gradient F """
    F = 2*(np.random.rand(3, 3)-.5)
    # print "deformation gradient, F:"
    # print F.round(4)

    # F = np.array([[1., 0., 1.],
    #               [0., 0., 0.],
    #               [1., 0., 0.]])

    """ calculate the associated total strain tensor from F as the Cauchy-Green
    strain. This tensor is in the sample frame """
    et = 0.5*(np.dot(np.transpose(F), F) - np.eye(3))
    # print "Cauchy-Green strain tensor, et:"
    # print et.round(4)

    """ find the deviatoric total strain tensor """
    et_ = et - (1./3.)*np.trace(et)*np.eye(3)
    # print "Deviatoric strain tensor, et_:"
    # print et_.round(4)

    return et_


def sorted_eig(et_n):

    """ find the principal strains """
    eigval, eigvec = LA.eig(et_n)
    # print "eigenvalues and eigenvectors of et_n"
    # print eigval.round(4)
    # print eigvec.round(4)

    """ sort the principal strains in descending order """
    indx = np.argsort(eigval)
    indx = indx[::-1]

    eigval = eigval[indx]

    eigvec = eigvec[:, indx]

    print "sorted eigenvalues and eigenvectors of et_n"
    print eigval.round(4)
    print eigvec.round(4)

    return eigval, eigvec


def theta2eig(x):

    et_ii = np.array([np.sqrt(2./3.)*np.cos(x-(np.pi/3.)),
                      np.sqrt(2./3.)*np.cos(x+(np.pi/3.)),
                      -np.sqrt(2./3.)*np.cos(x)])

    return et_ii


def eig2theta(eigval):

    theta = np.zeros(3)

    # determine the angle theta associated with the diagonal matrix of interest
    theta[0] = np.arccos(np.sqrt(3./2.)*eigval[0])+(np.pi/3.)
    theta[1] = np.arccos(np.sqrt(3./2.)*eigval[1])-(np.pi/3.)
    theta[2] = np.arccos(-np.sqrt(3./2.)*eigval[2])

    print "deformation mode angles versions: %s" % theta.round(4)

    return theta[2]


# et_ = np.array([[1., 0., 0.],
#                 [0., 0., 0.],
#                 [0., 0., -1.]])
et_ = gen_test_tensor()

# calculate the magnitude of the deviatoric total strain tensor
en = np.sqrt(np.sum(et_**2))
# print "magnitude of deviatoric strain tensor, en:"
# print en.round(4)

# normalize the deviatoric total strain tensor
et_n = et_ / en

print "unit deviatoric strain tensor, et_n:"
print et_n.round(4)

eigval, eigvec = sorted_eig(et_n)
theta = eig2theta(eigval)

print "retrieved eigenvalues from deformation mode:"
print theta2eig(theta).round(4)

print "retrieved eigenvalues from symmetric deformation mode:"
print theta2eig((2.*np.pi/3.)-theta).round(4)

recon = np.dot(np.dot(np.transpose(eigvec), et_n), eigvec)
print "demonstrate the transformation from et_n to the principal frame:"
print recon.round(4)

et_n_recon = np.dot(np.dot(eigvec, recon), np.transpose(eigvec))
print "demonstrate the transformation from recon to et_n:"
print et_n_recon.round(4)

print "\n\nnow lets see what theta is for the negative strain tensor\n\n"""

print "unit deviatoric strain tensor, et_n:"
print -et_n.round(4)

eigval, eigvec = sorted_eig(-et_n)
theta = eig2theta(eigval)

print "retrieved eigenvalues from deformation mode:"
print theta2eig(theta).round(4)

print "retrieved eigenvalues from symmetric deformation mode:"
print theta2eig((2.*np.pi/3.)-theta).round(4)

recon = np.dot(np.dot(np.transpose(eigvec), -et_n), eigvec)
print "demonstrate the transformation from et_n to the principal frame:"
print recon.round(4)

et_n_recon = np.dot(np.dot(eigvec, recon), np.transpose(eigvec))
print "demonstrate the transformation from recon to et_n:"
print et_n_recon.round(4)
