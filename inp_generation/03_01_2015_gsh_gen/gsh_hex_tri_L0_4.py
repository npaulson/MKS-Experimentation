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

    t17 = np.cos(phi)
    t10 = 1 + t17
    t39 = t17 * np.sqrt(t10)
    t15 = t17 ** 2
    t12 = 7 * t15
    t38 = t12 - 3
    t37 = (0.9e1 / 0.4e1*1j) * t39
    t11 = 1 - t17
    t24 = np.sqrt(t11)
    t35 = t24 * t39
    t16 = np.sin(phi)
    t14 = t16 ** 2
    t21 = np.sqrt(0.6e1)
    t34 = -0.5e1 / 0.4e1 * t14 * t21
    t33 = -0.9e1 / 0.8e1 * t14 * np.sqrt(0.10e2) * (t12 - 1)
    t32 = t10 * np.sqrt(0.35e2) * t37
    t31 = 0.9e1 / 0.16e2 * t14 ** 2 * np.sqrt(0.70e2)
    t30 = (-0.5e1 / 0.2e1*1j) * t21 * t35
    t22 = np.sqrt(0.5e1)
    t9 = np.exp((-2*1j) * phi1)
    t8 = np.exp((-1*1j) * phi1)
    t7 = np.exp((1j) * phi1)
    t6 = np.exp((2*1j) * phi1)
    t4 = 0.1e1 / t24
    out_tvalues[0, :] = 1
    out_tvalues[1, :] = t9 * t34
    out_tvalues[2, :] = t8 * t30
    out_tvalues[3, :] = 0.15e2 / 0.2e1 * t15 - 0.5e1 / 0.2e1
    out_tvalues[4, :] = t7 * t30
    out_tvalues[5, :] = t6 * t34
    out_tvalues[6, :] = np.exp((-4*1j) * phi1) * t31
    out_tvalues[7, :] = (t15 - 2 * t17 + 1) * np.exp((-3*1j) * phi1) * t4 * t32
    out_tvalues[8, :] = t9 * t33
    out_tvalues[9, :] = t8 * t22 * (t17 * t38 - 7 * t15 + 3) * t4 * t37
    out_tvalues[10, :] = 0.27e2 / 0.8e1 + (-0.135e3 / 0.4e1 + 0.315e3 / 0.8e1 * t15) * t15
    out_tvalues[11, :] = (-0.9e1 / 0.4e1*1j) * t7 * t22 * t38 * t35
    out_tvalues[12, :] = t6 * t33
    out_tvalues[13, :] = np.exp((3*1j) * phi1) * t24 * t11 * t32
    out_tvalues[14, :] = np.exp((4*1j) * phi1) * t31

    return out_tvalues

if __name__ == '__main__':
    tvals = gsh(np.array([[.1], [.2], [.3]]))
    print tvals

