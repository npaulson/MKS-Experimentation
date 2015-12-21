import numpy as np


def gsh_basis_info():

    indxvec = np.array([[0, 0, 0],
                        [1, -1, -1],
                        [1, -1, 0],
                        [1, -1, 1],
                        [1, 0, -1],
                        [1, 0, 0],
                        [1, 0, 1],
                        [1, 1, -1],
                        [1, 1, 0],
                        [1, 1, 1],
                        [2, -2, -2],
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
                        [2, 2, 2],
                        [3, -3, -3],
                        [3, -3, -2],
                        [3, -3, -1],
                        [3, -3, 0],
                        [3, -3, 1],
                        [3, -3, 2],
                        [3, -3, 3],
                        [3, -2, -3],
                        [3, -2, -2],
                        [3, -2, -1],
                        [3, -2, 0],
                        [3, -2, 1],
                        [3, -2, 2],
                        [3, -2, 3],
                        [3, -1, -3],
                        [3, -1, -2],
                        [3, -1, -1],
                        [3, -1, 0],
                        [3, -1, 1],
                        [3, -1, 2],
                        [3, -1, 3],
                        [3, 0, -3],
                        [3, 0, -2],
                        [3, 0, -1],
                        [3, 0, 0],
                        [3, 0, 1],
                        [3, 0, 2],
                        [3, 0, 3],
                        [3, 1, -3],
                        [3, 1, -2],
                        [3, 1, -1],
                        [3, 1, 0],
                        [3, 1, 1],
                        [3, 1, 2],
                        [3, 1, 3],
                        [3, 2, -3],
                        [3, 2, -2],
                        [3, 2, -1],
                        [3, 2, 0],
                        [3, 2, 1],
                        [3, 2, 2],
                        [3, 2, 3],
                        [3, 3, -3],
                        [3, 3, -2],
                        [3, 3, -1],
                        [3, 3, 0],
                        [3, 3, 1],
                        [3, 3, 2],
                        [3, 3, 3],
                        [4, -4, -4],
                        [4, -4, -3],
                        [4, -4, -2],
                        [4, -4, -1],
                        [4, -4, 0],
                        [4, -4, 1],
                        [4, -4, 2],
                        [4, -4, 3],
                        [4, -4, 4],
                        [4, -3, -4],
                        [4, -3, -3],
                        [4, -3, -2],
                        [4, -3, -1],
                        [4, -3, 0],
                        [4, -3, 1],
                        [4, -3, 2],
                        [4, -3, 3],
                        [4, -3, 4],
                        [4, -2, -4],
                        [4, -2, -3],
                        [4, -2, -2],
                        [4, -2, -1],
                        [4, -2, 0],
                        [4, -2, 1],
                        [4, -2, 2],
                        [4, -2, 3],
                        [4, -2, 4],
                        [4, -1, -4],
                        [4, -1, -3],
                        [4, -1, -2],
                        [4, -1, -1],
                        [4, -1, 0],
                        [4, -1, 1],
                        [4, -1, 2],
                        [4, -1, 3],
                        [4, -1, 4],
                        [4, 0, -4],
                        [4, 0, -3],
                        [4, 0, -2],
                        [4, 0, -1],
                        [4, 0, 0],
                        [4, 0, 1],
                        [4, 0, 2],
                        [4, 0, 3],
                        [4, 0, 4],
                        [4, 1, -4],
                        [4, 1, -3],
                        [4, 1, -2],
                        [4, 1, -1],
                        [4, 1, 0],
                        [4, 1, 1],
                        [4, 1, 2],
                        [4, 1, 3],
                        [4, 1, 4],
                        [4, 2, -4],
                        [4, 2, -3],
                        [4, 2, -2],
                        [4, 2, -1],
                        [4, 2, 0],
                        [4, 2, 1],
                        [4, 2, 2],
                        [4, 2, 3],
                        [4, 2, 4],
                        [4, 3, -4],
                        [4, 3, -3],
                        [4, 3, -2],
                        [4, 3, -1],
                        [4, 3, 0],
                        [4, 3, 1],
                        [4, 3, 2],
                        [4, 3, 3],
                        [4, 3, 4],
                        [4, 4, -4],
                        [4, 4, -3],
                        [4, 4, -2],
                        [4, 4, -1],
                        [4, 4, 0],
                        [4, 4, 1],
                        [4, 4, 2],
                        [4, 4, 3],
                        [4, 4, 4]])

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
            tfunc[..., c] = (0.3e1 / 0.2e1) * (0.1e1 + np.cos(phi)) * np.exp((-1*1j) * (phi1 + phi2))

        if Bindx == 2:
            t1 = np.cos(phi)
            tfunc[..., c] = (-0.3e1 / 0.2e1*1j) * np.exp((-1*1j) * phi1) * np.sqrt(0.2e1) * np.sqrt((1 + t1)) * np.sqrt((1 - t1))

        if Bindx == 3:
            tfunc[..., c] = (0.3e1 / 0.2e1) * (-0.1e1 + np.cos(phi)) * np.exp((-1*1j) * (phi1 - phi2))

        if Bindx == 4:
            t2 = np.cos(phi)
            tfunc[..., c] = (-0.3e1 / 0.2e1*1j) * np.exp((-1*1j) * phi2) * np.sqrt(0.2e1) * np.sqrt((1 - t2)) * np.sqrt((1 + t2))

        if Bindx == 5:
            tfunc[..., c] = 0.3e1 * np.cos(phi)

        if Bindx == 6:
            t3 = np.cos(phi)
            tfunc[..., c] = (-0.3e1 / 0.2e1*1j) * np.exp((1j) * phi2) * np.sqrt(0.2e1) * np.sqrt((1 - t3)) * np.sqrt((1 + t3))

        if Bindx == 7:
            tfunc[..., c] = (0.3e1 / 0.2e1) * (-0.1e1 + np.cos(phi)) * np.exp((1j) * (phi1 - phi2))

        if Bindx == 8:
            t4 = np.cos(phi)
            tfunc[..., c] = (-0.3e1 / 0.2e1*1j) * np.exp((1j) * phi1) * np.sqrt(0.2e1) * np.sqrt((1 - t4)) * np.sqrt((1 + t4))

        if Bindx == 9:
            tfunc[..., c] = (0.3e1 / 0.2e1) * (0.1e1 + np.cos(phi)) * np.exp((1j) * (phi1 + phi2))

        if Bindx == 10:
            t5 = np.cos(phi)
            tfunc[..., c] = (0.5e1 / 0.4e1) * np.exp((-2*1j) * (phi1 + phi2)) * (1 + (2 + t5) * t5)

        if Bindx == 11:
            t6 = np.cos(phi)
            tfunc[..., c] = (-0.5e1 / 0.2e1*1j) * np.exp((-1*1j) * (2 * phi1 + phi2)) * ((1 + t6) ** (0.3e1 / 0.2e1)) * np.sqrt((1 - t6))

        if Bindx == 12:
            t7 = np.sin(phi)
            tfunc[..., c] = -(0.5e1 / 0.4e1) * np.exp((-2*1j) * phi1) * np.sqrt(0.6e1) * t7 ** 2

        if Bindx == 13:
            t8 = np.cos(phi)
            tfunc[..., c] = (0.5e1 / 0.2e1*1j) * np.exp((-1*1j) * (2 * phi1 - phi2)) * ((1 - t8) ** (0.3e1 / 0.2e1)) * np.sqrt((1 + t8))

        if Bindx == 14:
            t9 = np.cos(phi)
            tfunc[..., c] = (0.5e1 / 0.4e1) * np.exp((-2*1j) * (phi1 - phi2)) * (1 + (-2 + t9) * t9)

        if Bindx == 15:
            t10 = np.cos(phi)
            tfunc[..., c] = (-0.5e1 / 0.2e1*1j) * np.exp((-1*1j) * (phi1 + 2 * phi2)) * np.sqrt((1 - t10)) * ((1 + t10) ** (0.3e1 / 0.2e1))

        if Bindx == 16:
            t11 = np.cos(phi)
            tfunc[..., c] = (0.5e1 / 0.2e1) * np.exp((-1*1j) * (phi1 + phi2)) * (2 * t11 ** 2 + t11 - 1)

        if Bindx == 17:
            t12 = np.cos(phi)
            tfunc[..., c] = (-0.5e1 / 0.2e1*1j) * np.exp((-1*1j) * phi1) * np.sqrt(0.6e1) * np.sqrt((1 + t12)) * t12 * np.sqrt((1 - t12))

        if Bindx == 18:
            t13 = np.cos(phi)
            tfunc[..., c] = (0.5e1 / 0.2e1) * np.exp((-1*1j) * (phi1 - phi2)) * (2 * t13 ** 2 - t13 - 1)

        if Bindx == 19:
            t14 = np.cos(phi)
            tfunc[..., c] = (0.5e1 / 0.2e1*1j) * np.exp((-1*1j) * (phi1 - 2 * phi2)) * ((1 - t14) ** (0.3e1 / 0.2e1)) * np.sqrt((1 + t14))

        if Bindx == 20:
            t15 = np.sin(phi)
            tfunc[..., c] = -(0.5e1 / 0.4e1) * np.exp((-2*1j) * phi2) * np.sqrt(0.6e1) * t15 ** 2

        if Bindx == 21:
            t16 = np.cos(phi)
            tfunc[..., c] = (-0.5e1 / 0.2e1*1j) * np.exp((-1*1j) * phi2) * np.sqrt(0.6e1) * np.sqrt((1 - t16)) * np.sqrt((1 + t16)) * t16

        if Bindx == 22:
            t17 = np.cos(phi)
            tfunc[..., c] = 0.15e2 / 0.2e1 * t17 ** 2 - 0.5e1 / 0.2e1

        if Bindx == 23:
            t18 = np.cos(phi)
            tfunc[..., c] = (-0.5e1 / 0.2e1*1j) * np.exp((1j) * phi2) * np.sqrt(0.6e1) * np.sqrt((1 + t18)) * t18 * np.sqrt((1 - t18))

        if Bindx == 24:
            t19 = np.sin(phi)
            tfunc[..., c] = -(0.5e1 / 0.4e1) * np.exp((2*1j) * phi2) * np.sqrt(0.6e1) * t19 ** 2

        if Bindx == 25:
            t20 = np.cos(phi)
            tfunc[..., c] = (0.5e1 / 0.2e1*1j) * np.exp((1j) * (phi1 - 2 * phi2)) * ((1 - t20) ** (0.3e1 / 0.2e1)) * np.sqrt((1 + t20))

        if Bindx == 26:
            t21 = np.cos(phi)
            tfunc[..., c] = (0.5e1 / 0.2e1) * np.exp((1j) * (phi1 - phi2)) * (2 * t21 ** 2 - t21 - 1)

        if Bindx == 27:
            t22 = np.cos(phi)
            tfunc[..., c] = (-0.5e1 / 0.2e1*1j) * np.exp((1j) * phi1) * np.sqrt(0.6e1) * np.sqrt((1 - t22)) * np.sqrt((1 + t22)) * t22

        if Bindx == 28:
            t23 = np.cos(phi)
            tfunc[..., c] = (0.5e1 / 0.2e1) * np.exp((1j) * (phi1 + phi2)) * (2 * t23 ** 2 + t23 - 1)

        if Bindx == 29:
            t24 = np.cos(phi)
            tfunc[..., c] = (-0.5e1 / 0.2e1*1j) * np.exp((1j) * (phi1 + 2 * phi2)) * np.sqrt((1 - t24)) * ((1 + t24) ** (0.3e1 / 0.2e1))

        if Bindx == 30:
            t25 = np.cos(phi)
            tfunc[..., c] = (0.5e1 / 0.4e1) * np.exp((2*1j) * (phi1 - phi2)) * (1 + (-2 + t25) * t25)

        if Bindx == 31:
            t26 = np.cos(phi)
            tfunc[..., c] = (0.5e1 / 0.2e1*1j) * np.exp((1j) * (2 * phi1 - phi2)) * ((1 - t26) ** (0.3e1 / 0.2e1)) * np.sqrt((1 + t26))

        if Bindx == 32:
            t27 = np.sin(phi)
            tfunc[..., c] = -(0.5e1 / 0.4e1) * np.exp((2*1j) * phi1) * np.sqrt(0.6e1) * t27 ** 2

        if Bindx == 33:
            t28 = np.cos(phi)
            tfunc[..., c] = (-0.5e1 / 0.2e1*1j) * np.exp((1j) * (2 * phi1 + phi2)) * np.sqrt((1 - t28)) * ((1 + t28) ** (0.3e1 / 0.2e1))

        if Bindx == 34:
            t29 = np.cos(phi)
            tfunc[..., c] = (0.5e1 / 0.4e1) * np.exp((2*1j) * (phi1 + phi2)) * (1 + (2 + t29) * t29)

        if Bindx == 35:
            t30 = np.cos(phi)
            t31 = t30 ** 2
            tfunc[..., c] = (0.7e1 / 0.8e1) * np.exp((-3*1j) * (phi1 + phi2)) * (3 * t31 + 1 + (t31 + 3) * t30)

        if Bindx == 36:
            t33 = np.cos(phi)
            tfunc[..., c] = (-0.7e1 / 0.8e1*1j) * np.exp((-1*1j) * (3 * phi1 + 2 * phi2)) * np.sqrt(0.6e1) * ((1 + t33) ** (0.5e1 / 0.2e1)) * np.sqrt((1 - t33))

        if Bindx == 37:
            t34 = np.sin(phi)
            tfunc[..., c] = -(0.7e1 / 0.8e1) * np.exp((-1*1j) * (3 * phi1 + phi2)) * np.sqrt(0.15e2) * t34 ** 2 * (0.1e1 + np.cos(phi))

        if Bindx == 38:
            t35 = np.cos(phi)
            tfunc[..., c] = (0.7e1 / 0.4e1*1j) * np.exp((-3*1j) * phi1) * np.sqrt(0.5e1) * ((1 - t35) ** (0.3e1 / 0.2e1)) * ((1 + t35) ** (0.3e1 / 0.2e1))

        if Bindx == 39:
            t36 = np.sin(phi)
            tfunc[..., c] = -(0.7e1 / 0.8e1) * np.exp((-1*1j) * (3 * phi1 - phi2)) * np.sqrt(0.15e2) * t36 ** 2 * (-0.1e1 + np.cos(phi))

        if Bindx == 40:
            t37 = np.cos(phi)
            tfunc[..., c] = (-0.7e1 / 0.8e1*1j) * np.exp((-1*1j) * (3 * phi1 - 2 * phi2)) * np.sqrt(0.6e1) * ((1 - t37) ** (0.5e1 / 0.2e1)) * np.sqrt((1 + t37))

        if Bindx == 41:
            t38 = np.cos(phi)
            t39 = t38 ** 2
            tfunc[..., c] = (0.7e1 / 0.8e1) * np.exp((-3*1j) * (phi1 - phi2)) * (-3 * t39 - 1 + (t39 + 3) * t38)

        if Bindx == 42:
            t41 = np.cos(phi)
            tfunc[..., c] = (-0.7e1 / 0.8e1*1j) * np.exp((-1*1j) * (2 * phi1 + 3 * phi2)) * np.sqrt(0.6e1) * np.sqrt((1 - t41)) * ((1 + t41) ** (0.5e1 / 0.2e1))

        if Bindx == 43:
            t42 = np.cos(phi)
            tfunc[..., c] = (0.7e1 / 0.4e1) * np.exp((-2*1j) * (phi1 + phi2)) * (-t42 - 2 + (3 * t42 + 4) * t42 ** 2)

        if Bindx == 44:
            t45 = np.cos(phi)
            tfunc[..., c] = (0.7e1 / 0.8e1*1j) * np.exp((-1*1j) * (2 * phi1 + phi2)) * np.sqrt(0.10e2) * ((1 + t45) ** (0.3e1 / 0.2e1)) * (1 + (-4 + 3 * t45) * t45) * ((1 - t45) ** (-0.1e1 / 0.2e1))

        if Bindx == 45:
            t46 = np.sin(phi)
            tfunc[..., c] = -(0.7e1 / 0.4e1) * np.exp((-2*1j) * phi1) * np.sqrt(0.30e2) * t46 ** 2 * np.cos(phi)

        if Bindx == 46:
            t47 = np.cos(phi)
            tfunc[..., c] = (0.7e1 / 0.8e1*1j) * (1 + 3 * t47) * np.sqrt((1 + t47)) * np.sqrt(0.10e2) * np.exp((-1*1j) * (2 * phi1 - phi2)) * ((1 - t47) ** (0.3e1 / 0.2e1))

        if Bindx == 47:
            t48 = np.cos(phi)
            tfunc[..., c] = (0.7e1 / 0.4e1) * np.exp((-2*1j) * (phi1 - phi2)) * (-t48 + 2 + (3 * t48 - 4) * t48 ** 2)

        if Bindx == 48:
            t51 = np.cos(phi)
            tfunc[..., c] = (-0.7e1 / 0.8e1*1j) * np.exp((-1*1j) * (2 * phi1 - 3 * phi2)) * np.sqrt(0.6e1) * ((1 - t51) ** (0.5e1 / 0.2e1)) * np.sqrt((1 + t51))

        if Bindx == 49:
            t52 = np.sin(phi)
            tfunc[..., c] = -(0.7e1 / 0.8e1) * np.exp((-1*1j) * (phi1 + 3 * phi2)) * np.sqrt(0.15e2) * t52 ** 2 * (0.1e1 + np.cos(phi))

        if Bindx == 50:
            t53 = np.cos(phi)
            tfunc[..., c] = (-0.7e1 / 0.8e1*1j) * np.exp((-1*1j) * (phi1 + 2 * phi2)) * np.sqrt(0.10e2) * np.sqrt((1 - t53)) * ((1 + t53) ** (0.3e1 / 0.2e1)) * (-1 + 3 * t53)

        if Bindx == 51:
            t54 = np.cos(phi)
            t55 = t54 ** 2
            tfunc[..., c] = (0.7e1 / 0.8e1) * np.exp((-1*1j) * (phi1 + phi2)) * (5 * t55 - 1 + (15 * t55 - 11) * t54)

        if Bindx == 52:
            t57 = np.cos(phi)
            t60 = 1 - t57
            tfunc[..., c] = (0.7e1 / 0.4e1*1j) * np.exp((-1*1j) * phi1) * np.sqrt(0.3e1) * np.sqrt((1 + t57)) * (t60 + (5 * t57 - 5) * t57 ** 2) * (t60 ** (-0.1e1 / 0.2e1))

        if Bindx == 53:
            t61 = np.cos(phi)
            t62 = t61 ** 2
            tfunc[..., c] = (0.7e1 / 0.8e1) * np.exp((-1*1j) * (phi1 - phi2)) * (-5 * t62 + 1 + (15 * t62 - 11) * t61)

        if Bindx == 54:
            t64 = np.cos(phi)
            tfunc[..., c] = (0.7e1 / 0.8e1*1j) * (1 + 3 * t64) * np.sqrt((1 + t64)) * np.sqrt(0.10e2) * np.exp((-1*1j) * (phi1 - 2 * phi2)) * ((1 - t64) ** (0.3e1 / 0.2e1))

        if Bindx == 55:
            t65 = np.sin(phi)
            tfunc[..., c] = -(0.7e1 / 0.8e1) * np.exp((-1*1j) * (phi1 - 3 * phi2)) * np.sqrt(0.15e2) * t65 ** 2 * (-0.1e1 + np.cos(phi))

        if Bindx == 56:
            t66 = np.cos(phi)
            tfunc[..., c] = (0.7e1 / 0.4e1*1j) * np.exp((-3*1j) * phi2) * np.sqrt(0.5e1) * ((1 - t66) ** (0.3e1 / 0.2e1)) * ((1 + t66) ** (0.3e1 / 0.2e1))

        if Bindx == 57:
            t67 = np.sin(phi)
            tfunc[..., c] = -(0.7e1 / 0.4e1) * np.exp((-2*1j) * phi2) * np.sqrt(0.30e2) * t67 ** 2 * np.cos(phi)

        if Bindx == 58:
            t68 = np.cos(phi)
            tfunc[..., c] = (-0.7e1 / 0.4e1*1j) * np.exp((-1*1j) * phi2) * np.sqrt(0.3e1) * np.sqrt((1 - t68)) * np.sqrt((1 + t68)) * (5 * t68 ** 2 - 1)

        if Bindx == 59:
            t69 = np.cos(phi)
            tfunc[..., c] = 0.7e1 / 0.2e1 * t69 * (5 * t69 ** 2 - 3)

        if Bindx == 60:
            t70 = np.cos(phi)
            t73 = 1 - t70
            tfunc[..., c] = (0.7e1 / 0.4e1*1j) * np.exp((1j) * phi2) * np.sqrt(0.3e1) * np.sqrt((1 + t70)) * (t73 + (5 * t70 - 5) * t70 ** 2) * (t73 ** (-0.1e1 / 0.2e1))

        if Bindx == 61:
            t74 = np.sin(phi)
            tfunc[..., c] = -(0.7e1 / 0.4e1) * np.exp((2*1j) * phi2) * np.sqrt(0.30e2) * t74 ** 2 * np.cos(phi)

        if Bindx == 62:
            t75 = np.cos(phi)
            tfunc[..., c] = (0.7e1 / 0.4e1*1j) * np.exp((3*1j) * phi2) * np.sqrt(0.5e1) * ((1 - t75) ** (0.3e1 / 0.2e1)) * ((1 + t75) ** (0.3e1 / 0.2e1))

        if Bindx == 63:
            t76 = np.sin(phi)
            tfunc[..., c] = -(0.7e1 / 0.8e1) * np.exp((1j) * (phi1 - 3 * phi2)) * np.sqrt(0.15e2) * t76 ** 2 * (-0.1e1 + np.cos(phi))

        if Bindx == 64:
            t77 = np.cos(phi)
            tfunc[..., c] = (0.7e1 / 0.8e1*1j) * np.exp((1j) * (phi1 - 2 * phi2)) * np.sqrt(0.10e2) * ((1 - t77) ** (0.3e1 / 0.2e1)) * np.sqrt((1 + t77)) * (1 + 3 * t77)

        if Bindx == 65:
            t78 = np.cos(phi)
            t79 = t78 ** 2
            tfunc[..., c] = (0.7e1 / 0.8e1) * np.exp((1j) * (phi1 - phi2)) * (-5 * t79 + 1 + (15 * t79 - 11) * t78)

        if Bindx == 66:
            t81 = np.cos(phi)
            tfunc[..., c] = (-0.7e1 / 0.4e1*1j) * np.exp((1j) * phi1) * np.sqrt(0.3e1) * np.sqrt((1 - t81)) * np.sqrt((1 + t81)) * (5 * t81 ** 2 - 1)

        if Bindx == 67:
            t82 = np.cos(phi)
            t83 = t82 ** 2
            tfunc[..., c] = (0.7e1 / 0.8e1) * np.exp((1j) * (phi1 + phi2)) * (5 * t83 - 1 + (15 * t83 - 11) * t82)

        if Bindx == 68:
            t85 = np.cos(phi)
            tfunc[..., c] = (0.7e1 / 0.8e1*1j) * np.exp((1j) * (phi1 + 2 * phi2)) * np.sqrt(0.10e2) * ((1 + t85) ** (0.3e1 / 0.2e1)) * (1 + (-4 + 3 * t85) * t85) * ((1 - t85) ** (-0.1e1 / 0.2e1))

        if Bindx == 69:
            t86 = np.sin(phi)
            tfunc[..., c] = -(0.7e1 / 0.8e1) * np.exp((1j) * (phi1 + 3 * phi2)) * np.sqrt(0.15e2) * t86 ** 2 * (0.1e1 + np.cos(phi))

        if Bindx == 70:
            t87 = np.cos(phi)
            tfunc[..., c] = (-0.7e1 / 0.8e1*1j) * np.exp((1j) * (2 * phi1 - 3 * phi2)) * np.sqrt(0.6e1) * ((1 - t87) ** (0.5e1 / 0.2e1)) * np.sqrt((1 + t87))

        if Bindx == 71:
            t88 = np.cos(phi)
            tfunc[..., c] = (0.7e1 / 0.4e1) * np.exp((2*1j) * (phi1 - phi2)) * (-t88 + 2 + (3 * t88 - 4) * t88 ** 2)

        if Bindx == 72:
            t91 = np.cos(phi)
            tfunc[..., c] = (0.7e1 / 0.8e1*1j) * np.exp((1j) * (2 * phi1 - phi2)) * np.sqrt(0.10e2) * ((1 - t91) ** (0.3e1 / 0.2e1)) * np.sqrt((1 + t91)) * (1 + 3 * t91)

        if Bindx == 73:
            t92 = np.sin(phi)
            tfunc[..., c] = -(0.7e1 / 0.4e1) * np.exp((2*1j) * phi1) * np.sqrt(0.30e2) * t92 ** 2 * np.cos(phi)

        if Bindx == 74:
            t93 = np.cos(phi)
            tfunc[..., c] = (-0.7e1 / 0.8e1*1j) * np.exp((1j) * (2 * phi1 + phi2)) * np.sqrt(0.10e2) * np.sqrt((1 - t93)) * ((1 + t93) ** (0.3e1 / 0.2e1)) * (-1 + 3 * t93)

        if Bindx == 75:
            t94 = np.cos(phi)
            tfunc[..., c] = (0.7e1 / 0.4e1) * np.exp((2*1j) * (phi1 + phi2)) * (-t94 - 2 + (3 * t94 + 4) * t94 ** 2)

        if Bindx == 76:
            t97 = np.cos(phi)
            tfunc[..., c] = (-0.7e1 / 0.8e1*1j) * np.exp((1j) * (2 * phi1 + 3 * phi2)) * np.sqrt(0.6e1) * np.sqrt((1 - t97)) * ((1 + t97) ** (0.5e1 / 0.2e1))

        if Bindx == 77:
            t98 = np.cos(phi)
            t99 = t98 ** 2
            tfunc[..., c] = (0.7e1 / 0.8e1) * np.exp((3*1j) * (phi1 - phi2)) * (-3 * t99 - 1 + (t99 + 3) * t98)

        if Bindx == 78:
            t101 = np.cos(phi)
            tfunc[..., c] = (-0.7e1 / 0.8e1*1j) * np.exp((1j) * (3 * phi1 - 2 * phi2)) * np.sqrt(0.6e1) * ((1 - t101) ** (0.5e1 / 0.2e1)) * np.sqrt((1 + t101))

        if Bindx == 79:
            t102 = np.sin(phi)
            tfunc[..., c] = -(0.7e1 / 0.8e1) * np.exp((1j) * (3 * phi1 - phi2)) * np.sqrt(0.15e2) * t102 ** 2 * (-0.1e1 + np.cos(phi))

        if Bindx == 80:
            t103 = np.cos(phi)
            tfunc[..., c] = (0.7e1 / 0.4e1*1j) * np.exp((3*1j) * phi1) * np.sqrt(0.5e1) * ((1 - t103) ** (0.3e1 / 0.2e1)) * ((1 + t103) ** (0.3e1 / 0.2e1))

        if Bindx == 81:
            t104 = np.sin(phi)
            tfunc[..., c] = -(0.7e1 / 0.8e1) * np.exp((1j) * (3 * phi1 + phi2)) * np.sqrt(0.15e2) * t104 ** 2 * (0.1e1 + np.cos(phi))

        if Bindx == 82:
            t105 = np.cos(phi)
            tfunc[..., c] = (-0.7e1 / 0.8e1*1j) * np.exp((1j) * (3 * phi1 + 2 * phi2)) * np.sqrt(0.6e1) * np.sqrt((1 - t105)) * ((1 + t105) ** (0.5e1 / 0.2e1))

        if Bindx == 83:
            t106 = np.cos(phi)
            t107 = t106 ** 2
            tfunc[..., c] = (0.7e1 / 0.8e1) * np.exp((3*1j) * (phi1 + phi2)) * (3 * t107 + 1 + (t107 + 3) * t106)

        if Bindx == 84:
            t109 = np.cos(phi)
            t113 = 4 * t109
            t110 = t109 ** 2
            tfunc[..., c] = (0.9e1 / 0.16e2) * np.exp((-4*1j) * (phi1 + phi2)) * (t113 + 1 + (t113 + 6 + t110) * t110)

        if Bindx == 85:
            t114 = np.cos(phi)
            tfunc[..., c] = (-0.9e1 / 0.8e1*1j) * np.exp((-1*1j) * (4 * phi1 + 3 * phi2)) * np.sqrt(0.2e1) * ((1 + t114) ** (0.7e1 / 0.2e1)) * np.sqrt((1 - t114))

        if Bindx == 86:
            t115 = np.cos(phi)
            t118 = 1 + t115
            t116 = t118 ** 2
            tfunc[..., c] = (0.9e1 / 0.8e1) * np.exp((-2*1j) * (2 * phi1 + phi2)) * np.sqrt(0.7e1) * (-1 + t115) * t118 * t116

        if Bindx == 87:
            t119 = np.cos(phi)
            tfunc[..., c] = (0.9e1 / 0.8e1*1j) * np.exp((-1*1j) * (4 * phi1 + phi2)) * np.sqrt(0.14e2) * ((1 - t119) ** (0.3e1 / 0.2e1)) * ((1 + t119) ** (0.5e1 / 0.2e1))

        if Bindx == 88:
            t122 = np.sin(phi)
            t120 = t122 ** 2
            tfunc[..., c] = (0.9e1 / 0.16e2) * np.exp((-4*1j) * phi1) * np.sqrt(0.70e2) * t120 ** 2

        if Bindx == 89:
            t123 = np.cos(phi)
            tfunc[..., c] = (-0.9e1 / 0.8e1*1j) * np.exp((-1*1j) * (4 * phi1 - phi2)) * np.sqrt(0.14e2) * ((1 - t123) ** (0.5e1 / 0.2e1)) * ((1 + t123) ** (0.3e1 / 0.2e1))

        if Bindx == 90:
            t124 = np.cos(phi)
            t127 = -1 + t124
            t125 = t127 ** 2
            tfunc[..., c] = (0.9e1 / 0.8e1) * np.exp((-2*1j) * (2 * phi1 - phi2)) * np.sqrt(0.7e1) * t127 * t125 * (1 + t124)

        if Bindx == 91:
            t128 = np.cos(phi)
            tfunc[..., c] = (0.9e1 / 0.8e1*1j) * np.exp((-1*1j) * (4 * phi1 - 3 * phi2)) * np.sqrt(0.2e1) * ((1 - t128) ** (0.7e1 / 0.2e1)) * np.sqrt((1 + t128))

        if Bindx == 92:
            t129 = np.cos(phi)
            t133 = -4 * t129
            t130 = t129 ** 2
            tfunc[..., c] = (0.9e1 / 0.16e2) * np.exp((-4*1j) * (phi1 - phi2)) * (t133 + 1 + (t133 + 6 + t130) * t130)

        if Bindx == 93:
            t134 = np.cos(phi)
            tfunc[..., c] = (-0.9e1 / 0.8e1*1j) * np.exp((-1*1j) * (3 * phi1 + 4 * phi2)) * np.sqrt(0.2e1) * np.sqrt((1 - t134)) * ((1 + t134) ** (0.7e1 / 0.2e1))

        if Bindx == 94:
            t135 = np.cos(phi)
            t136 = t135 ** 2
            tfunc[..., c] = (0.9e1 / 0.8e1) * np.exp((-3*1j) * (phi1 + phi2)) * (-5 * t135 - 3 + (9 * t135 + 3 + 4 * t136) * t136)

        if Bindx == 95:
            t139 = np.cos(phi)
            tfunc[..., c] = (0.9e1 / 0.8e1*1j) * np.exp((-1*1j) * (3 * phi1 + 2 * phi2)) * np.sqrt(0.14e2) * ((1 + t139) ** (0.5e1 / 0.2e1)) * (1 + (-3 + 2 * t139) * t139) * ((1 - t139) ** (-0.1e1 / 0.2e1))

        if Bindx == 96:
            t141 = np.cos(phi)
            t140 = np.sin(phi)
            tfunc[..., c] = -(0.9e1 / 0.8e1) * np.exp((-1*1j) * (3 * phi1 + phi2)) * np.sqrt(0.7e1) * t140 ** 2 * (-1 + (3 + 4 * t141) * t141)

        if Bindx == 97:
            t142 = np.cos(phi)
            tfunc[..., c] = (0.9e1 / 0.4e1*1j) * t142 * (1 + (-2 + t142) * t142) * ((1 + t142) ** (0.3e1 / 0.2e1)) * np.sqrt(0.35e2) * np.exp((-3*1j) * phi1) * ((1 - t142) ** (-0.1e1 / 0.2e1))

        if Bindx == 98:
            t144 = np.cos(phi)
            t143 = np.sin(phi)
            tfunc[..., c] = -(0.9e1 / 0.8e1) * np.exp((-1*1j) * (3 * phi1 - phi2)) * np.sqrt(0.7e1) * t143 ** 2 * (-1 + (-3 + 4 * t144) * t144)

        if Bindx == 99:
            t145 = np.cos(phi)
            tfunc[..., c] = (-0.9e1 / 0.8e1*1j) * (1 + 2 * t145) * np.sqrt((1 + t145)) * np.sqrt(0.14e2) * np.exp((-1*1j) * (3 * phi1 - 2 * phi2)) * ((1 - t145) ** (0.5e1 / 0.2e1))

        if Bindx == 100:
            t146 = np.cos(phi)
            t147 = t146 ** 2
            tfunc[..., c] = (0.9e1 / 0.8e1) * np.exp((-3*1j) * (phi1 - phi2)) * (5 * t146 - 3 + (-9 * t146 + 3 + 4 * t147) * t147)

        if Bindx == 101:
            t150 = np.cos(phi)
            tfunc[..., c] = (0.9e1 / 0.8e1*1j) * np.exp((-1*1j) * (3 * phi1 - 4 * phi2)) * np.sqrt(0.2e1) * ((1 - t150) ** (0.7e1 / 0.2e1)) * np.sqrt((1 + t150))

        if Bindx == 102:
            t151 = np.cos(phi)
            t154 = 1 + t151
            t152 = t154 ** 2
            tfunc[..., c] = (0.9e1 / 0.8e1) * np.exp((-2*1j) * (phi1 + 2 * phi2)) * np.sqrt(0.7e1) * (-1 + t151) * t154 * t152

        if Bindx == 103:
            t155 = np.cos(phi)
            tfunc[..., c] = (-0.9e1 / 0.8e1*1j) * np.exp((-1*1j) * (2 * phi1 + 3 * phi2)) * np.sqrt(0.14e2) * np.sqrt((1 - t155)) * ((1 + t155) ** (0.5e1 / 0.2e1)) * (-1 + 2 * t155)

        if Bindx == 104:
            t156 = np.cos(phi)
            t157 = t156 ** 2
            tfunc[..., c] = (0.9e1 / 0.4e1) * np.exp((-2*1j) * (phi1 + phi2)) * (-5 * t156 + 1 + (7 * t156 - 6 + 7 * t157) * t157)

        if Bindx == 105:
            t160 = np.cos(phi)
            t161 = t160 ** 2
            tfunc[..., c] = (0.9e1 / 0.8e1*1j) * np.exp((-1*1j) * (2 * phi1 + phi2)) * np.sqrt(0.2e1) * ((1 + t160) ** (0.3e1 / 0.2e1)) * (-21 * t161 + 1 + (14 * t161 + 6) * t160) * ((1 - t160) ** (-0.1e1 / 0.2e1))

        if Bindx == 106:
            t164 = np.cos(phi)
            t163 = np.sin(phi)
            tfunc[..., c] = -(0.9e1 / 0.8e1) * np.exp((-2*1j) * phi1) * np.sqrt(0.10e2) * t163 ** 2 * (7 * t164 ** 2 - 1)

        if Bindx == 107:
            t165 = np.cos(phi)
            tfunc[..., c] = (0.9e1 / 0.8e1*1j) * (-1 + (7 + 14 * t165) * t165) * np.sqrt((1 + t165)) * np.sqrt(0.2e1) * np.exp((-1*1j) * (2 * phi1 - phi2)) * ((1 - t165) ** (0.3e1 / 0.2e1))

        if Bindx == 108:
            t166 = np.cos(phi)
            t167 = t166 ** 2
            tfunc[..., c] = (0.9e1 / 0.4e1) * np.exp((-2*1j) * (phi1 - phi2)) * (5 * t166 + 1 + (-7 * t166 - 6 + 7 * t167) * t167)

        if Bindx == 109:
            t170 = np.cos(phi)
            tfunc[..., c] = (-0.9e1 / 0.8e1*1j) * (1 + 2 * t170) * np.sqrt((1 + t170)) * np.sqrt(0.14e2) * np.exp((-1*1j) * (2 * phi1 - 3 * phi2)) * ((1 - t170) ** (0.5e1 / 0.2e1))

        if Bindx == 110:
            t171 = np.cos(phi)
            t174 = -1 + t171
            t172 = t174 ** 2
            tfunc[..., c] = (0.9e1 / 0.8e1) * np.exp((-2*1j) * (phi1 - 2 * phi2)) * np.sqrt(0.7e1) * t174 * t172 * (1 + t171)

        if Bindx == 111:
            t175 = np.cos(phi)
            tfunc[..., c] = (0.9e1 / 0.8e1*1j) * np.exp((-1*1j) * (phi1 + 4 * phi2)) * np.sqrt(0.14e2) * ((1 - t175) ** (0.3e1 / 0.2e1)) * ((1 + t175) ** (0.5e1 / 0.2e1))

        if Bindx == 112:
            t177 = np.cos(phi)
            t176 = np.sin(phi)
            tfunc[..., c] = -(0.9e1 / 0.8e1) * np.exp((-1*1j) * (phi1 + 3 * phi2)) * np.sqrt(0.7e1) * t176 ** 2 * (-1 + (3 + 4 * t177) * t177)

        if Bindx == 113:
            t178 = np.cos(phi)
            tfunc[..., c] = (-0.9e1 / 0.8e1*1j) * np.exp((-1*1j) * (phi1 + 2 * phi2)) * np.sqrt(0.2e1) * np.sqrt((1 - t178)) * ((1 + t178) ** (0.3e1 / 0.2e1)) * (-1 + (-7 + 14 * t178) * t178)

        if Bindx == 114:
            t179 = np.cos(phi)
            t180 = t179 ** 2
            tfunc[..., c] = (0.9e1 / 0.8e1) * np.exp((-1*1j) * (phi1 + phi2)) * (-3 * t179 + 3 + (7 * t179 - 27 + 28 * t180) * t180)

        if Bindx == 115:
            t183 = np.cos(phi)
            tfunc[..., c] = (-0.9e1 / 0.4e1*1j) * np.exp((-1*1j) * phi1) * np.sqrt(0.5e1) * t183 * np.sqrt((1 + t183)) * np.sqrt((1 - t183)) * (7 * t183 ** 2 - 3)

        if Bindx == 116:
            t188 = np.cos(phi)
            t189 = t188 ** 2
            tfunc[..., c] = (0.9e1 / 0.8e1) * np.exp((-1*1j) * (phi1 - phi2)) * (3 * t188 + 3 + (-7 * t188 - 27 + 28 * t189) * t189)

        if Bindx == 117:
            t192 = np.cos(phi)
            tfunc[..., c] = (0.9e1 / 0.8e1*1j) * (-1 + (7 + 14 * t192) * t192) * np.sqrt((1 + t192)) * np.sqrt(0.2e1) * np.exp((-1*1j) * (phi1 - 2 * phi2)) * ((1 - t192) ** (0.3e1 / 0.2e1))

        if Bindx == 118:
            t194 = np.cos(phi)
            t193 = np.sin(phi)
            tfunc[..., c] = -(0.9e1 / 0.8e1) * np.exp((-1*1j) * (phi1 - 3 * phi2)) * np.sqrt(0.7e1) * t193 ** 2 * (-1 + (-3 + 4 * t194) * t194)

        if Bindx == 119:
            t195 = np.cos(phi)
            tfunc[..., c] = (-0.9e1 / 0.8e1*1j) * np.exp((-1*1j) * (phi1 - 4 * phi2)) * np.sqrt(0.14e2) * ((1 - t195) ** (0.5e1 / 0.2e1)) * ((1 + t195) ** (0.3e1 / 0.2e1))

        if Bindx == 120:
            t198 = np.sin(phi)
            t196 = t198 ** 2
            tfunc[..., c] = (0.9e1 / 0.16e2) * np.exp((-4*1j) * phi2) * np.sqrt(0.70e2) * t196 ** 2

        if Bindx == 121:
            t199 = np.cos(phi)
            tfunc[..., c] = (0.9e1 / 0.4e1*1j) * np.exp((-3*1j) * phi2) * np.sqrt(0.35e2) * ((1 - t199) ** (0.3e1 / 0.2e1)) * ((1 + t199) ** (0.3e1 / 0.2e1)) * t199

        if Bindx == 122:
            t201 = np.cos(phi)
            t200 = np.sin(phi)
            tfunc[..., c] = -(0.9e1 / 0.8e1) * np.exp((-2*1j) * phi2) * np.sqrt(0.10e2) * t200 ** 2 * (7 * t201 ** 2 - 1)

        if Bindx == 123:
            t202 = np.cos(phi)
            tfunc[..., c] = (-0.9e1 / 0.4e1*1j) * np.exp((-1*1j) * phi2) * np.sqrt(0.5e1) * np.sqrt((1 - t202)) * np.sqrt((1 + t202)) * t202 * (7 * t202 ** 2 - 3)

        if Bindx == 124:
            t203 = np.cos(phi)
            t204 = t203 ** 2
            tfunc[..., c] = 0.27e2 / 0.8e1 + (-0.135e3 / 0.4e1 + 0.315e3 / 0.8e1 * t204) * t204

        if Bindx == 125:
            t206 = np.cos(phi)
            tfunc[..., c] = (-0.9e1 / 0.4e1*1j) * np.exp((1j) * phi2) * np.sqrt(0.5e1) * t206 * np.sqrt((1 + t206)) * np.sqrt((1 - t206)) * (7 * t206 ** 2 - 3)

        if Bindx == 126:
            t212 = np.cos(phi)
            t211 = np.sin(phi)
            tfunc[..., c] = -(0.9e1 / 0.8e1) * np.exp((2*1j) * phi2) * np.sqrt(0.10e2) * t211 ** 2 * (7 * t212 ** 2 - 1)

        if Bindx == 127:
            t213 = np.cos(phi)
            tfunc[..., c] = (0.9e1 / 0.4e1*1j) * t213 * ((1 + t213) ** (0.3e1 / 0.2e1)) * (1 + (-2 + t213) * t213) * np.sqrt(0.35e2) * np.exp((3*1j) * phi2) * ((1 - t213) ** (-0.1e1 / 0.2e1))

        if Bindx == 128:
            t216 = np.sin(phi)
            t214 = t216 ** 2
            tfunc[..., c] = (0.9e1 / 0.16e2) * np.exp((4*1j) * phi2) * np.sqrt(0.70e2) * t214 ** 2

        if Bindx == 129:
            t217 = np.cos(phi)
            tfunc[..., c] = (-0.9e1 / 0.8e1*1j) * np.exp((1j) * (phi1 - 4 * phi2)) * np.sqrt(0.14e2) * ((1 - t217) ** (0.5e1 / 0.2e1)) * ((1 + t217) ** (0.3e1 / 0.2e1))

        if Bindx == 130:
            t219 = np.cos(phi)
            t218 = np.sin(phi)
            tfunc[..., c] = -(0.9e1 / 0.8e1) * np.exp((1j) * (phi1 - 3 * phi2)) * np.sqrt(0.7e1) * t218 ** 2 * (-1 + (-3 + 4 * t219) * t219)

        if Bindx == 131:
            t220 = np.cos(phi)
            tfunc[..., c] = (0.9e1 / 0.8e1*1j) * np.exp((1j) * (phi1 - 2 * phi2)) * np.sqrt(0.2e1) * ((1 - t220) ** (0.3e1 / 0.2e1)) * np.sqrt((1 + t220)) * (-1 + (7 + 14 * t220) * t220)

        if Bindx == 132:
            t221 = np.cos(phi)
            t222 = t221 ** 2
            tfunc[..., c] = (0.9e1 / 0.8e1) * np.exp((1j) * (phi1 - phi2)) * (3 * t221 + 3 + (-7 * t221 - 27 + 28 * t222) * t222)

        if Bindx == 133:
            t225 = np.cos(phi)
            tfunc[..., c] = (-0.9e1 / 0.4e1*1j) * np.exp((1j) * phi1) * np.sqrt(0.5e1) * np.sqrt((1 - t225)) * np.sqrt((1 + t225)) * t225 * (7 * t225 ** 2 - 3)

        if Bindx == 134:
            t226 = np.cos(phi)
            t227 = t226 ** 2
            tfunc[..., c] = (0.9e1 / 0.8e1) * np.exp((1j) * (phi1 + phi2)) * (-3 * t226 + 3 + (7 * t226 - 27 + 28 * t227) * t227)

        if Bindx == 135:
            t230 = np.cos(phi)
            t231 = t230 ** 2
            tfunc[..., c] = (0.9e1 / 0.8e1*1j) * np.exp((1j) * (phi1 + 2 * phi2)) * np.sqrt(0.2e1) * ((1 + t230) ** (0.3e1 / 0.2e1)) * (-21 * t231 + 1 + (14 * t231 + 6) * t230) * ((1 - t230) ** (-0.1e1 / 0.2e1))

        if Bindx == 136:
            t234 = np.cos(phi)
            t233 = np.sin(phi)
            tfunc[..., c] = -(0.9e1 / 0.8e1) * np.exp((1j) * (phi1 + 3 * phi2)) * np.sqrt(0.7e1) * t233 ** 2 * (-1 + (3 + 4 * t234) * t234)

        if Bindx == 137:
            t235 = np.cos(phi)
            tfunc[..., c] = (0.9e1 / 0.8e1*1j) * np.exp((1j) * (phi1 + 4 * phi2)) * np.sqrt(0.14e2) * ((1 - t235) ** (0.3e1 / 0.2e1)) * ((1 + t235) ** (0.5e1 / 0.2e1))

        if Bindx == 138:
            t236 = np.cos(phi)
            t239 = -1 + t236
            t237 = t239 ** 2
            tfunc[..., c] = (0.9e1 / 0.8e1) * np.exp((2*1j) * (phi1 - 2 * phi2)) * np.sqrt(0.7e1) * t239 * t237 * (1 + t236)

        if Bindx == 139:
            t240 = np.cos(phi)
            tfunc[..., c] = (-0.9e1 / 0.8e1*1j) * np.exp((1j) * (2 * phi1 - 3 * phi2)) * np.sqrt(0.14e2) * ((1 - t240) ** (0.5e1 / 0.2e1)) * np.sqrt((1 + t240)) * (1 + 2 * t240)

        if Bindx == 140:
            t241 = np.cos(phi)
            t242 = t241 ** 2
            tfunc[..., c] = (0.9e1 / 0.4e1) * np.exp((2*1j) * (phi1 - phi2)) * (5 * t241 + 1 + (-7 * t241 - 6 + 7 * t242) * t242)

        if Bindx == 141:
            t245 = np.cos(phi)
            tfunc[..., c] = (0.9e1 / 0.8e1*1j) * np.exp((1j) * (2 * phi1 - phi2)) * np.sqrt(0.2e1) * ((1 - t245) ** (0.3e1 / 0.2e1)) * np.sqrt((1 + t245)) * (-1 + (7 + 14 * t245) * t245)

        if Bindx == 142:
            t247 = np.cos(phi)
            t246 = np.sin(phi)
            tfunc[..., c] = -(0.9e1 / 0.8e1) * np.exp((2*1j) * phi1) * np.sqrt(0.10e2) * t246 ** 2 * (7 * t247 ** 2 - 1)

        if Bindx == 143:
            t248 = np.cos(phi)
            tfunc[..., c] = (-0.9e1 / 0.8e1*1j) * np.exp((1j) * (2 * phi1 + phi2)) * np.sqrt(0.2e1) * np.sqrt((1 - t248)) * ((1 + t248) ** (0.3e1 / 0.2e1)) * (-1 + (-7 + 14 * t248) * t248)

        if Bindx == 144:
            t249 = np.cos(phi)
            t250 = t249 ** 2
            tfunc[..., c] = (0.9e1 / 0.4e1) * np.exp((2*1j) * (phi1 + phi2)) * (-5 * t249 + 1 + (7 * t249 - 6 + 7 * t250) * t250)

        if Bindx == 145:
            t253 = np.cos(phi)
            tfunc[..., c] = (0.9e1 / 0.8e1*1j) * np.exp((1j) * (2 * phi1 + 3 * phi2)) * np.sqrt(0.14e2) * ((1 + t253) ** (0.5e1 / 0.2e1)) * (1 + (-3 + 2 * t253) * t253) * ((1 - t253) ** (-0.1e1 / 0.2e1))

        if Bindx == 146:
            t254 = np.cos(phi)
            t257 = 1 + t254
            t255 = t257 ** 2
            tfunc[..., c] = (0.9e1 / 0.8e1) * np.exp((2*1j) * (phi1 + 2 * phi2)) * np.sqrt(0.7e1) * (-1 + t254) * t257 * t255

        if Bindx == 147:
            t258 = np.cos(phi)
            tfunc[..., c] = (0.9e1 / 0.8e1*1j) * np.exp((1j) * (3 * phi1 - 4 * phi2)) * np.sqrt(0.2e1) * ((1 - t258) ** (0.7e1 / 0.2e1)) * np.sqrt((1 + t258))

        if Bindx == 148:
            t259 = np.cos(phi)
            t260 = t259 ** 2
            tfunc[..., c] = (0.9e1 / 0.8e1) * np.exp((3*1j) * (phi1 - phi2)) * (5 * t259 - 3 + (-9 * t259 + 3 + 4 * t260) * t260)

        if Bindx == 149:
            t263 = np.cos(phi)
            tfunc[..., c] = (-0.9e1 / 0.8e1*1j) * np.exp((1j) * (3 * phi1 - 2 * phi2)) * np.sqrt(0.14e2) * ((1 - t263) ** (0.5e1 / 0.2e1)) * np.sqrt((1 + t263)) * (1 + 2 * t263)

        if Bindx == 150:
            t265 = np.cos(phi)
            t264 = np.sin(phi)
            tfunc[..., c] = -(0.9e1 / 0.8e1) * np.exp((1j) * (3 * phi1 - phi2)) * np.sqrt(0.7e1) * t264 ** 2 * (-1 + (-3 + 4 * t265) * t265)

        if Bindx == 151:
            t266 = np.cos(phi)
            tfunc[..., c] = (0.9e1 / 0.4e1*1j) * np.exp((3*1j) * phi1) * np.sqrt(0.35e2) * ((1 - t266) ** (0.3e1 / 0.2e1)) * ((1 + t266) ** (0.3e1 / 0.2e1)) * t266

        if Bindx == 152:
            t268 = np.cos(phi)
            t267 = np.sin(phi)
            tfunc[..., c] = -(0.9e1 / 0.8e1) * np.exp((1j) * (3 * phi1 + phi2)) * np.sqrt(0.7e1) * t267 ** 2 * (-1 + (3 + 4 * t268) * t268)

        if Bindx == 153:
            t269 = np.cos(phi)
            tfunc[..., c] = (-0.9e1 / 0.8e1*1j) * np.exp((1j) * (3 * phi1 + 2 * phi2)) * np.sqrt(0.14e2) * np.sqrt((1 - t269)) * ((1 + t269) ** (0.5e1 / 0.2e1)) * (-1 + 2 * t269)

        if Bindx == 154:
            t270 = np.cos(phi)
            t271 = t270 ** 2
            tfunc[..., c] = (0.9e1 / 0.8e1) * np.exp((3*1j) * (phi1 + phi2)) * (-5 * t270 - 3 + (9 * t270 + 3 + 4 * t271) * t271)

        if Bindx == 155:
            t274 = np.cos(phi)
            tfunc[..., c] = (-0.9e1 / 0.8e1*1j) * np.exp((1j) * (3 * phi1 + 4 * phi2)) * np.sqrt(0.2e1) * np.sqrt((1 - t274)) * ((1 + t274) ** (0.7e1 / 0.2e1))

        if Bindx == 156:
            t275 = np.cos(phi)
            t279 = -4 * t275
            t276 = t275 ** 2
            tfunc[..., c] = (0.9e1 / 0.16e2) * np.exp((4*1j) * (phi1 - phi2)) * (t279 + 1 + (t279 + 6 + t276) * t276)

        if Bindx == 157:
            t280 = np.cos(phi)
            tfunc[..., c] = (0.9e1 / 0.8e1*1j) * np.exp((1j) * (4 * phi1 - 3 * phi2)) * np.sqrt(0.2e1) * ((1 - t280) ** (0.7e1 / 0.2e1)) * np.sqrt((1 + t280))

        if Bindx == 158:
            t281 = np.cos(phi)
            t284 = -1 + t281
            t282 = t284 ** 2
            tfunc[..., c] = (0.9e1 / 0.8e1) * np.exp((2*1j) * (2 * phi1 - phi2)) * np.sqrt(0.7e1) * t284 * t282 * (1 + t281)

        if Bindx == 159:
            t285 = np.cos(phi)
            tfunc[..., c] = (-0.9e1 / 0.8e1*1j) * np.exp((1j) * (4 * phi1 - phi2)) * np.sqrt(0.14e2) * ((1 - t285) ** (0.5e1 / 0.2e1)) * ((1 + t285) ** (0.3e1 / 0.2e1))

        if Bindx == 160:
            t288 = np.sin(phi)
            t286 = t288 ** 2
            tfunc[..., c] = (0.9e1 / 0.16e2) * np.exp((4*1j) * phi1) * np.sqrt(0.70e2) * t286 ** 2

        if Bindx == 161:
            t289 = np.cos(phi)
            tfunc[..., c] = (0.9e1 / 0.8e1*1j) * np.exp((1j) * (4 * phi1 + phi2)) * np.sqrt(0.14e2) * ((1 - t289) ** (0.3e1 / 0.2e1)) * ((1 + t289) ** (0.5e1 / 0.2e1))

        if Bindx == 162:
            t290 = np.cos(phi)
            t293 = 1 + t290
            t291 = t293 ** 2
            tfunc[..., c] = (0.9e1 / 0.8e1) * np.exp((2*1j) * (2 * phi1 + phi2)) * np.sqrt(0.7e1) * (-1 + t290) * t293 * t291

        if Bindx == 163:
            t294 = np.cos(phi)
            tfunc[..., c] = (-0.9e1 / 0.8e1*1j) * np.exp((1j) * (4 * phi1 + 3 * phi2)) * np.sqrt(0.2e1) * np.sqrt((1 - t294)) * ((1 + t294) ** (0.7e1 / 0.2e1))

        if Bindx == 164:
            t295 = np.cos(phi)
            t299 = 4 * t295
            t296 = t295 ** 2
            tfunc[..., c] = (0.9e1 / 0.16e2) * np.exp((4*1j) * (phi1 + phi2)) * (t299 + 1 + (t299 + 6 + t296) * t296)

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

