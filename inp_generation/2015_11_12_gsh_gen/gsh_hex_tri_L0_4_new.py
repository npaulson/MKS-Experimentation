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
            t27 = np.sin(phi)
            tfunc[..., c] = -(0.5e1 / 0.4e1) * np.exp((-2*1j) * phi1) * np.sqrt(0.6e1) * t27 ** 2

        if Bindx == 2:
            t28 = np.cos(phi)
            tfunc[..., c] = (-0.5e1 / 0.2e1*1j) * np.exp((-1*1j) * phi1) * np.sqrt(0.6e1) * np.sqrt((1 + t28)) * t28 * np.sqrt((1 - t28))

        if Bindx == 3:
            t29 = np.cos(phi)
            tfunc[..., c] = 0.15e2 / 0.2e1 * t29 ** 2 - 0.5e1 / 0.2e1

        if Bindx == 4:
            t30 = np.cos(phi)
            tfunc[..., c] = (-0.5e1 / 0.2e1*1j) * np.exp((1j) * phi1) * np.sqrt(0.6e1) * np.sqrt((1 - t30)) * np.sqrt((1 + t30)) * t30

        if Bindx == 5:
            t31 = np.sin(phi)
            tfunc[..., c] = -(0.5e1 / 0.4e1) * np.exp((2*1j) * phi1) * np.sqrt(0.6e1) * t31 ** 2

        if Bindx == 6:
            t34 = np.sin(phi)
            t32 = t34 ** 2
            tfunc[..., c] = (0.9e1 / 0.16e2) * np.exp((-4*1j) * phi1) * np.sqrt(0.70e2) * t32 ** 2

        if Bindx == 7:
            t35 = np.cos(phi)
            tfunc[..., c] = (0.9e1 / 0.4e1*1j) * t35 * (1 + (-2 + t35) * t35) * ((1 + t35) ** (0.3e1 / 0.2e1)) * np.sqrt(0.35e2) * np.exp((-3*1j) * phi1) * ((1 - t35) ** (-0.1e1 / 0.2e1))

        if Bindx == 8:
            t37 = np.cos(phi)
            t36 = np.sin(phi)
            tfunc[..., c] = -(0.9e1 / 0.8e1) * np.exp((-2*1j) * phi1) * np.sqrt(0.10e2) * t36 ** 2 * (7 * t37 ** 2 - 1)

        if Bindx == 9:
            t38 = np.cos(phi)
            tfunc[..., c] = (-0.9e1 / 0.4e1*1j) * np.exp((-1*1j) * phi1) * np.sqrt(0.5e1) * t38 * np.sqrt((1 + t38)) * np.sqrt((1 - t38)) * (7 * t38 ** 2 - 3)

        if Bindx == 10:
            t43 = np.cos(phi)
            t44 = t43 ** 2
            tfunc[..., c] = 0.27e2 / 0.8e1 + (-0.135e3 / 0.4e1 + 0.315e3 / 0.8e1 * t44) * t44

        if Bindx == 11:
            t46 = np.cos(phi)
            tfunc[..., c] = (-0.9e1 / 0.4e1*1j) * np.exp((1j) * phi1) * np.sqrt(0.5e1) * np.sqrt((1 - t46)) * np.sqrt((1 + t46)) * t46 * (7 * t46 ** 2 - 3)

        if Bindx == 12:
            t48 = np.cos(phi)
            t47 = np.sin(phi)
            tfunc[..., c] = -(0.9e1 / 0.8e1) * np.exp((2*1j) * phi1) * np.sqrt(0.10e2) * t47 ** 2 * (7 * t48 ** 2 - 1)

        if Bindx == 13:
            t49 = np.cos(phi)
            tfunc[..., c] = (0.9e1 / 0.4e1*1j) * np.exp((3*1j) * phi1) * np.sqrt(0.35e2) * ((1 - t49) ** (0.3e1 / 0.2e1)) * ((1 + t49) ** (0.3e1 / 0.2e1)) * t49

        if Bindx == 14:
            t52 = np.sin(phi)
            t50 = t52 ** 2
            tfunc[..., c] = (0.9e1 / 0.16e2) * np.exp((4*1j) * phi1) * np.sqrt(0.70e2) * t50 ** 2

        c += 1

    return tfunc


if __name__ == '__main__':
    X = np.zeros([2, 3])
    phi1 = np.array([0.1, 0.2])
    X[:, 0] = phi1
    phi = np.array([0.2, 0.0])
    X[:, 1] = phi
    phi2 = np.array([0.3, 0.6])
    X[:, 2] = phi2

    indxvec = gsh_basis_info()
    print indxvec

    lte2 = indxvec[:, 0] <= 4
    print lte2

    Bvec = np.arange(indxvec.shape[0])[lte2]
    print Bvec

    out_tvalues = gsh_eval(X, Bvec)
    print out_tvalues
    print out_tvalues.shape

