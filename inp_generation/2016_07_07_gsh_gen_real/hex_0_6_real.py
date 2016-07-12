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
            tfunc[..., c] = -0.13e2 / 0.16e2 * np.sqrt(0.231e3) * np.cos((6 * phi2)) * (-3 * t22 - 1 + (t22 + 3) * t21)

        if Bindx == 10:
            t24 = np.cos(phi)
            t25 = t24 ** 2
            t26 = t25 ** 2
            tfunc[..., c] = -0.4095e4 / 0.16e2 * t26 - 0.65e2 / 0.16e2 + (0.3003e4 / 0.16e2 * t26 + 0.1365e4 / 0.16e2) * t25

        if Bindx == 11:
            t34 = np.cos(phi)
            t33 = t34 ** 2
            t40 = 1 + (-2 + t33) * t33
            t38 = t40 * t34
            tfunc[..., c] = 0.39e2 / 0.32e2 * np.sqrt(0.22e2) * np.sqrt((1 - t34)) * np.sqrt((1 + t34)) * ((t38 - t40) * np.sin((phi1 - 6 * phi2)) + (t38 + t40) * np.sin((phi1 + 6 * phi2)))

        if Bindx == 12:
            t42 = np.cos(phi)
            t43 = t42 ** 2
            t41 = np.sin(phi)
            tfunc[..., c] = -0.13e2 / 0.8e1 * np.sqrt(0.21e2) * t42 * t41 ** 2 * (5 + (-30 + 33 * t43) * t43) * np.sin(phi1) * ((1 + t42) ** (-0.1e1 / 0.2e1)) * ((1 - t42) ** (-0.1e1 / 0.2e1))

        if Bindx == 13:
            t52 = np.cos(phi)
            t51 = t52 ** 2
            t54 = t52 * t51
            t55 = t51 ** 2
            t59 = -2 * t52 * t55 - 2 * t52 + 4 * t54
            t58 = t54 ** 2 - t51 - t55 + 1
            t53 = 2 * phi1
            tfunc[..., c] = 0.39e2 / 0.64e2 * np.sqrt(0.55e2) * ((t58 + t59) * np.cos((-t53 + 6 * phi2)) + (t58 - t59) * np.cos((t53 + 6 * phi2)))

        if Bindx == 14:
            t60 = np.cos(phi)
            t61 = t60 ** 2
            t62 = t61 ** 2
            tfunc[..., c] = -0.13e2 / 0.32e2 * np.sqrt(0.2e1) * np.sqrt(0.105e3) * (-51 * t62 - 1 + (33 * t62 + 19) * t61) * np.cos((2 * phi1))

        if Bindx == 15:
            t70 = np.cos(phi)
            t69 = t70 ** 2
            t77 = 2 * t69
            t73 = t69 ** 2
            t76 = 1 + t77 - 3 * t73
            t75 = (t73 + t77 - 3) * t70
            t71 = 3 * phi1
            tfunc[..., c] = -0.13e2 / 0.32e2 * np.sqrt(0.55e2) * np.sqrt((1 - t70)) * np.sqrt((1 + t70)) * (-(t75 + t76) * np.sin((-t71 + 6 * phi2)) + (t75 - t76) * np.sin((t71 + 6 * phi2)))

        if Bindx == 16:
            t81 = np.sin(phi)
            t79 = t81 ** 2
            t78 = np.cos(phi)
            tfunc[..., c] = -0.13e2 / 0.16e2 * np.sqrt(0.2e1) * np.sqrt(0.105e3) * t78 * t79 ** 2 * (11 * t78 ** 2 - 3) * np.sin((3 * phi1)) * ((1 + t78) ** (-0.1e1 / 0.2e1)) * ((1 - t78) ** (-0.1e1 / 0.2e1))

        if Bindx == 17:
            t88 = np.cos(phi)
            t87 = t88 ** 2
            t90 = t87 ** 2
            t91 = t88 * t90
            t94 = 4 * t88 - 4 * t91
            t93 = t88 * t91 - 5 * t87 + 5 * t90 - 1
            t89 = 4 * phi1
            tfunc[..., c] = -0.13e2 / 0.64e2 * np.sqrt(0.66e2) * ((t93 + t94) * np.cos((-t89 + 6 * phi2)) + (t93 - t94) * np.cos((t89 + 6 * phi2)))

        if Bindx == 18:
            t95 = np.cos(phi)
            t96 = t95 ** 2
            t97 = t96 ** 2
            tfunc[..., c] = 0.39e2 / 0.16e2 * np.sqrt(0.7e1) * (-23 * t97 - 1 + (11 * t97 + 13) * t96) * np.cos((4 * phi1))

        if Bindx == 19:
            t105 = np.cos(phi)
            t104 = t105 ** 2
            t108 = t104 ** 2
            t111 = -1 - 10 * t104 - 5 * t108
            t110 = (10 * t104 + t108 + 5) * t105
            t106 = 5 * phi1
            tfunc[..., c] = 0.13e2 / 0.32e2 * np.sqrt(0.3e1) * np.sqrt((1 + t105)) * np.sqrt((1 - t105)) * ((t110 - t111) * np.sin((t106 + 6 * phi2)) - (t110 + t111) * np.sin((-t106 + 6 * phi2)))

        if Bindx == 20:
            t116 = np.sin(phi)
            t113 = t116 ** 2
            t114 = t116 * t113
            t112 = np.cos(phi)
            tfunc[..., c] = -0.39e2 / 0.16e2 * np.sqrt(0.2e1) * np.sqrt(0.77e2) * t112 * t114 ** 2 * np.sin((5 * phi1)) * ((1 + t112) ** (-0.1e1 / 0.2e1)) * ((1 - t112) ** (-0.1e1 / 0.2e1))

        if Bindx == 21:
            t124 = np.cos(phi)
            t131 = -0.39e2 / 0.32e2 * t124
            t123 = t124 ** 2
            t125 = t124 * t123
            t126 = t123 ** 2
            t130 = -0.65e2 / 0.16e2 * t125 + t126 * t131 + t131
            t129 = 0.13e2 / 0.64e2 * t125 ** 2 + 0.13e2 / 0.64e2 + 0.195e3 / 0.64e2 * t126 + 0.195e3 / 0.64e2 * t123
            tfunc[..., c] = (t129 + t130) * np.cos((6 * phi1 - 6 * phi2)) + (t129 - t130) * np.cos((6 * phi1 + 6 * phi2))

        if Bindx == 22:
            t132 = np.cos(phi)
            t133 = t132 ** 2
            t134 = t133 ** 2
            tfunc[..., c] = -0.13e2 / 0.32e2 * np.sqrt(0.2e1) * np.sqrt(0.231e3) * np.cos((6 * phi1)) * (-3 * t134 - 1 + (t134 + 3) * t133)

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

