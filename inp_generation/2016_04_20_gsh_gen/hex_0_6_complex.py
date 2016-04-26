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
                        [4, 4, 1],
                        [6, -6, 1],
                        [6, -6, 2],
                        [6, -5, 1],
                        [6, -5, 2],
                        [6, -4, 1],
                        [6, -4, 2],
                        [6, -3, 1],
                        [6, -3, 2],
                        [6, -2, 1],
                        [6, -2, 2],
                        [6, -1, 1],
                        [6, -1, 2],
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
            tfunc[..., c] = (-0.9e1 / 0.4e1*1j) * np.exp((-1*1j) * phi1) * np.sqrt(0.5e1) * t12 * np.sqrt((1 + t12)) * np.sqrt((1 - t12)) * (7 * t12 ** 2 - 3)

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

        if Bindx == 15:
            t30 = np.sin(phi)
            t27 = t30 ** 2
            t28 = t30 * t27
            tfunc[..., c] = -(0.13e2 / 0.32e2) * np.exp((-6*1j) * phi1) * np.sqrt(0.231e3) * t28 ** 2

        if Bindx == 16:
            t38 = np.cos(phi)
            t45 = -6 * t38
            t37 = t38 ** 2
            t39 = t38 * t37
            t40 = t37 ** 2
            t44 = t40 * t45 - 20 * t39 + t45
            t43 = t39 ** 2 + 15 * t37 + 15 * t40 + 1
            tfunc[..., c] = (0.13e2 / 0.128e3) * np.sqrt(0.2e1) * ((t43 + t44) * np.exp((-6*1j) * (phi1 - phi2)) + (t43 - t44) * np.exp((-6*1j) * (phi1 + phi2)))

        if Bindx == 17:
            t46 = np.cos(phi)
            t47 = t46 ** 2
            tfunc[..., c] = (0.39e2 / 0.16e2*1j) * t46 * (-3 * t47 - 1 + (t47 + 3) * t46) * ((1 + t46) ** (0.5e1 / 0.2e1)) * np.sqrt(0.77e2) * np.exp((-5*1j) * phi1) * ((1 - t46) ** (-0.1e1 / 0.2e1))

        if Bindx == 18:
            t55 = np.cos(phi)
            t54 = t55 ** 2
            t58 = t54 ** 2
            t61 = -1 - 10 * t54 - 5 * t58
            t60 = (10 * t54 + t58 + 5) * t55
            t56 = 5 * phi1
            tfunc[..., c] = (-0.13e2 / 0.64e2*1j) * np.sqrt(0.2e1) * np.sqrt(0.3e1) * np.sqrt((1 - t55)) * np.sqrt((1 + t55)) * ((t60 + t61) * np.exp((-1*1j) * (t56 - 6 * phi2)) + (t60 - t61) * np.exp((-1*1j) * (t56 + 6 * phi2)))

        if Bindx == 19:
            t65 = np.sin(phi)
            t63 = t65 ** 2
            t62 = np.cos(phi)
            tfunc[..., c] = (0.39e2 / 0.32e2) * np.exp((-4*1j) * phi1) * np.sqrt(0.14e2) * t63 ** 2 * (11 * t62 ** 2 - 1)

        if Bindx == 20:
            t72 = np.cos(phi)
            t71 = t72 ** 2
            t74 = t71 ** 2
            t75 = t72 * t74
            t78 = 4 * t72 - 4 * t75
            t77 = t72 * t75 - 5 * t71 + 5 * t74 - 1
            t73 = 2 * phi1
            tfunc[..., c] = (0.13e2 / 0.64e2) * ((t77 + t78) * np.exp((-2*1j) * (t73 - 3 * phi2)) + (t77 - t78) * np.exp((-2*1j) * (t73 + 3 * phi2))) * np.sqrt(0.33e2)

        if Bindx == 21:
            t79 = np.cos(phi)
            tfunc[..., c] = (0.13e2 / 0.16e2*1j) * (11 * t79 ** 2 - 3) * t79 * ((1 + t79) ** (0.3e1 / 0.2e1)) * np.sqrt(0.105e3) * np.exp((-3*1j) * phi1) * ((1 - t79) ** (0.3e1 / 0.2e1))

        if Bindx == 22:
            t86 = np.cos(phi)
            t85 = t86 ** 2
            t92 = 2 * t85
            t88 = t85 ** 2
            t91 = 1 + t92 - 3 * t88
            t90 = (t88 + t92 - 3) * t86
            tfunc[..., c] = (-0.13e2 / 0.64e2*1j) * np.sqrt(0.2e1) * np.sqrt(0.55e2) * np.sqrt((1 - t86)) * np.sqrt((1 + t86)) * ((t90 + t91) * np.exp((-3*1j) * (phi1 - 2 * phi2)) + (t90 - t91) * np.exp((-3*1j) * (phi1 + 2 * phi2)))

        if Bindx == 23:
            t94 = np.cos(phi)
            t95 = t94 ** 2
            t93 = np.sin(phi)
            tfunc[..., c] = -(0.13e2 / 0.32e2) * np.exp((-2*1j) * phi1) * np.sqrt(0.105e3) * t93 ** 2 * (1 + (-18 + 33 * t95) * t95)

        if Bindx == 24:
            t104 = np.cos(phi)
            t103 = t104 ** 2
            t105 = t104 * t103
            t106 = t103 ** 2
            t110 = -2 * t104 * t106 - 2 * t104 + 4 * t105
            t109 = t105 ** 2 - t103 - t106 + 1
            tfunc[..., c] = (0.39e2 / 0.128e3) * np.sqrt(0.2e1) * np.sqrt(0.55e2) * ((t109 + t110) * np.exp((-2*1j) * (phi1 - 3 * phi2)) + (t109 - t110) * np.exp((-2*1j) * (phi1 + 3 * phi2)))

        if Bindx == 25:
            t111 = np.cos(phi)
            t112 = t111 ** 2
            tfunc[..., c] = (-0.13e2 / 0.16e2*1j) * np.exp((-1*1j) * phi1) * np.sqrt(0.42e2) * t111 * np.sqrt((1 + t111)) * np.sqrt((1 - t111)) * (5 + (-30 + 33 * t112) * t112)

        if Bindx == 26:
            t124 = np.cos(phi)
            t123 = t124 ** 2
            t130 = 1 + (-2 + t123) * t123
            t128 = t130 * t124
            tfunc[..., c] = (-0.39e2 / 0.32e2*1j) * np.sqrt(0.11e2) * np.sqrt((1 - t124)) * np.sqrt((1 + t124)) * ((t128 - t130) * np.exp((-1*1j) * (phi1 - 6 * phi2)) + (t128 + t130) * np.exp((-1*1j) * (phi1 + 6 * phi2)))

        if Bindx == 27:
            t131 = np.cos(phi)
            t132 = t131 ** 2
            t133 = t132 ** 2
            tfunc[..., c] = -0.4095e4 / 0.16e2 * t133 - 0.65e2 / 0.16e2 + (0.3003e4 / 0.16e2 * t133 + 0.1365e4 / 0.16e2) * t132

        if Bindx == 28:
            t135 = np.cos(phi)
            t136 = t135 ** 2
            t137 = t136 ** 2
            tfunc[..., c] = 0.13e2 / 0.32e2 * np.sqrt(0.231e3) * np.sqrt(0.2e1) * np.cos((6 * phi2)) * (-3 * t137 - 1 + (t137 + 3) * t136)

        if Bindx == 29:
            t139 = np.cos(phi)
            t140 = t139 ** 2
            tfunc[..., c] = (-0.13e2 / 0.16e2*1j) * np.exp((1j) * phi1) * np.sqrt(0.42e2) * np.sqrt((1 - t139)) * np.sqrt((1 + t139)) * t139 * (5 + (-30 + 33 * t140) * t140)

        if Bindx == 30:
            t148 = np.cos(phi)
            t147 = t148 ** 2
            t154 = 1 + (-2 + t147) * t147
            t152 = t154 * t148
            tfunc[..., c] = (-0.39e2 / 0.32e2*1j) * np.sqrt(0.11e2) * np.sqrt((1 - t148)) * np.sqrt((1 + t148)) * ((t152 - t154) * np.exp((1j) * (phi1 - 6 * phi2)) + (t152 + t154) * np.exp((1j) * (phi1 + 6 * phi2)))

        if Bindx == 31:
            t156 = np.cos(phi)
            t157 = t156 ** 2
            t155 = np.sin(phi)
            tfunc[..., c] = -(0.13e2 / 0.32e2) * np.exp((2*1j) * phi1) * np.sqrt(0.105e3) * t155 ** 2 * (1 + (-18 + 33 * t157) * t157)

        if Bindx == 32:
            t166 = np.cos(phi)
            t165 = t166 ** 2
            t167 = t166 * t165
            t168 = t165 ** 2
            t172 = -2 * t166 * t168 - 2 * t166 + 4 * t167
            t171 = t167 ** 2 - t165 - t168 + 1
            tfunc[..., c] = (0.39e2 / 0.128e3) * np.sqrt(0.2e1) * np.sqrt(0.55e2) * ((t171 + t172) * np.exp((2*1j) * (phi1 - 3 * phi2)) + (t171 - t172) * np.exp((2*1j) * (phi1 + 3 * phi2)))

        if Bindx == 33:
            t173 = np.cos(phi)
            tfunc[..., c] = (0.13e2 / 0.16e2*1j) * np.exp((3*1j) * phi1) * np.sqrt(0.105e3) * ((1 - t173) ** (0.3e1 / 0.2e1)) * ((1 + t173) ** (0.3e1 / 0.2e1)) * t173 * (11 * t173 ** 2 - 3)

        if Bindx == 34:
            t180 = np.cos(phi)
            t179 = t180 ** 2
            t186 = 2 * t179
            t182 = t179 ** 2
            t185 = 1 + t186 - 3 * t182
            t184 = (t182 + t186 - 3) * t180
            tfunc[..., c] = (-0.13e2 / 0.64e2*1j) * np.sqrt(0.2e1) * np.sqrt(0.55e2) * np.sqrt((1 - t180)) * np.sqrt((1 + t180)) * ((t184 + t185) * np.exp((3*1j) * (phi1 - 2 * phi2)) + (t184 - t185) * np.exp((3*1j) * (phi1 + 2 * phi2)))

        if Bindx == 35:
            t190 = np.sin(phi)
            t188 = t190 ** 2
            t187 = np.cos(phi)
            tfunc[..., c] = (0.39e2 / 0.32e2) * np.exp((4*1j) * phi1) * np.sqrt(0.14e2) * t188 ** 2 * (11 * t187 ** 2 - 1)

        if Bindx == 36:
            t197 = np.cos(phi)
            t196 = t197 ** 2
            t199 = t196 ** 2
            t200 = t197 * t199
            t203 = 4 * t197 - 4 * t200
            t202 = t197 * t200 - 5 * t196 + 5 * t199 - 1
            t198 = 2 * phi1
            tfunc[..., c] = (0.13e2 / 0.64e2) * ((t202 + t203) * np.exp((2*1j) * (t198 - 3 * phi2)) + (t202 - t203) * np.exp((2*1j) * (t198 + 3 * phi2))) * np.sqrt(0.33e2)

        if Bindx == 37:
            t204 = np.cos(phi)
            tfunc[..., c] = (-0.39e2 / 0.16e2*1j) * np.exp((5*1j) * phi1) * np.sqrt(0.77e2) * ((1 - t204) ** (0.5e1 / 0.2e1)) * ((1 + t204) ** (0.5e1 / 0.2e1)) * t204

        if Bindx == 38:
            t211 = np.cos(phi)
            t210 = t211 ** 2
            t214 = t210 ** 2
            t217 = -1 - 10 * t210 - 5 * t214
            t216 = (10 * t210 + t214 + 5) * t211
            t212 = 5 * phi1
            tfunc[..., c] = (-0.13e2 / 0.64e2*1j) * np.sqrt(0.2e1) * np.sqrt(0.3e1) * np.sqrt((1 - t211)) * np.sqrt((1 + t211)) * ((t216 + t217) * np.exp((1j) * (t212 - 6 * phi2)) + (t216 - t217) * np.exp((1j) * (t212 + 6 * phi2)))

        if Bindx == 39:
            t221 = np.sin(phi)
            t218 = t221 ** 2
            t219 = t221 * t218
            tfunc[..., c] = -(0.13e2 / 0.32e2) * np.exp((6*1j) * phi1) * np.sqrt(0.231e3) * t219 ** 2

        if Bindx == 40:
            t229 = np.cos(phi)
            t236 = -6 * t229
            t228 = t229 ** 2
            t230 = t229 * t228
            t231 = t228 ** 2
            t235 = t231 * t236 - 20 * t230 + t236
            t234 = t230 ** 2 + 15 * t228 + 15 * t231 + 1
            tfunc[..., c] = (0.13e2 / 0.128e3) * np.sqrt(0.2e1) * ((t234 + t235) * np.exp((6*1j) * (phi1 - phi2)) + (t234 - t235) * np.exp((6*1j) * (phi1 + phi2)))
	
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

