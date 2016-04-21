import numpy as np


def gsh_basis_info():

    indxvec = np.array([[2, -2, -2],
                        [2, -2, -1],
                        [2, -2, 0],
                        [2, -2, 1],
                        [2, -2, 2],
                        [2, -1, -2],
                        [2, -1, -1],
                        [2, -1, 0],
                        [2, -1, 1],
                        [2, -1, 2],
                        [2, 0, -2],
                        [2, 0, -1],
                        [2, 0, 0],
                        [2, 0, 1],
                        [2, 0, 2],
                        [2, 1, -2],
                        [2, 1, -1],
                        [2, 1, 0],
                        [2, 1, 1],
                        [2, 1, 2],
                        [2, 2, -2],
                        [2, 2, -1],
                        [2, 2, 0],
                        [2, 2, 1],
                        [2, 2, 2]])

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
            t1 = np.cos(phi)
            tfunc[..., c] = 0.5e1 / 0.4e1 * np.sqrt(0.2e1) * np.cos((2 * phi1 + 2 * phi2)) * (1 + (2 + t1) * t1)

        if Bindx == 1:
            t2 = np.cos(phi)
            tfunc[..., c] = -0.5e1 / 0.2e1 * np.sqrt(0.2e1) * ((1 + t2) ** (0.3e1 / 0.2e1)) * np.sqrt((1 - t2)) * np.sin((2 * phi1 + phi2))

        if Bindx == 2:
            t3 = np.cos(phi)
            tfunc[..., c] = -0.5e1 / 0.2e1 * np.sqrt(0.3e1) * (t3 ** 2 - 1) * np.cos((2 * phi1))

        if Bindx == 3:
            t4 = np.cos(phi)
            tfunc[..., c] = -0.5e1 / 0.2e1 * np.sqrt(0.2e1) * ((1 - t4) ** (0.3e1 / 0.2e1)) * np.sqrt((1 + t4)) * np.sin((2 * phi1 - phi2))

        if Bindx == 4:
            t5 = np.cos(phi)
            tfunc[..., c] = 0.5e1 / 0.4e1 * np.sqrt(0.2e1) * np.cos((2 * phi1 - 2 * phi2)) * (1 + (-2 + t5) * t5)

        if Bindx == 5:
            t6 = np.cos(phi)
            tfunc[..., c] = 0.5e1 / 0.2e1 * np.sqrt(0.2e1) * np.sqrt((1 - t6)) * ((1 + t6) ** (0.3e1 / 0.2e1)) * np.sin((phi1 + 2 * phi2))

        if Bindx == 6:
            t7 = np.cos(phi)
            tfunc[..., c] = 0.5e1 / 0.2e1 * np.sqrt(0.2e1) * (2 * t7 ** 2 + t7 - 1) * np.cos(phi1 + phi2)

        if Bindx == 7:
            t9 = np.cos(phi)
            t8 = np.sin(phi)
            tfunc[..., c] = -0.5e1 * np.sqrt(0.3e1) * t9 * t8 ** 2 * np.sin(phi1) * ((1 - t9) ** (-0.1e1 / 0.2e1)) * ((1 + t9) ** (-0.1e1 / 0.2e1))

        if Bindx == 8:
            t10 = np.cos(phi)
            tfunc[..., c] = -0.5e1 / 0.2e1 * np.sqrt(0.2e1) * (2 * t10 ** 2 - t10 - 1) * np.cos(phi1 - phi2)

        if Bindx == 9:
            t11 = np.cos(phi)
            tfunc[..., c] = -0.5e1 / 0.2e1 * np.sqrt(0.2e1) * ((1 - t11) ** (0.3e1 / 0.2e1)) * np.sqrt((1 + t11)) * np.sin((phi1 - 2 * phi2))

        if Bindx == 10:
            t12 = np.cos(phi)
            tfunc[..., c] = -0.5e1 / 0.2e1 * np.sqrt(0.3e1) * (t12 ** 2 - 1) * np.cos((2 * phi2))

        if Bindx == 11:
            t14 = np.cos(phi)
            t13 = np.sin(phi)
            tfunc[..., c] = 0.5e1 * np.sqrt(0.3e1) * t14 * t13 ** 2 * np.sin(phi2) * ((1 - t14) ** (-0.1e1 / 0.2e1)) * ((1 + t14) ** (-0.1e1 / 0.2e1))

        if Bindx == 12:
            t15 = np.cos(phi)
            tfunc[..., c] = 0.15e2 / 0.2e1 * t15 ** 2 - 0.5e1 / 0.2e1

        if Bindx == 13:
            t17 = np.cos(phi)
            t16 = np.sin(phi)
            tfunc[..., c] = 0.5e1 * np.sqrt(0.3e1) * t17 * t16 ** 2 * np.sin(phi2) * ((1 - t17) ** (-0.1e1 / 0.2e1)) * ((1 + t17) ** (-0.1e1 / 0.2e1))

        if Bindx == 14:
            t18 = np.cos(phi)
            tfunc[..., c] = -0.5e1 / 0.2e1 * np.sqrt(0.3e1) * (t18 ** 2 - 1) * np.cos((2 * phi2))

        if Bindx == 15:
            t19 = np.cos(phi)
            tfunc[..., c] = -0.5e1 / 0.2e1 * np.sqrt(0.2e1) * ((1 - t19) ** (0.3e1 / 0.2e1)) * np.sqrt((1 + t19)) * np.sin((phi1 - 2 * phi2))

        if Bindx == 16:
            t20 = np.cos(phi)
            tfunc[..., c] = -0.5e1 / 0.2e1 * np.sqrt(0.2e1) * (2 * t20 ** 2 - t20 - 1) * np.cos(phi1 - phi2)

        if Bindx == 17:
            t22 = np.cos(phi)
            t21 = np.sin(phi)
            tfunc[..., c] = -0.5e1 * np.sqrt(0.3e1) * t22 * t21 ** 2 * np.sin(phi1) * ((1 - t22) ** (-0.1e1 / 0.2e1)) * ((1 + t22) ** (-0.1e1 / 0.2e1))

        if Bindx == 18:
            t23 = np.cos(phi)
            tfunc[..., c] = 0.5e1 / 0.2e1 * np.sqrt(0.2e1) * (2 * t23 ** 2 + t23 - 1) * np.cos(phi1 + phi2)

        if Bindx == 19:
            t24 = np.cos(phi)
            tfunc[..., c] = 0.5e1 / 0.2e1 * np.sqrt(0.2e1) * np.sqrt((1 - t24)) * ((1 + t24) ** (0.3e1 / 0.2e1)) * np.sin((phi1 + 2 * phi2))

        if Bindx == 20:
            t25 = np.cos(phi)
            tfunc[..., c] = 0.5e1 / 0.4e1 * np.sqrt(0.2e1) * np.cos((2 * phi1 - 2 * phi2)) * (1 + (-2 + t25) * t25)

        if Bindx == 21:
            t26 = np.cos(phi)
            tfunc[..., c] = -0.5e1 / 0.2e1 * np.sqrt(0.2e1) * ((1 - t26) ** (0.3e1 / 0.2e1)) * np.sqrt((1 + t26)) * np.sin((2 * phi1 - phi2))

        if Bindx == 22:
            t27 = np.cos(phi)
            tfunc[..., c] = -0.5e1 / 0.2e1 * np.sqrt(0.3e1) * (t27 ** 2 - 1) * np.cos((2 * phi1))

        if Bindx == 23:
            t28 = np.cos(phi)
            tfunc[..., c] = -0.5e1 / 0.2e1 * np.sqrt(0.2e1) * ((1 + t28) ** (0.3e1 / 0.2e1)) * np.sqrt((1 - t28)) * np.sin((2 * phi1 + phi2))

        if Bindx == 24:
            t29 = np.cos(phi)
            tfunc[..., c] = 0.5e1 / 0.4e1 * np.sqrt(0.2e1) * np.cos((2 * phi1 + 2 * phi2)) * (1 + (2 + t29) * t29)

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

