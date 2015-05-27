import numpy as np


def gsh(e_angles):

    phi1 = e_angles[0, :]
    phi = e_angles[1, :]
    phi2 = e_angles[2, :]

    zvec = np.abs(phi) < 10e-17
    zvec = zvec.astype(int)
    randvec = np.round(np.random.rand(zvec.shape[0]))
    randvecopp = np.ones(zvec.shape[0]) - randvec
    phi += (1e-7)*zvec*(randvec - randvecopp)

    out_tvalues = np.zeros([15, e_angles.shape[1]], dtype = 'complex128')

    t134 = np.cos(phi)
    t127 = 1 + t134
    t156 = t134 * np.sqrt(t127)
    t132 = t134 ** 2
    t129 = 7 * t132
    t155 = t129 - 3
    t154 = (0.1e1 / 0.4e1*1j) * t156
    t128 = 1 - t134
    t141 = np.sqrt(t128)
    t152 = t141 * t156
    t133 = np.sin(phi)
    t131 = t133 ** 2
    t138 = np.sqrt(0.6e1)
    t151 = -t131 * t138 / 0.4e1
    t150 = -(t129 - 1) * t131 * np.sqrt(0.10e2) / 0.8e1
    t149 = t131 ** 2 * np.sqrt(0.70e2) / 0.16e2
    t148 = t127 * np.sqrt(0.35e2) * t154
    t147 = (-0.1e1 / 0.2e1*1j) * t138 * t152
    t139 = np.sqrt(0.5e1)
    t126 = np.exp((-2*1j) * phi1)
    t125 = np.exp((-1*1j) * phi1)
    t124 = np.exp((1j) * phi1)
    t123 = np.exp((2*1j) * phi1)
    t121 = 0.1e1 / t141
    out_tvalues[0, :] = 1
    out_tvalues[1, :] = t126 * t151
    out_tvalues[2, :] = t125 * t147
    out_tvalues[3, :] = 0.3e1 / 0.2e1 * t132 - 0.1e1 / 0.2e1
    out_tvalues[4, :] = t124 * t147
    out_tvalues[5, :] = t123 * t151
    out_tvalues[6, :] = np.exp((-4*1j) * phi1) * t149
    out_tvalues[7, :] = (t132 - 2 * t134 + 1) * np.exp((-3*1j) * phi1) * t121 * t148
    out_tvalues[8, :] = t126 * t150
    out_tvalues[9, :] = t125 * t139 * (t155 * t134 - 7 * t132 + 3) * t121 * t154
    out_tvalues[10, :] = 0.3e1 / 0.8e1 + (-0.15e2 / 0.4e1 + 0.35e2 / 0.8e1 * t132) * t132
    out_tvalues[11, :] = (-0.1e1 / 0.4e1*1j) * t124 * t139 * t155 * t152
    out_tvalues[12, :] = t123 * t150
    out_tvalues[13, :] = np.exp((3*1j) * phi1) * t141 * t128 * t148
    out_tvalues[14, :] = np.exp((4*1j) * phi1) * t149

    return out_tvalues

if __name__ == '__main__':
    tvals = gsh(np.array([[.1], [.2], [.3]]))
    print tvals

