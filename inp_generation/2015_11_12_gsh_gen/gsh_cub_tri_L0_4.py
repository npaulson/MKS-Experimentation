import numpy as np


def gsh_basis_info():

    indxvec = np.array([[0, 0, 1],
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
            t7 = np.cos(phi)
            t6 = t7 ** 2
            t11 = 4 * (-t6 - 1) * t7
            t4 = t6 ** 2
            t10 = 1 + t4 + 6 * t6
            tfunc[..., c] = (0.3e1 / 0.64e2) * np.sqrt(0.3e1) * np.sqrt(0.5e1) * np.sqrt(0.2e1) * ((14 * t4 - 28 * t6 + 14) * np.exp((-4*1j) * phi2) + (t10 - t11) * np.exp((-4*1j) * (phi1 + phi2)) + (t10 + t11) * np.exp((4*1j) * (phi1 - phi2)))

        if Bindx == 2:
            t19 = 4 * phi1
            t18 = np.cos(phi)
            t17 = t18 ** 2
            t16 = t18 * t17
            t15 = t17 ** 2
            tfunc[..., c] = (0.3e1 / 0.16e2*1j) * np.sqrt(0.5e1) * np.sqrt(0.3e1) * np.sqrt((1 + t18)) * ((1 - t18) ** (-0.1e1 / 0.2e1)) * ((t15 + 2 * t16 - 2 * t18 - 1) * np.exp((-1*1j) * (t19 + 3 * phi2)) + 14 * (t15 - t16 - t17 + t18) * np.exp((-3*1j) * phi2) + (t15 - 4 * t16 + 6 * t17 - 4 * t18 + 1) * np.exp((1j) * (t19 - 3 * phi2)))

        if Bindx == 3:
            t27 = np.cos(phi)
            t29 = t27 ** 2
            t25 = t29 ** 2
            t33 = -1 + t25
            t32 = 2 * (-t29 + 1) * t27
            t28 = 2 * phi1
            tfunc[..., c] = (0.3e1 / 0.32e2) * np.sqrt(0.2e1) * np.sqrt(0.5e1) * np.sqrt(0.21e2) * ((14 * t25 - 16 * t29 + 2) * np.exp((-2*1j) * phi2) + (-t32 + t33) * np.exp((-2*1j) * (t28 + phi2)) + (t32 + t33) * np.exp((2*1j) * (t28 - phi2)))

        if Bindx == 4:
            t41 = 4 * phi1
            t40 = np.cos(phi)
            t39 = t40 ** 2
            t38 = t40 * t39
            t37 = t39 ** 2
            tfunc[..., c] = (0.3e1 / 0.16e2*1j) * np.sqrt((1 + t40)) * np.sqrt(0.7e1) * np.sqrt(0.3e1) * np.sqrt(0.5e1) * ((1 - t40) ** (-0.1e1 / 0.2e1)) * ((t37 - 2 * t39 + 1) * np.exp((-1*1j) * (t41 + phi2)) + (t37 - 2 * t38 + 2 * t40 - 1) * np.exp((1j) * (t41 - phi2)) + (14 * t37 - 14 * t38 - 6 * t39 + 6 * t40) * np.exp((-1*1j) * phi2))

        if Bindx == 5:
            t47 = np.cos(phi)
            t46 = t47 ** 2
            t45 = t46 ** 2
            tfunc[..., c] = 0.3e1 / 0.16e2 * np.sqrt(0.7e1) * np.sqrt(0.3e1) * ((35 * t45) - (30 * t46) + 0.3e1 + (5 * t45 - 10 * t46 + 5) * np.cos((4 * phi1)))

        if Bindx == 6:
            t56 = 4 * phi1
            t55 = np.cos(phi)
            t54 = t55 ** 2
            t53 = t55 * t54
            t52 = t54 ** 2
            tfunc[..., c] = (-0.3e1 / 0.16e2*1j) * np.sqrt((1 - t55)) * np.sqrt(0.7e1) * np.sqrt(0.3e1) * np.sqrt(0.5e1) * ((1 + t55) ** (-0.1e1 / 0.2e1)) * ((t52 - 2 * t54 + 1) * np.exp((-1*1j) * (t56 - phi2)) + (t52 + 2 * t53 - 2 * t55 - 1) * np.exp((1j) * (t56 + phi2)) + (14 * t52 + 14 * t53 - 6 * t54 - 6 * t55) * np.exp((1j) * phi2))

        if Bindx == 7:
            t64 = np.cos(phi)
            t66 = t64 ** 2
            t62 = t66 ** 2
            t70 = -1 + t62
            t69 = 2 * (-t66 + 1) * t64
            t65 = 2 * phi1
            tfunc[..., c] = (0.3e1 / 0.32e2) * np.sqrt(0.2e1) * np.sqrt(0.5e1) * np.sqrt(0.21e2) * ((14 * t62 - 16 * t66 + 2) * np.exp((2*1j) * phi2) + (t69 + t70) * np.exp((-2*1j) * (t65 - phi2)) + (-t69 + t70) * np.exp((2*1j) * (t65 + phi2)))

        if Bindx == 8:
            t78 = 4 * phi1
            t77 = np.cos(phi)
            t76 = t77 ** 2
            t75 = t77 * t76
            t74 = t76 ** 2
            tfunc[..., c] = (-0.3e1 / 0.16e2*1j) * np.sqrt(0.5e1) * np.sqrt(0.3e1) * np.sqrt((1 - t77)) * ((1 + t77) ** (-0.1e1 / 0.2e1)) * ((t74 - 2 * t75 + 2 * t77 - 1) * np.exp((-1*1j) * (t78 - 3 * phi2)) + 14 * (t74 + t75 - t76 - t77) * np.exp((3*1j) * phi2) + (t74 + 4 * t75 + 6 * t76 + 4 * t77 + 1) * np.exp((1j) * (t78 + 3 * phi2)))

        if Bindx == 9:
            t87 = np.cos(phi)
            t86 = t87 ** 2
            t91 = 4 * (-t86 - 1) * t87
            t84 = t86 ** 2
            t90 = 1 + t84 + 6 * t86
            tfunc[..., c] = (0.3e1 / 0.64e2) * np.sqrt(0.3e1) * np.sqrt(0.5e1) * np.sqrt(0.2e1) * ((14 * t84 - 28 * t86 + 14) * np.exp((4*1j) * phi2) + (t90 + t91) * np.exp((-4*1j) * (phi1 - phi2)) + (t90 - t91) * np.exp((4*1j) * (phi1 + phi2)))

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

