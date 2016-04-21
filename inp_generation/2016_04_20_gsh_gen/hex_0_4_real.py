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
            t1 = np.cos(phi)
            tfunc[..., c] = -0.5e1 / 0.2e1 * np.sqrt(0.3e1) * (t1 ** 2 - 1) * np.cos((2 * phi1))

        if Bindx == 2:
            t3 = np.cos(phi)
            t2 = np.sin(phi)
            tfunc[..., c] = -0.5e1 * np.sqrt(0.3e1) * t3 * t2 ** 2 * np.sin(phi1) * ((1 + t3) ** (-0.1e1 / 0.2e1)) * ((1 - t3) ** (-0.1e1 / 0.2e1))

        if Bindx == 3:
            t4 = np.cos(phi)
            tfunc[..., c] = 0.15e2 / 0.2e1 * t4 ** 2 - 0.5e1 / 0.2e1

        if Bindx == 4:
            t6 = np.cos(phi)
            t5 = np.sin(phi)
            tfunc[..., c] = -0.5e1 * np.sqrt(0.3e1) * t6 * t5 ** 2 * np.sin(phi1) * ((1 + t6) ** (-0.1e1 / 0.2e1)) * ((1 - t6) ** (-0.1e1 / 0.2e1))

        if Bindx == 5:
            t7 = np.cos(phi)
            tfunc[..., c] = -0.5e1 / 0.2e1 * np.sqrt(0.3e1) * (t7 ** 2 - 1) * np.cos((2 * phi1))

        if Bindx == 6:
            t8 = np.cos(phi)
            t9 = t8 ** 2
            tfunc[..., c] = 0.9e1 / 0.8e1 * np.sqrt(0.35e2) * np.cos((4 * phi1)) * (1 + (-2 + t9) * t9)

        if Bindx == 7:
            t14 = np.sin(phi)
            t12 = t14 ** 2
            t11 = np.cos(phi)
            tfunc[..., c] = -0.9e1 / 0.4e1 * np.sqrt(0.2e1) * np.sqrt(0.35e2) * t11 * t12 ** 2 * np.sin((3 * phi1)) * ((1 + t11) ** (-0.1e1 / 0.2e1)) * ((1 - t11) ** (-0.1e1 / 0.2e1))

        if Bindx == 8:
            t15 = np.cos(phi)
            t16 = t15 ** 2
            tfunc[..., c] = -0.9e1 / 0.4e1 * np.sqrt(0.5e1) * (1 + (-8 + 7 * t16) * t16) * np.cos((2 * phi1))

        if Bindx == 9:
            t19 = np.cos(phi)
            t18 = np.sin(phi)
            tfunc[..., c] = -0.9e1 / 0.4e1 * np.sqrt(0.2e1) * np.sqrt(0.5e1) * t19 * t18 ** 2 * (7 * t19 ** 2 - 3) * np.sin(phi1) * ((1 + t19) ** (-0.1e1 / 0.2e1)) * ((1 - t19) ** (-0.1e1 / 0.2e1))

        if Bindx == 10:
            t20 = np.cos(phi)
            t21 = t20 ** 2
            tfunc[..., c] = 0.27e2 / 0.8e1 + (-0.135e3 / 0.4e1 + 0.315e3 / 0.8e1 * t21) * t21

        if Bindx == 11:
            t24 = np.cos(phi)
            t23 = np.sin(phi)
            tfunc[..., c] = -0.9e1 / 0.4e1 * np.sqrt(0.2e1) * np.sqrt(0.5e1) * t24 * t23 ** 2 * (7 * t24 ** 2 - 3) * np.sin(phi1) * ((1 + t24) ** (-0.1e1 / 0.2e1)) * ((1 - t24) ** (-0.1e1 / 0.2e1))

        if Bindx == 12:
            t25 = np.cos(phi)
            t26 = t25 ** 2
            tfunc[..., c] = -0.9e1 / 0.4e1 * np.sqrt(0.5e1) * (1 + (-8 + 7 * t26) * t26) * np.cos((2 * phi1))

        if Bindx == 13:
            t31 = np.sin(phi)
            t29 = t31 ** 2
            t28 = np.cos(phi)
            tfunc[..., c] = -0.9e1 / 0.4e1 * np.sqrt(0.2e1) * np.sqrt(0.35e2) * t28 * t29 ** 2 * np.sin((3 * phi1)) * ((1 + t28) ** (-0.1e1 / 0.2e1)) * ((1 - t28) ** (-0.1e1 / 0.2e1))

        if Bindx == 14:
            t32 = np.cos(phi)
            t33 = t32 ** 2
            tfunc[..., c] = 0.9e1 / 0.8e1 * np.sqrt(0.35e2) * np.cos((4 * phi1)) * (1 + (-2 + t33) * t33)
	
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

