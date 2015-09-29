import numpy as np


def et_ii(th):

	et_ii_vec = np.array([np.sqrt(2/3)*np.cos(th-(np.pi/3)),
                          np.sqrt(2/3)*np.cos(th+(np.pi/3)),
                          -np.sqrt(2/3)*np.cos(th)])

	return et_ii_vec


def rotmat2euler(g):

    if np.abs(g[2, 2] - 1) < .01:

        Phi = 0.0
        phi1 = 0.5*np.arctan2(g[0, 1], g[0, 0])
        phi2 = phi1

    else:

        Phi = np.arccos(g[2, 2])
        phi1 = np.arctan2(g[2, 0]/np.sin(Phi), -g[2, 1]/np.sin(Phi))
        phi2 = np.arctan2(g[0, 2]/np.sin(Phi), g[1, 2]/np.sin(Phi))

    euler = np.array([phi1, Phi, phi2])

    return euler


def calc(et):

    # find the deviatoric total strain tensor
    et_ = et - (1/3)*np.trace(et)*np.eye(3)

    # calculate the magnitude of the deviatoric total strain tensor
    # en = np.sqrt(np.sum(et_[...]**2))
    en = np.linalg.norm(et_)
    print en

    # normalize the deviatoric total strain tensor
    et_n = et_ / en

    # find the principal strains 
    w,v = np.linalg.eig(et_n)

    print w
    print v

    # sort the principal strains in descending order
    indx = np.flipud(np.argsort(w))

    W = w[indx]

    print W

    V = np.array([v[:, indx[0]], v[:, indx[1]], v[:, indx[2]]])

    print V

    # determine the angle theta associated with the diagonal matrix of interest
    theta1 = np.arccos(np.sqrt(3/2)*W[1])+(np.pi/3)
    theta2 = np.arccos(np.sqrt(3/2)*W[2])-(np.pi/3)
    theta3 = np.arccos(-np.sqrt(3/2)*W[3])

    print et_ii(theta2)

    # demonstrate the transformation from et_n to the principal frame using 
    # eigenvectors
    print V.T*et_n*V

    # find the set of euler angle associated with the transformation from the
    # principal to crystal reference frames <-- ?
    euler_P_C = rotmat2euler(V)

    return theta, euler_P_C


if __name__ == "__main__":

	F = 2*(np.random.rand(3, 3)-0.5)
	et = 0.5*(F.T*F-np.eye(3))

	theta, euler_P_C = calc(et)

	print theta
	print euler_P_C
