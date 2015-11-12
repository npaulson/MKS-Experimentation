import numpy as np
from numpy import linalg as LA


# generate a random 3x3 matrix with values ranging from -1 to 1. This
# represents some deformation gradient F
F = 2*(np.random.rand(3, 3)-.5)
print "deformation gradient, F:"
print F

# F = np.array([[1., 0., 1.],
#               [0., 0., 0.],
#               [1., 0., 0.]])

# calculate the associated total strain tensor from F as the Cauchy-Green
# strain. This tensor is in the sample frame
et = 0.5*(np.dot(np.transpose(F), F) - np.eye(3))
print "Cauchy-Green strain tensor, et:"
print et

# calculate the magnitude of the total strain tensor
en = np.sqrt(np.sum(et**2))
print "magnitude of strain tensor, en:"
print en

# find the deviatoric total strain tensor
et_ = et - (1./3.)*np.trace(et)*np.eye(3)
print "Deviatoric strain tensor, et_:"
print et_

# calculate the magnitude of the deviatoric total strain tensor
en = np.sqrt(np.sum(et_**2))
print "magnitude of deviatoric strain tensor, en:"
print en

# normalize the deviatoric total strain tensor
et_n = et_ / en

# find the principal strains
eigval, eigvec = LA.eig(et_n)
print "eigenvalues and eigenvectors of et_n"
print eigval
print eigvec

# sort the principal strains in descending order
indx = np.argsort(eigval)
indx = indx[::-1]

eigval = eigval[indx]

eigvec = eigvec[:, indx]

print "sorted eigenvalues and eigenvectors of et_n"
print eigval
print eigvec

# determine the angle theta associated with the diagonal matrix of interest
theta1 = np.arccos(np.sqrt(3./2.)*eigval[0])+(np.pi/3.)
theta2 = np.arccos(np.sqrt(3./2.)*eigval[1])-(np.pi/3.)
theta3 = np.arccos(-np.sqrt(3./2.)*eigval[2])

print "deformation mode angles: theta 1, 2 and 3"
print theta1
print theta2
print theta3


def et_back(x):

    et_ii = np.array([np.sqrt(2./3.)*np.cos(x-(np.pi/3.)),
                      np.sqrt(2./3.)*np.cos(x+(np.pi/3.)),
                      -np.sqrt(2./3.)*np.cos(x)])

    return et_ii

et_ii = et_back(theta2)

print "retrieved eigenvalues from deformation mode:"
print et_ii

recon = np.dot(np.dot(np.transpose(eigvec), et_n), eigvec)
recon = np.round(recon, 4)
print "demonstrate the transformation from et_n to the principal frame"
print recon

# # find the set of euler angle associated with the transformation from the
# # principal to crystal reference frames <-- ?
# euler = rotmat2euler(V)
