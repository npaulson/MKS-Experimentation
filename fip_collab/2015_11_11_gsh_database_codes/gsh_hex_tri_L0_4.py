import numpy as np


def gsh(e_angles, L):

    phi1 = e_angles[0, :]
    phi = e_angles[1, :]
    phi2 = e_angles[2, :]

    zvec = np.abs(phi) < 10e-17
    zvec = zvec.astype(int)
    randvec = np.round(np.random.rand(zvec.shape[0]))
    randvecopp = np.ones(zvec.shape[0]) - randvec
    phi += (1e-7)*zvec*(randvec - randvecopp)

    if L == 0:
        out_tvalues = 1

    if L == 1:
        t652 = np.sin(phi)
        out_tvalues = -(0.5e1 / 0.4e1) * np.exp((-2*1j) * phi1) * np.sqrt(0.6e1) * t652 ** 2

    if L == 2:
        t653 = np.cos(phi)
        out_tvalues = (-0.5e1 / 0.2e1*1j) * np.exp((-1*1j) * phi1) * np.sqrt(0.6e1) * np.sqrt((1 + t653)) * t653 * np.sqrt((1 - t653))

    if L == 3:
        t654 = np.cos(phi)
        out_tvalues = 0.15e2 / 0.2e1 * t654 ** 2 - 0.5e1 / 0.2e1

    if L == 4:
        t655 = np.cos(phi)
        out_tvalues = (-0.5e1 / 0.2e1*1j) * np.exp((1j) * phi1) * np.sqrt(0.6e1) * np.sqrt((1 - t655)) * np.sqrt((1 + t655)) * t655

    if L == 5:
        t656 = np.sin(phi)
        out_tvalues = -(0.5e1 / 0.4e1) * np.exp((2*1j) * phi1) * np.sqrt(0.6e1) * t656 ** 2

    if L == 6:
        t659 = np.sin(phi)
        t657 = t659 ** 2
        out_tvalues = (0.9e1 / 0.16e2) * np.exp((-4*1j) * phi1) * np.sqrt(0.70e2) * t657 ** 2

    if L == 7:
        t660 = np.cos(phi)
        out_tvalues = (0.9e1 / 0.4e1*1j) * t660 * (1 + (-2 + t660) * t660) * ((1 + t660) ** (0.3e1 / 0.2e1)) * np.sqrt(0.35e2) * np.exp((-3*1j) * phi1) * ((1 - t660) ** (-0.1e1 / 0.2e1))

    if L == 8:
        t662 = np.cos(phi)
        t661 = np.sin(phi)
        out_tvalues = -(0.9e1 / 0.8e1) * np.exp((-2*1j) * phi1) * np.sqrt(0.10e2) * t661 ** 2 * (7 * t662 ** 2 - 1)

    if L == 9:
        t663 = np.cos(phi)
        out_tvalues = (-0.9e1 / 0.4e1*1j) * np.exp((-1*1j) * phi1) * np.sqrt(0.5e1) * np.sqrt((1 + t663)) * t663 * np.sqrt((1 - t663)) * (7 * t663 ** 2 - 3)

    if L == 10:
        t668 = np.cos(phi)
        t669 = t668 ** 2
        out_tvalues = 0.27e2 / 0.8e1 + (-0.135e3 / 0.4e1 + 0.315e3 / 0.8e1 * t669) * t669

    if L == 11:
        t671 = np.cos(phi)
        out_tvalues = (-0.9e1 / 0.4e1*1j) * np.exp((1j) * phi1) * np.sqrt(0.5e1) * np.sqrt((1 - t671)) * np.sqrt((1 + t671)) * t671 * (7 * t671 ** 2 - 3)

    if L == 12:
        t673 = np.cos(phi)
        t672 = np.sin(phi)
        out_tvalues = -(0.9e1 / 0.8e1) * np.exp((2*1j) * phi1) * np.sqrt(0.10e2) * t672 ** 2 * (7 * t673 ** 2 - 1)

    if L == 13:
        t674 = np.cos(phi)
        out_tvalues = (0.9e1 / 0.4e1*1j) * np.exp((3*1j) * phi1) * np.sqrt(0.35e2) * ((1 - t674) ** (0.3e1 / 0.2e1)) * ((1 + t674) ** (0.3e1 / 0.2e1)) * t674

    if L == 14:
        t677 = np.sin(phi)
        t675 = t677 ** 2
        out_tvalues = (0.9e1 / 0.16e2) * np.exp((4*1j) * phi1) * np.sqrt(0.70e2) * t675 ** 2

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
    tvals, indxvec = gsh(np.array([[.1], [.2], [.3]]), 1)
    print tvals
    print indxvec

