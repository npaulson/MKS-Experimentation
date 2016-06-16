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
                        [6, 0, 2],
                        [6, 1, 1],
                        [6, 1, 2],
                        [6, 2, 1],
                        [6, 2, 2],
                        [6, 3, 1],
                        [6, 3, 2],
                        [6, 4, 1],
                        [6, 4, 2],
                        [6, 5, 1],
                        [6, 5, 2],
                        [6, 6, 1],
                        [6, 6, 2]])

    return indxvec


def gsh_eval(X, Bvec):

    phi1 = X[..., 0]
    phi = X[..., 1]
    phi2 = X[..., 2]

    zvec = np.abs(phi) < 5e-8
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
            tfunc[..., c] = -0.5e1 * np.sqrt(0.3e1) * t3 * t2 ** 2 * np.sin(phi1) * ((1 + t3) ** (-0.1e1 / 0.2e1)) * ((1 - t3) ** (-0.1e1 / 0.2e1))

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
            t24 = np.cos(phi)
            t25 = t24 ** 2
            t26 = t25 ** 2
            tfunc[..., c] = -0.13e2 / 0.16e2 * np.sqrt(0.231e3) * np.cos((6 * phi2)) * (-3 * t26 - 1 + (t26 + 3) * t25)

        if Bindx == 11:
            t29 = np.cos(phi)
            t30 = t29 ** 2
            t28 = np.sin(phi)
            tfunc[..., c] = -0.13e2 / 0.8e1 * np.sqrt(0.21e2) * t29 * t28 ** 2 * (5 + (-30 + 33 * t30) * t30) * np.sin(phi1) * ((1 + t29) ** (-0.1e1 / 0.2e1)) * ((1 - t29) ** (-0.1e1 / 0.2e1))

        if Bindx == 12:
            t38 = np.cos(phi)
            t37 = t38 ** 2
            t44 = 1 + (-2 + t37) * t37
            t42 = t44 * t38
            tfunc[..., c] = 0.39e2 / 0.32e2 * np.sqrt(0.22e2) * np.sqrt((1 + t38)) * np.sqrt((1 - t38)) * ((t42 - t44) * np.sin((phi1 - 6 * phi2)) + (t42 + t44) * np.sin((phi1 + 6 * phi2)))

        if Bindx == 13:
            t45 = np.cos(phi)
            t46 = t45 ** 2
            t47 = t46 ** 2
            tfunc[..., c] = -0.13e2 / 0.32e2 * np.sqrt(0.2e1) * np.sqrt(0.105e3) * (-51 * t47 - 1 + (33 * t47 + 19) * t46) * np.cos((2 * phi1))

        if Bindx == 14:
            t56 = np.cos(phi)
            t55 = t56 ** 2
            t58 = t56 * t55
            t59 = t55 ** 2
            t63 = -2 * t56 * t59 - 2 * t56 + 4 * t58
            t62 = t58 ** 2 - t55 - t59 + 1
            t57 = 2 * phi1
            tfunc[..., c] = 0.39e2 / 0.64e2 * np.sqrt(0.55e2) * ((t62 + t63) * np.cos((-t57 + 6 * phi2)) + (t62 - t63) * np.cos((t57 + 6 * phi2)))

        if Bindx == 15:
            t67 = np.sin(phi)
            t65 = t67 ** 2
            t64 = np.cos(phi)
            tfunc[..., c] = -0.13e2 / 0.16e2 * np.sqrt(0.2e1) * np.sqrt(0.105e3) * t64 * t65 ** 2 * (11 * t64 ** 2 - 3) * np.sin((3 * phi1)) * ((1 + t64) ** (-0.1e1 / 0.2e1)) * ((1 - t64) ** (-0.1e1 / 0.2e1))

        if Bindx == 16:
            t74 = np.cos(phi)
            t73 = t74 ** 2
            t81 = 2 * t73
            t77 = t73 ** 2
            t80 = 1 + t81 - 3 * t77
            t79 = (t77 + t81 - 3) * t74
            t75 = 3 * phi1
            tfunc[..., c] = -0.13e2 / 0.32e2 * np.sqrt(0.55e2) * np.sqrt((1 - t74)) * np.sqrt((1 + t74)) * (-(t79 + t80) * np.sin((-t75 + 6 * phi2)) + (t79 - t80) * np.sin((t75 + 6 * phi2)))

        if Bindx == 17:
            t82 = np.cos(phi)
            t83 = t82 ** 2
            t84 = t83 ** 2
            tfunc[..., c] = 0.39e2 / 0.16e2 * np.sqrt(0.7e1) * (-23 * t84 - 1 + (11 * t84 + 13) * t83) * np.cos((4 * phi1))

        if Bindx == 18:
            t92 = np.cos(phi)
            t91 = t92 ** 2
            t94 = t91 ** 2
            t95 = t92 * t94
            t98 = 4 * t92 - 4 * t95
            t97 = t92 * t95 - 5 * t91 + 5 * t94 - 1
            t93 = 4 * phi1
            tfunc[..., c] = -0.13e2 / 0.64e2 * np.sqrt(0.66e2) * ((t97 + t98) * np.cos((-t93 + 6 * phi2)) + (t97 - t98) * np.cos((t93 + 6 * phi2)))

        if Bindx == 19:
            t103 = np.sin(phi)
            t100 = t103 ** 2
            t101 = t103 * t100
            t99 = np.cos(phi)
            tfunc[..., c] = -0.39e2 / 0.16e2 * np.sqrt(0.2e1) * np.sqrt(0.77e2) * t99 * t101 ** 2 * np.sin((5 * phi1)) * ((1 + t99) ** (-0.1e1 / 0.2e1)) * ((1 - t99) ** (-0.1e1 / 0.2e1))

        if Bindx == 20:
            t110 = np.cos(phi)
            t109 = t110 ** 2
            t113 = t109 ** 2
            t116 = -1 - 10 * t109 - 5 * t113
            t115 = (10 * t109 + t113 + 5) * t110
            t111 = 5 * phi1
            tfunc[..., c] = 0.13e2 / 0.32e2 * np.sqrt(0.3e1) * np.sqrt((1 - t110)) * np.sqrt((1 + t110)) * (-(t115 + t116) * np.sin((-t111 + 6 * phi2)) + (t115 - t116) * np.sin((t111 + 6 * phi2)))

        if Bindx == 21:
            t117 = np.cos(phi)
            t118 = t117 ** 2
            t119 = t118 ** 2
            tfunc[..., c] = -0.13e2 / 0.32e2 * np.sqrt(0.2e1) * np.sqrt(0.231e3) * np.cos((6 * phi1)) * (-3 * t119 - 1 + (t119 + 3) * t118)

        if Bindx == 22:
            t128 = np.cos(phi)
            t135 = -0.39e2 / 0.32e2 * t128
            t127 = t128 ** 2
            t129 = t128 * t127
            t130 = t127 ** 2
            t134 = -0.65e2 / 0.16e2 * t129 + t130 * t135 + t135
            t133 = 0.13e2 / 0.64e2 * t129 ** 2 + 0.13e2 / 0.64e2 + 0.195e3 / 0.64e2 * t130 + 0.195e3 / 0.64e2 * t127
            tfunc[..., c] = (t133 + t134) * np.cos((6 * phi1 - 6 * phi2)) + (t133 - t134) * np.cos((6 * phi1 + 6 * phi2))

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

