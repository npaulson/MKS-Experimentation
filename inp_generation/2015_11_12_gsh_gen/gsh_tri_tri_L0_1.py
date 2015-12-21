import numpy as np


def gsh_basis_info():

    indxvec = np.array([[0, 0, 0],
                        [1, -1, -1],
                        [1, -1, 0],
                        [1, -1, 1],
                        [1, 0, -1],
                        [1, 0, 0],
                        [1, 0, 1],
                        [1, 1, -1],
                        [1, 1, 0],
                        [1, 1, 1]])

    return indxvec


def gsh_eval(X, Bvec):

    phi1 = X[..., 0]
    phi = X[..., 1]
    phi2 = X[..., 2]

    zvec = np.abs(phi) < 1e-8
    zvec = zvec.astype(int)
    randvec = np.round(np.random.rand(zvec.size)).reshape(zvec.shape)
    randvecopp = np.ones(zvec.shape) - randvec
    phi += (1e-7)*zvec*(randvec - randvecopp)

    final_shape = np.hstack([phi1.shape, len(Bvec)])
    tfunc = np.zeros(final_shape, dtype='complex128')

    c = 0
    for Bindx in Bvec:

        if Bindx == 0:
            tfunc[..., c] = 1

        if Bindx == 1:
            tfunc[..., c] = (0.3e1 / 0.2e1) * (0.1e1 + np.cos(phi)) * np.exp((-1*1j) * (phi1 + phi2))

        if Bindx == 2:
            t329 = np.cos(phi)
            tfunc[..., c] = (-0.3e1 / 0.2e1*1j) * np.exp((-1*1j) * phi1) * np.sqrt(0.2e1) * np.sqrt((1 + t329)) * np.sqrt((1 - t329))

        if Bindx == 3:
            tfunc[..., c] = (0.3e1 / 0.2e1) * (-0.1e1 + np.cos(phi)) * np.exp((-1*1j) * (phi1 - phi2))

        if Bindx == 4:
            t330 = np.cos(phi)
            tfunc[..., c] = (-0.3e1 / 0.2e1*1j) * np.exp((-1*1j) * phi2) * np.sqrt(0.2e1) * np.sqrt((1 - t330)) * np.sqrt((1 + t330))

        if Bindx == 5:
            tfunc[..., c] = 0.3e1 * np.cos(phi)

        if Bindx == 6:
            t331 = np.cos(phi)
            tfunc[..., c] = (-0.3e1 / 0.2e1*1j) * np.exp((1j) * phi2) * np.sqrt(0.2e1) * np.sqrt((1 - t331)) * np.sqrt((1 + t331))

        if Bindx == 7:
            tfunc[..., c] = (0.3e1 / 0.2e1) * (-0.1e1 + np.cos(phi)) * np.exp((1j) * (phi1 - phi2))

        if Bindx == 8:
            t332 = np.cos(phi)
            tfunc[..., c] = (-0.3e1 / 0.2e1*1j) * np.exp((1j) * phi1) * np.sqrt(0.2e1) * np.sqrt((1 - t332)) * np.sqrt((1 + t332))

        if Bindx == 9:
            tfunc[..., c] = (0.3e1 / 0.2e1) * (0.1e1 + np.cos(phi)) * np.exp((1j) * (phi1 + phi2))

        c += 1

    return tfunc


if __name__ == '__main__':
    X = np.zeros([2, 3])
    phi1 = np.array([0.1,0.2])
    X[:, 0] = phi1
    phi = np.array([0.0, 0.4])
    X[:, 1] = phi
    phi2 = np.array([0.3, 0.6])
    X[:, 2] = phi2

    indxvec = gsh_basis_info()
    print indxvec

    lte2 = indxvec[:, 0] <= 2
    print lte2

    Bvec = np.arange(indxvec.shape[0])[lte2]
    print Bvec

    out_tvalues = gsh_eval(X, Bvec)
    print out_tvalues
    print out_tvalues.shape

