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
            t98 = np.cos(phi)
            t97 = t98 ** 2
            t102 = 4 * (-t97 - 1) * t98
            t95 = t97 ** 2
            t101 = 1 + t95 + 6 * t97
            tfunc[..., c] = (0.3e1 / 0.64e2) * np.sqrt(0.3e1) * np.sqrt(0.5e1) * np.sqrt(0.2e1) * ((14 * t95 - 28 * t97 + 14) * np.exp((-4*1j) * phi2) + (t101 - t102) * np.exp((-4*1j) * (phi1 + phi2)) + (t101 + t102) * np.exp((4*1j) * (phi1 - phi2)))

        if Bindx == 2:
            t110 = 4 * phi1
            t109 = np.cos(phi)
            t108 = t109 ** 2
            t107 = t109 * t108
            t106 = t108 ** 2
            tfunc[..., c] = (0.3e1 / 0.16e2*1j) * np.sqrt(0.5e1) * np.sqrt(0.3e1) * np.sqrt((1 + t109)) * ((1 - t109) ** (-0.1e1 / 0.2e1)) * ((t106 + 2 * t107 - 2 * t109 - 1) * np.exp((-1*1j) * (t110 + 3 * phi2)) + 14 * (t106 - t107 - t108 + t109) * np.exp((-3*1j) * phi2) + (t106 - 4 * t107 + 6 * t108 - 4 * t109 + 1) * np.exp((1j) * (t110 - 3 * phi2)))

        if Bindx == 3:
            t118 = np.cos(phi)
            t120 = t118 ** 2
            t116 = t120 ** 2
            t124 = -1 + t116
            t123 = 2 * (-t120 + 1) * t118
            t119 = 2 * phi1
            tfunc[..., c] = (0.3e1 / 0.32e2) * np.sqrt(0.2e1) * np.sqrt(0.5e1) * np.sqrt(0.21e2) * ((14 * t116 - 16 * t120 + 2) * np.exp((-2*1j) * phi2) + (-t123 + t124) * np.exp((-2*1j) * (t119 + phi2)) + (t123 + t124) * np.exp((2*1j) * (t119 - phi2)))

        if Bindx == 4:
            t132 = 4 * phi1
            t131 = np.cos(phi)
            t130 = t131 ** 2
            t129 = t131 * t130
            t128 = t130 ** 2
            tfunc[..., c] = (0.3e1 / 0.16e2*1j) * np.sqrt((1 + t131)) * np.sqrt(0.7e1) * np.sqrt(0.3e1) * np.sqrt(0.5e1) * ((1 - t131) ** (-0.1e1 / 0.2e1)) * ((t128 - 2 * t130 + 1) * np.exp((-1*1j) * (t132 + phi2)) + (t128 - 2 * t129 + 2 * t131 - 1) * np.exp((1j) * (t132 - phi2)) + (14 * t128 - 14 * t129 - 6 * t130 + 6 * t131) * np.exp((-1*1j) * phi2))

        if Bindx == 5:
            t138 = np.cos(phi)
            t137 = t138 ** 2
            t136 = t137 ** 2
            tfunc[..., c] = 0.3e1 / 0.16e2 * np.sqrt(0.7e1) * np.sqrt(0.3e1) * ((35 * t136) - (30 * t137) + 0.3e1 + (5 * t136 - 10 * t137 + 5) * np.cos((4 * phi1)))

        if Bindx == 6:
            t147 = 4 * phi1
            t146 = np.cos(phi)
            t145 = t146 ** 2
            t144 = t146 * t145
            t143 = t145 ** 2
            tfunc[..., c] = (-0.3e1 / 0.16e2*1j) * np.sqrt((1 - t146)) * np.sqrt(0.7e1) * np.sqrt(0.3e1) * np.sqrt(0.5e1) * ((1 + t146) ** (-0.1e1 / 0.2e1)) * ((t143 - 2 * t145 + 1) * np.exp((-1*1j) * (t147 - phi2)) + (t143 + 2 * t144 - 2 * t146 - 1) * np.exp((1j) * (t147 + phi2)) + (14 * t143 + 14 * t144 - 6 * t145 - 6 * t146) * np.exp((1j) * phi2))

        if Bindx == 7:
            t155 = np.cos(phi)
            t157 = t155 ** 2
            t153 = t157 ** 2
            t161 = -1 + t153
            t160 = 2 * (-t157 + 1) * t155
            t156 = 2 * phi1
            tfunc[..., c] = (0.3e1 / 0.32e2) * np.sqrt(0.2e1) * np.sqrt(0.5e1) * np.sqrt(0.21e2) * ((14 * t153 - 16 * t157 + 2) * np.exp((2*1j) * phi2) + (t160 + t161) * np.exp((-2*1j) * (t156 - phi2)) + (-t160 + t161) * np.exp((2*1j) * (t156 + phi2)))

        if Bindx == 8:
            t169 = 4 * phi1
            t168 = np.cos(phi)
            t167 = t168 ** 2
            t166 = t168 * t167
            t165 = t167 ** 2
            tfunc[..., c] = (-0.3e1 / 0.16e2*1j) * np.sqrt(0.5e1) * np.sqrt(0.3e1) * np.sqrt((1 - t168)) * ((1 + t168) ** (-0.1e1 / 0.2e1)) * ((t165 - 2 * t166 + 2 * t168 - 1) * np.exp((-1*1j) * (t169 - 3 * phi2)) + 14 * (t165 + t166 - t167 - t168) * np.exp((3*1j) * phi2) + (t165 + 4 * t166 + 6 * t167 + 4 * t168 + 1) * np.exp((1j) * (t169 + 3 * phi2)))

        if Bindx == 9:
            t178 = np.cos(phi)
            t177 = t178 ** 2
            t182 = 4 * (-t177 - 1) * t178
            t175 = t177 ** 2
            t181 = 1 + t175 + 6 * t177
            tfunc[..., c] = (0.3e1 / 0.64e2) * np.sqrt(0.3e1) * np.sqrt(0.5e1) * np.sqrt(0.2e1) * ((14 * t175 - 28 * t177 + 14) * np.exp((4*1j) * phi2) + (t181 + t182) * np.exp((-4*1j) * (phi1 - phi2)) + (t181 - t182) * np.exp((4*1j) * (phi1 + phi2)))

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

