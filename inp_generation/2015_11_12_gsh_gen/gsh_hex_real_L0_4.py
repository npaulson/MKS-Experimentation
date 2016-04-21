import numpy as np


def gsh(phi1, phi, phi2, L):

    zvec = np.abs(phi) < 1e-8
    zvec = zvec.astype(int)
    randvec = np.round(np.random.rand(zvec.shape[0]))
    randvecopp = np.ones(zvec.shape[0]) - randvec
    phi += (1e-7)*zvec*(randvec - randvecopp)

    out_tvalues = np.zeros(phi1.shape, dtype='complex128')

    if L == 0:
        out_tvalues = np.sqrt(0.2e1)

    if L == 1:
        t35 = np.cos(phi)
        out_tvalues = -0.5e1 / 0.2e1 * np.sqrt(0.3e1) * (t35 ** 2 - 1) * np.cos((2 * phi1))

    if L == 2:
        t37 = np.cos(phi)
        t36 = np.sin(phi)
        out_tvalues = -0.5e1 * np.sqrt(0.3e1) * t37 * t36 ** 2 * np.sin(phi1) * ((1 - t37) ** (-0.1e1 / 0.2e1)) * ((1 + t37) ** (-0.1e1 / 0.2e1))

    if L == 3:
        t38 = np.cos(phi)
        out_tvalues = 0.5e1 / 0.2e1 * np.sqrt(0.2e1) * (3 * t38 ** 2 - 1)

    if L == 4:
        t40 = np.cos(phi)
        t39 = np.sin(phi)
        out_tvalues = -0.5e1 * np.sqrt(0.3e1) * t40 * t39 ** 2 * np.sin(phi1) * ((1 - t40) ** (-0.1e1 / 0.2e1)) * ((1 + t40) ** (-0.1e1 / 0.2e1))

    if L == 5:
        t41 = np.cos(phi)
        out_tvalues = -0.5e1 / 0.2e1 * np.sqrt(0.3e1) * (t41 ** 2 - 1) * np.cos((2 * phi1))

    if L == 6:
        t42 = np.cos(phi)
        t43 = t42 ** 2
        out_tvalues = 0.9e1 / 0.8e1 * np.sqrt(0.35e2) * np.cos((4 * phi1)) * (1 + (-2 + t43) * t43)

    if L == 7:
        t48 = np.sin(phi)
        t46 = t48 ** 2
        t45 = np.cos(phi)
        out_tvalues = -0.9e1 / 0.4e1 * np.sqrt(0.2e1) * np.sqrt(0.35e2) * t45 * t46 ** 2 * np.sin((3 * phi1)) * ((1 - t45) ** (-0.1e1 / 0.2e1)) * ((1 + t45) ** (-0.1e1 / 0.2e1))

    if L == 8:
        t49 = np.cos(phi)
        t50 = t49 ** 2
        out_tvalues = -0.9e1 / 0.4e1 * np.sqrt(0.5e1) * (1 + (-8 + 7 * t50) * t50) * np.cos((2 * phi1))

    if L == 9:
        t53 = np.cos(phi)
        t52 = np.sin(phi)
        out_tvalues = -0.9e1 / 0.4e1 * np.sqrt(0.2e1) * np.sqrt(0.5e1) * t53 * t52 ** 2 * (7 * t53 ** 2 - 3) * np.sin(phi1) * ((1 - t53) ** (-0.1e1 / 0.2e1)) * ((1 + t53) ** (-0.1e1 / 0.2e1))

    if L == 10:
        t54 = np.cos(phi)
        t55 = t54 ** 2
        out_tvalues = 0.9e1 / 0.8e1 * np.sqrt(0.2e1) * (3 + (-30 + 35 * t55) * t55)

    if L == 11:
        t58 = np.cos(phi)
        t57 = np.sin(phi)
        out_tvalues = -0.9e1 / 0.4e1 * np.sqrt(0.2e1) * np.sqrt(0.5e1) * t58 * t57 ** 2 * (7 * t58 ** 2 - 3) * np.sin(phi1) * ((1 - t58) ** (-0.1e1 / 0.2e1)) * ((1 + t58) ** (-0.1e1 / 0.2e1))

    if L == 12:
        t59 = np.cos(phi)
        t60 = t59 ** 2
        out_tvalues = -0.9e1 / 0.4e1 * np.sqrt(0.5e1) * (1 + (-8 + 7 * t60) * t60) * np.cos((2 * phi1))

    if L == 13:
        t65 = np.sin(phi)
        t63 = t65 ** 2
        t62 = np.cos(phi)
        out_tvalues = -0.9e1 / 0.4e1 * np.sqrt(0.2e1) * np.sqrt(0.35e2) * t62 * t63 ** 2 * np.sin((3 * phi1)) * ((1 - t62) ** (-0.1e1 / 0.2e1)) * ((1 + t62) ** (-0.1e1 / 0.2e1))

    if L == 14:
        t66 = np.cos(phi)
        t67 = t66 ** 2
        out_tvalues = 0.9e1 / 0.8e1 * np.sqrt(0.35e2) * np.cos((4 * phi1)) * (1 + (-2 + t67) * t67)

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

    return out_tvalues, indxvec


if __name__ == '__main__':
    tvals, indxvec = gsh(np.array([0.1,0.2]), np.array([0.0, 0.4]), np.array([0.3, 0.6]), 1)
    print tvals
    print indxvec

