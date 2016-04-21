import numpy as np


def gsh_basis_info():

    indxvec = np.array([[0, 0, 1],
                        [2, 0, 1],
                        [2, 1, 1],
                        [2, 2, 1],
                        [4, 0, 1],
                        [4, 1, 1],
                        [4, 2, 1],
                        [4, 3, 1],
                        [4, 4, 1],
                        [6, 0, 1],
                        [6, 1, 1],
                        [6, 2, 1],
                        [6, 3, 1],
                        [6, 4, 1],
                        [6, 5, 1],
                        [6, 6, 1]])

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
            tfunc[..., c] = 0.15e2 / 0.2e1 * t1 ** 2 - 0.5e1 / 0.2e1

        if Bindx == 2:
            t3 = np.cos(phi)
            t2 = np.sin(phi)
            tfunc[..., c] = -0.5e1 * np.sqrt(0.3e1) * t3 * t2 ** 2 * np.sin(phi1) * ((1 - t3) ** (-0.1e1 / 0.2e1)) * ((1 + t3) ** (-0.1e1 / 0.2e1))

        if Bindx == 3:
            t4 = np.cos(phi)
            tfunc[..., c] = -0.5e1 / 0.2e1 * np.sqrt(0.3e1) * (t4 ** 2 - 1) * np.cos((2 * phi1))

        if Bindx == 4:
            t5 = np.cos(phi)
            t6 = t5 ** 2
            tfunc[..., c] = 0.27e2 / 0.8e1 + (-0.135e3 / 0.4e1 + 0.315e3 / 0.8e1 * t6) * t6

        if Bindx == 5:
            t9 = np.cos(phi)
            t8 = np.sin(phi)
            tfunc[..., c] = -0.9e1 / 0.4e1 * np.sqrt(0.2e1) * np.sqrt(0.5e1) * t9 * t8 ** 2 * (7 * t9 ** 2 - 3) * np.sin(phi1) * ((1 + t9) ** (-0.1e1 / 0.2e1)) * ((1 - t9) ** (-0.1e1 / 0.2e1))

        if Bindx == 6:
            t10 = np.cos(phi)
            t11 = t10 ** 2
            tfunc[..., c] = -0.9e1 / 0.4e1 * np.sqrt(0.5e1) * (1 + (-8 + 7 * t11) * t11) * np.cos((2 * phi1))

        if Bindx == 7:
            t16 = np.sin(phi)
            t14 = t16 ** 2
            t13 = np.cos(phi)
            tfunc[..., c] = -0.9e1 / 0.4e1 * np.sqrt(0.2e1) * np.sqrt(0.35e2) * t13 * t14 ** 2 * np.sin((3 * phi1)) * ((1 + t13) ** (-0.1e1 / 0.2e1)) * ((1 - t13) ** (-0.1e1 / 0.2e1))

        if Bindx == 8:
            t17 = np.cos(phi)
            t18 = t17 ** 2
            tfunc[..., c] = 0.9e1 / 0.8e1 * np.sqrt(0.35e2) * np.cos((4 * phi1)) * (1 + (-2 + t18) * t18)

        if Bindx == 9:
            t20 = np.cos(phi)
            t21 = t20 ** 2
            t22 = t21 ** 2
            tfunc[..., c] = -0.4095e4 / 0.16e2 * t22 - 0.65e2 / 0.16e2 + (0.3003e4 / 0.16e2 * t22 + 0.1365e4 / 0.16e2) * t21

        if Bindx == 10:
            t25 = np.cos(phi)
            t26 = t25 ** 2
            t24 = np.sin(phi)
            tfunc[..., c] = -0.13e2 / 0.8e1 * np.sqrt(0.21e2) * t25 * t24 ** 2 * (5 + (-30 + 33 * t26) * t26) * np.sin(phi1) * ((1 + t25) ** (-0.1e1 / 0.2e1)) * ((1 - t25) ** (-0.1e1 / 0.2e1))

        if Bindx == 11:
            t28 = np.cos(phi)
            t29 = t28 ** 2
            t30 = t29 ** 2
            tfunc[..., c] = -0.13e2 / 0.32e2 * np.sqrt(0.2e1) * np.sqrt(0.105e3) * (-51 * t30 - 1 + (33 * t30 + 19) * t29) * np.cos((2 * phi1))

        if Bindx == 12:
            t35 = np.sin(phi)
            t33 = t35 ** 2
            t32 = np.cos(phi)
            tfunc[..., c] = -0.13e2 / 0.16e2 * np.sqrt(0.2e1) * np.sqrt(0.105e3) * t32 * t33 ** 2 * (11 * t32 ** 2 - 3) * np.sin((3 * phi1)) * ((1 + t32) ** (-0.1e1 / 0.2e1)) * ((1 - t32) ** (-0.1e1 / 0.2e1))

        if Bindx == 13:
            t36 = np.cos(phi)
            t37 = t36 ** 2
            t38 = t37 ** 2
            tfunc[..., c] = 0.39e2 / 0.16e2 * np.sqrt(0.7e1) * (-23 * t38 - 1 + (11 * t38 + 13) * t37) * np.cos((4 * phi1))

        if Bindx == 14:
            t44 = np.sin(phi)
            t41 = t44 ** 2
            t42 = t44 * t41
            t40 = np.cos(phi)
            tfunc[..., c] = -0.39e2 / 0.16e2 * np.sqrt(0.2e1) * np.sqrt(0.77e2) * t40 * t42 ** 2 * np.sin((5 * phi1)) * ((1 + t40) ** (-0.1e1 / 0.2e1)) * ((1 - t40) ** (-0.1e1 / 0.2e1))

        if Bindx == 15:
            t45 = np.cos(phi)
            t46 = t45 ** 2
            t47 = t46 ** 2
            tfunc[..., c] = -0.13e2 / 0.32e2 * np.sqrt(0.2e1) * np.sqrt(0.231e3) * np.cos((6 * phi1)) * (-3 * t47 - 1 + (t47 + 3) * t46)
	
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

