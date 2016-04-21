import numpy as np


def gsh_basis_info():

    indxvec = np.array([[0, 0, 1],
                        [2, -2, 1],
                        [2, -1, 1],
                        [2, 0, 1],
                        [2, 1, 1],
                        [2, 2, 1],
                        [4, -4, 1],
                        [4, -3, 1],
                        [4, -2, 1],
                        [4, -1, 1],
                        [4, 0, 1],
                        [4, 1, 1],
                        [4, 2, 1],
                        [4, 3, 1],
                        [4, 4, 1]])

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
            t1 = np.sin(phi)
            tfunc[..., c] = -(0.5e1 / 0.4e1) * np.exp((-2*1j) * phi1) * np.sqrt(0.6e1) * t1 ** 2

        if Bindx == 2:
            t2 = np.cos(phi)
            tfunc[..., c] = (-0.5e1 / 0.2e1*1j) * np.exp((-1*1j) * phi1) * np.sqrt(0.6e1) * np.sqrt((1 + t2)) * t2 * np.sqrt((1 - t2))

        if Bindx == 3:
            t3 = np.cos(phi)
            tfunc[..., c] = 0.15e2 / 0.2e1 * t3 ** 2 - 0.5e1 / 0.2e1

        if Bindx == 4:
            t4 = np.cos(phi)
            tfunc[..., c] = (-0.5e1 / 0.2e1*1j) * np.exp((1j) * phi1) * np.sqrt(0.6e1) * np.sqrt((1 - t4)) * np.sqrt((1 + t4)) * t4

        if Bindx == 5:
            t5 = np.sin(phi)
            tfunc[..., c] = -(0.5e1 / 0.4e1) * np.exp((2*1j) * phi1) * np.sqrt(0.6e1) * t5 ** 2

        if Bindx == 6:
            t8 = np.sin(phi)
            t6 = t8 ** 2
            tfunc[..., c] = (0.9e1 / 0.16e2) * np.exp((-4*1j) * phi1) * np.sqrt(0.70e2) * t6 ** 2

        if Bindx == 7:
            t9 = np.cos(phi)
            tfunc[..., c] = (0.9e1 / 0.4e1*1j) * t9 * (1 + (-2 + t9) * t9) * ((1 + t9) ** (0.3e1 / 0.2e1)) * np.sqrt(0.35e2) * np.exp((-3*1j) * phi1) * ((1 - t9) ** (-0.1e1 / 0.2e1))

        if Bindx == 8:
            t11 = np.cos(phi)
            t10 = np.sin(phi)
            tfunc[..., c] = -(0.9e1 / 0.8e1) * np.exp((-2*1j) * phi1) * np.sqrt(0.10e2) * t10 ** 2 * (7 * t11 ** 2 - 1)

        if Bindx == 9:
            t12 = np.cos(phi)
            tfunc[..., c] = (-0.9e1 / 0.4e1*1j) * np.exp((-1*1j) * phi1) * np.sqrt(0.5e1) * np.sqrt((1 + t12)) * t12 * np.sqrt((1 - t12)) * (7 * t12 ** 2 - 3)

        if Bindx == 10:
            t17 = np.cos(phi)
            t18 = t17 ** 2
            tfunc[..., c] = 0.27e2 / 0.8e1 + (-0.135e3 / 0.4e1 + 0.315e3 / 0.8e1 * t18) * t18

        if Bindx == 11:
            t20 = np.cos(phi)
            tfunc[..., c] = (-0.9e1 / 0.4e1*1j) * np.exp((1j) * phi1) * np.sqrt(0.5e1) * np.sqrt((1 - t20)) * np.sqrt((1 + t20)) * t20 * (7 * t20 ** 2 - 3)

        if Bindx == 12:
            t22 = np.cos(phi)
            t21 = np.sin(phi)
            tfunc[..., c] = -(0.9e1 / 0.8e1) * np.exp((2*1j) * phi1) * np.sqrt(0.10e2) * t21 ** 2 * (7 * t22 ** 2 - 1)

        if Bindx == 13:
            t23 = np.cos(phi)
            tfunc[..., c] = (0.9e1 / 0.4e1*1j) * np.exp((3*1j) * phi1) * np.sqrt(0.35e2) * ((1 - t23) ** (0.3e1 / 0.2e1)) * ((1 + t23) ** (0.3e1 / 0.2e1)) * t23

        if Bindx == 14:
            t26 = np.sin(phi)
            t24 = t26 ** 2
            tfunc[..., c] = (0.9e1 / 0.16e2) * np.exp((4*1j) * phi1) * np.sqrt(0.70e2) * t24 ** 2

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

