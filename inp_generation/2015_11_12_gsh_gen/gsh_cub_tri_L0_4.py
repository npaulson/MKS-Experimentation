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
            t10734 = np.cos(phi)
            t10733 = t10734 ** 2
            t10738 = 4 * (-t10733 - 1) * t10734
            t10731 = t10733 ** 2
            t10737 = 1 + t10731 + 6 * t10733
            tfunc[..., c] = (0.3e1 / 0.64e2) * np.sqrt(0.3e1) * np.sqrt(0.5e1) * np.sqrt(0.2e1) * ((14 * t10731 - 28 * t10733 + 14) * np.exp((-4*1j) * phi2) + (t10737 - t10738) * np.exp((-4*1j) * (phi1 + phi2)) + (t10737 + t10738) * np.exp((4*1j) * (phi1 - phi2)))

        if Bindx == 2:
            t10746 = 4 * phi1
            t10745 = np.cos(phi)
            t10744 = t10745 ** 2
            t10743 = t10745 * t10744
            t10742 = t10744 ** 2
            tfunc[..., c] = (0.3e1 / 0.16e2*1j) * np.sqrt(0.5e1) * np.sqrt(0.3e1) * np.sqrt((1 + t10745)) * ((1 - t10745) ** (-0.1e1 / 0.2e1)) * ((t10742 + 2 * t10743 - 2 * t10745 - 1) * np.exp((-1*1j) * (t10746 + 3 * phi2)) + 14 * (t10742 - t10743 - t10744 + t10745) * np.exp((-3*1j) * phi2) + (t10742 - 4 * t10743 + 6 * t10744 - 4 * t10745 + 1) * np.exp((1j) * (t10746 - 3 * phi2)))

        if Bindx == 3:
            t10754 = np.cos(phi)
            t10756 = t10754 ** 2
            t10752 = t10756 ** 2
            t10760 = -1 + t10752
            t10759 = 2 * (-t10756 + 1) * t10754
            t10755 = 2 * phi1
            tfunc[..., c] = (0.3e1 / 0.32e2) * np.sqrt(0.2e1) * np.sqrt(0.5e1) * np.sqrt(0.21e2) * ((14 * t10752 - 16 * t10756 + 2) * np.exp((-2*1j) * phi2) + (-t10759 + t10760) * np.exp((-2*1j) * (t10755 + phi2)) + (t10759 + t10760) * np.exp((2*1j) * (t10755 - phi2)))

        if Bindx == 4:
            t10768 = 4 * phi1
            t10767 = np.cos(phi)
            t10766 = t10767 ** 2
            t10765 = t10767 * t10766
            t10764 = t10766 ** 2
            tfunc[..., c] = (0.3e1 / 0.16e2*1j) * np.sqrt((1 + t10767)) * np.sqrt(0.7e1) * np.sqrt(0.3e1) * np.sqrt(0.5e1) * ((1 - t10767) ** (-0.1e1 / 0.2e1)) * ((t10764 - 2 * t10766 + 1) * np.exp((-1*1j) * (t10768 + phi2)) + (t10764 - 2 * t10765 + 2 * t10767 - 1) * np.exp((1j) * (t10768 - phi2)) + (14 * t10764 - 14 * t10765 - 6 * t10766 + 6 * t10767) * np.exp((-1*1j) * phi2))

        if Bindx == 5:
            t10774 = np.cos(phi)
            t10773 = t10774 ** 2
            t10772 = t10773 ** 2
            tfunc[..., c] = 0.3e1 / 0.16e2 * np.sqrt(0.7e1) * np.sqrt(0.3e1) * ((35 * t10772) - (30 * t10773) + 0.3e1 + (5 * t10772 - 10 * t10773 + 5) * np.cos((4 * phi1)))

        if Bindx == 6:
            t10783 = 4 * phi1
            t10782 = np.cos(phi)
            t10781 = t10782 ** 2
            t10780 = t10782 * t10781
            t10779 = t10781 ** 2
            tfunc[..., c] = (-0.3e1 / 0.16e2*1j) * np.sqrt((1 - t10782)) * np.sqrt(0.7e1) * np.sqrt(0.3e1) * np.sqrt(0.5e1) * ((1 + t10782) ** (-0.1e1 / 0.2e1)) * ((t10779 - 2 * t10781 + 1) * np.exp((-1*1j) * (t10783 - phi2)) + (t10779 + 2 * t10780 - 2 * t10782 - 1) * np.exp((1j) * (t10783 + phi2)) + (14 * t10779 + 14 * t10780 - 6 * t10781 - 6 * t10782) * np.exp((1j) * phi2))

        if Bindx == 7:
            t10791 = np.cos(phi)
            t10793 = t10791 ** 2
            t10789 = t10793 ** 2
            t10797 = -1 + t10789
            t10796 = 2 * (-t10793 + 1) * t10791
            t10792 = 2 * phi1
            tfunc[..., c] = (0.3e1 / 0.32e2) * np.sqrt(0.2e1) * np.sqrt(0.5e1) * np.sqrt(0.21e2) * ((14 * t10789 - 16 * t10793 + 2) * np.exp((2*1j) * phi2) + (t10796 + t10797) * np.exp((-2*1j) * (t10792 - phi2)) + (-t10796 + t10797) * np.exp((2*1j) * (t10792 + phi2)))

        if Bindx == 8:
            t10805 = 4 * phi1
            t10804 = np.cos(phi)
            t10803 = t10804 ** 2
            t10802 = t10804 * t10803
            t10801 = t10803 ** 2
            tfunc[..., c] = (-0.3e1 / 0.16e2*1j) * np.sqrt(0.5e1) * np.sqrt(0.3e1) * np.sqrt((1 - t10804)) * ((1 + t10804) ** (-0.1e1 / 0.2e1)) * ((t10801 - 2 * t10802 + 2 * t10804 - 1) * np.exp((-1*1j) * (t10805 - 3 * phi2)) + 14 * (t10801 + t10802 - t10803 - t10804) * np.exp((3*1j) * phi2) + (t10801 + 4 * t10802 + 6 * t10803 + 4 * t10804 + 1) * np.exp((1j) * (t10805 + 3 * phi2)))

        if Bindx == 9:
            t10814 = np.cos(phi)
            t10813 = t10814 ** 2
            t10818 = 4 * (-t10813 - 1) * t10814
            t10811 = t10813 ** 2
            t10817 = 1 + t10811 + 6 * t10813
            tfunc[..., c] = (0.3e1 / 0.64e2) * np.sqrt(0.3e1) * np.sqrt(0.5e1) * np.sqrt(0.2e1) * ((14 * t10811 - 28 * t10813 + 14) * np.exp((4*1j) * phi2) + (t10817 + t10818) * np.exp((-4*1j) * (phi1 - phi2)) + (t10817 - t10818) * np.exp((4*1j) * (phi1 + phi2)))

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

