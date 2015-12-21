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
                        [2, 2, 2]])

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
            t300 = np.cos(phi)
            tfunc[..., c] = (-0.3e1 / 0.2e1*1j) * np.exp((-1*1j) * phi1) * np.sqrt(0.2e1) * np.sqrt((1 + t300)) * np.sqrt((1 - t300))

        if Bindx == 3:
            tfunc[..., c] = (0.3e1 / 0.2e1) * (-0.1e1 + np.cos(phi)) * np.exp((-1*1j) * (phi1 - phi2))

        if Bindx == 4:
            t301 = np.cos(phi)
            tfunc[..., c] = (-0.3e1 / 0.2e1*1j) * np.exp((-1*1j) * phi2) * np.sqrt(0.2e1) * np.sqrt((1 - t301)) * np.sqrt((1 + t301))

        if Bindx == 5:
            tfunc[..., c] = 0.3e1 * np.cos(phi)

        if Bindx == 6:
            t302 = np.cos(phi)
            tfunc[..., c] = (-0.3e1 / 0.2e1*1j) * np.exp((1j) * phi2) * np.sqrt(0.2e1) * np.sqrt((1 - t302)) * np.sqrt((1 + t302))

        if Bindx == 7:
            tfunc[..., c] = (0.3e1 / 0.2e1) * (-0.1e1 + np.cos(phi)) * np.exp((1j) * (phi1 - phi2))

        if Bindx == 8:
            t303 = np.cos(phi)
            tfunc[..., c] = (-0.3e1 / 0.2e1*1j) * np.exp((1j) * phi1) * np.sqrt(0.2e1) * np.sqrt((1 - t303)) * np.sqrt((1 + t303))

        if Bindx == 9:
            tfunc[..., c] = (0.3e1 / 0.2e1) * (0.1e1 + np.cos(phi)) * np.exp((1j) * (phi1 + phi2))

        if Bindx == 10:
            t304 = np.cos(phi)
            tfunc[..., c] = (0.5e1 / 0.4e1) * np.exp((-2*1j) * (phi1 + phi2)) * (1 + (2 + t304) * t304)

        if Bindx == 11:
            t305 = np.cos(phi)
            tfunc[..., c] = (-0.5e1 / 0.2e1*1j) * np.exp((-1*1j) * (2 * phi1 + phi2)) * ((1 + t305) ** (0.3e1 / 0.2e1)) * np.sqrt((1 - t305))

        if Bindx == 12:
            t306 = np.sin(phi)
            tfunc[..., c] = -(0.5e1 / 0.4e1) * np.exp((-2*1j) * phi1) * np.sqrt(0.6e1) * t306 ** 2

        if Bindx == 13:
            t307 = np.cos(phi)
            tfunc[..., c] = (0.5e1 / 0.2e1*1j) * np.exp((-1*1j) * (2 * phi1 - phi2)) * ((1 - t307) ** (0.3e1 / 0.2e1)) * np.sqrt((1 + t307))

        if Bindx == 14:
            t308 = np.cos(phi)
            tfunc[..., c] = (0.5e1 / 0.4e1) * np.exp((-2*1j) * (phi1 - phi2)) * (1 + (-2 + t308) * t308)

        if Bindx == 15:
            t309 = np.cos(phi)
            tfunc[..., c] = (-0.5e1 / 0.2e1*1j) * np.exp((-1*1j) * (phi1 + 2 * phi2)) * np.sqrt((1 - t309)) * ((1 + t309) ** (0.3e1 / 0.2e1))

        if Bindx == 16:
            t310 = np.cos(phi)
            tfunc[..., c] = (0.5e1 / 0.2e1) * np.exp((-1*1j) * (phi1 + phi2)) * (2 * t310 ** 2 + t310 - 1)

        if Bindx == 17:
            t311 = np.cos(phi)
            tfunc[..., c] = (-0.5e1 / 0.2e1*1j) * np.exp((-1*1j) * phi1) * np.sqrt(0.6e1) * np.sqrt((1 + t311)) * t311 * np.sqrt((1 - t311))

        if Bindx == 18:
            t312 = np.cos(phi)
            tfunc[..., c] = (0.5e1 / 0.2e1) * np.exp((-1*1j) * (phi1 - phi2)) * (2 * t312 ** 2 - t312 - 1)

        if Bindx == 19:
            t313 = np.cos(phi)
            tfunc[..., c] = (0.5e1 / 0.2e1*1j) * np.exp((-1*1j) * (phi1 - 2 * phi2)) * ((1 - t313) ** (0.3e1 / 0.2e1)) * np.sqrt((1 + t313))

        if Bindx == 20:
            t314 = np.sin(phi)
            tfunc[..., c] = -(0.5e1 / 0.4e1) * np.exp((-2*1j) * phi2) * np.sqrt(0.6e1) * t314 ** 2

        if Bindx == 21:
            t315 = np.cos(phi)
            tfunc[..., c] = (-0.5e1 / 0.2e1*1j) * np.exp((-1*1j) * phi2) * np.sqrt(0.6e1) * np.sqrt((1 - t315)) * np.sqrt((1 + t315)) * t315

        if Bindx == 22:
            t316 = np.cos(phi)
            tfunc[..., c] = 0.15e2 / 0.2e1 * t316 ** 2 - 0.5e1 / 0.2e1

        if Bindx == 23:
            t317 = np.cos(phi)
            tfunc[..., c] = (-0.5e1 / 0.2e1*1j) * np.exp((1j) * phi2) * np.sqrt(0.6e1) * np.sqrt((1 + t317)) * t317 * np.sqrt((1 - t317))

        if Bindx == 24:
            t318 = np.sin(phi)
            tfunc[..., c] = -(0.5e1 / 0.4e1) * np.exp((2*1j) * phi2) * np.sqrt(0.6e1) * t318 ** 2

        if Bindx == 25:
            t319 = np.cos(phi)
            tfunc[..., c] = (0.5e1 / 0.2e1*1j) * np.exp((1j) * (phi1 - 2 * phi2)) * ((1 - t319) ** (0.3e1 / 0.2e1)) * np.sqrt((1 + t319))

        if Bindx == 26:
            t320 = np.cos(phi)
            tfunc[..., c] = (0.5e1 / 0.2e1) * np.exp((1j) * (phi1 - phi2)) * (2 * t320 ** 2 - t320 - 1)

        if Bindx == 27:
            t321 = np.cos(phi)
            tfunc[..., c] = (-0.5e1 / 0.2e1*1j) * np.exp((1j) * phi1) * np.sqrt(0.6e1) * np.sqrt((1 - t321)) * np.sqrt((1 + t321)) * t321

        if Bindx == 28:
            t322 = np.cos(phi)
            tfunc[..., c] = (0.5e1 / 0.2e1) * np.exp((1j) * (phi1 + phi2)) * (2 * t322 ** 2 + t322 - 1)

        if Bindx == 29:
            t323 = np.cos(phi)
            tfunc[..., c] = (-0.5e1 / 0.2e1*1j) * np.exp((1j) * (phi1 + 2 * phi2)) * np.sqrt((1 - t323)) * ((1 + t323) ** (0.3e1 / 0.2e1))

        if Bindx == 30:
            t324 = np.cos(phi)
            tfunc[..., c] = (0.5e1 / 0.4e1) * np.exp((2*1j) * (phi1 - phi2)) * (1 + (-2 + t324) * t324)

        if Bindx == 31:
            t325 = np.cos(phi)
            tfunc[..., c] = (0.5e1 / 0.2e1*1j) * np.exp((1j) * (2 * phi1 - phi2)) * ((1 - t325) ** (0.3e1 / 0.2e1)) * np.sqrt((1 + t325))

        if Bindx == 32:
            t326 = np.sin(phi)
            tfunc[..., c] = -(0.5e1 / 0.4e1) * np.exp((2*1j) * phi1) * np.sqrt(0.6e1) * t326 ** 2

        if Bindx == 33:
            t327 = np.cos(phi)
            tfunc[..., c] = (-0.5e1 / 0.2e1*1j) * np.exp((1j) * (2 * phi1 + phi2)) * np.sqrt((1 - t327)) * ((1 + t327) ** (0.3e1 / 0.2e1))

        if Bindx == 34:
            t328 = np.cos(phi)
            tfunc[..., c] = (0.5e1 / 0.4e1) * np.exp((2*1j) * (phi1 + phi2)) * (1 + (2 + t328) * t328)

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

