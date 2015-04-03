import numpy as np


def gsh_hexagonal_triclinic_L0_4(e_angles):
    # NOTE: after MAPLE code generation replace math with np and exp with np.exp

    phi1 = e_angles[0, :]
    phi = e_angles[1, :]
    phi2 = e_angles[2, :]

    zvec = np.abs(phi) < 10e-17
    zvec = zvec.astype(int)
    randvec = np.round(np.random.rand(zvec.shape[0]))
    randvecopp = np.ones(zvec.shape[0]) - randvec
    phi += (1e-7)*zvec*(randvec - randvecopp)

    out_tvalues = np.zeros([15, e_angles.shape[1]], dtype = 'complex128')

    out_tvalues[0, :] = 1
    out_tvalues[1, :] = -exp(complex(0, -2) * phi2) * math.sqrt(0.6e1) * (0.1e1 + math.cos(phi)) * (0.1e1 - math.cos(phi)) / 0.4e1
    out_tvalues[2, :] = complex(0, -0.1e1 / 0.24e2) * exp(complex(0, -1) * phi2) * math.sqrt(0.6e1) * (0.1e1 - math.cos(phi)) ** (-0.1e1 / 0.2e1) * math.sqrt(0.1e1 + math.cos(phi)) * -0.6e1 * (0.1e1 - math.cos(phi)) ** 2 + 0.6e1 * (0.1e1 + math.cos(phi)) * (0.1e1 - math.cos(phi))
    out_tvalues[3, :] = (0.1e1 - math.cos(phi)) ** 2 / 0.4e1 - (0.1e1 + math.cos(phi)) * (0.1e1 - math.cos(phi)) + (0.1e1 + math.cos(phi)) ** 2 / 0.4e1
    out_tvalues[4, :] = complex(0, 0.1e1 / 0.24e2) * exp(complex(0, 1) * phi2) * math.sqrt(0.6e1) * math.sqrt(0.1e1 - math.cos(phi)) * (0.1e1 + math.cos(phi)) ** (-0.1e1 / 0.2e1) * 0.6e1 * (0.1e1 + math.cos(phi)) * (0.1e1 - math.cos(phi)) - 0.6e1 * (0.1e1 + math.cos(phi)) ** 2
    out_tvalues[5, :] = -exp(complex(0, 2) * phi2) * math.sqrt(0.6e1) * (0.1e1 + math.cos(phi)) * (0.1e1 - math.cos(phi)) / 0.4e1
    out_tvalues[6, :] = exp(complex(0, -4) * phi2) * math.sqrt(0.70e2) * (0.1e1 + math.cos(phi)) ** 2 * (0.1e1 - math.cos(phi)) ** 2 / 0.16e2
    out_tvalues[7, :] = complex(0, 0.1e1 / 0.6720e4) * exp(complex(0, -3) * phi2) * math.sqrt(0.35e2) * (0.1e1 - math.cos(phi)) ** (-0.3e1 / 0.2e1) * (0.1e1 + math.cos(phi)) ** (0.3e1 / 0.2e1) * -0.840e3 * (0.1e1 - math.cos(phi)) ** 4 + 0.840e3 * (0.1e1 + math.cos(phi)) * (0.1e1 - math.cos(phi)) ** 3
    out_tvalues[8, :] = -exp(complex(0, -2) * phi2) * math.sqrt(0.10e2) * (0.1e1 + math.cos(phi)) / (0.1e1 - math.cos(phi)) * (0.360e3 * (0.1e1 - math.cos(phi)) ** 4 - 0.960e3 * (0.1e1 + math.cos(phi)) * (0.1e1 - math.cos(phi)) ** 3 + 0.360e3 * (0.1e1 + math.cos(phi)) ** 2 * (0.1e1 - math.cos(phi)) ** 2) / 0.1920e4
    out_tvalues[9, :] = complex(0, -0.1e1 / 0.960e3) * exp(complex(0, -1) * phi2) * math.sqrt(0.5e1) * (0.1e1 - math.cos(phi)) ** (-0.1e1 / 0.2e1) * math.sqrt(0.1e1 + math.cos(phi)) * -0.120e3 * (0.1e1 - math.cos(phi)) ** 4 + 0.720e3 * (0.1e1 + math.cos(phi)) * (0.1e1 - math.cos(phi)) ** 3 - 0.720e3 * (0.1e1 + math.cos(phi)) ** 2 * (0.1e1 - math.cos(phi)) ** 2 + 0.120e3 * (0.1e1 + math.cos(phi)) ** 3 * (0.1e1 - math.cos(phi))
    out_tvalues[10, :] = (0.1e1 - math.cos(phi)) ** 4 / 0.16e2 - (0.1e1 + math.cos(phi)) * (0.1e1 - math.cos(phi)) ** 3 + 0.9e1 / 0.4e1 * (0.1e1 + math.cos(phi)) ** 2 * (0.1e1 - math.cos(phi)) ** 2 - (0.1e1 + math.cos(phi)) ** 3 * (0.1e1 - math.cos(phi)) + (0.1e1 + math.cos(phi)) ** 4 / 0.16e2
    out_tvalues[11, :] = complex(0, 0.1e1 / 0.960e3) * exp(complex(0, 1) * phi2) * math.sqrt(0.5e1) * math.sqrt(0.1e1 - math.cos(phi)) * (0.1e1 + math.cos(phi)) ** (-0.1e1 / 0.2e1) * 0.120e3 * (0.1e1 + math.cos(phi)) * (0.1e1 - math.cos(phi)) ** 3 - 0.720e3 * (0.1e1 + math.cos(phi)) ** 2 * (0.1e1 - math.cos(phi)) ** 2 + 0.720e3 * (0.1e1 + math.cos(phi)) ** 3 * (0.1e1 - math.cos(phi)) - 0.120e3 * (0.1e1 + math.cos(phi)) ** 4
    out_tvalues[12, :] = -exp(complex(0, 2) * phi2) * math.sqrt(0.10e2) / (0.1e1 + math.cos(phi)) * (0.1e1 - math.cos(phi)) * (0.360e3 * (0.1e1 + math.cos(phi)) ** 2 * (0.1e1 - math.cos(phi)) ** 2 - 0.960e3 * (0.1e1 + math.cos(phi)) ** 3 * (0.1e1 - math.cos(phi)) + 0.360e3 * (0.1e1 + math.cos(phi)) ** 4) / 0.1920e4
    out_tvalues[13, :] = complex(0, -0.1e1 / 0.6720e4) * exp(complex(0, 3) * phi2) * math.sqrt(0.35e2) * (0.1e1 - math.cos(phi)) ** (0.3e1 / 0.2e1) * (0.1e1 + math.cos(phi)) ** (-0.3e1 / 0.2e1) * 0.840e3 * (0.1e1 + math.cos(phi)) ** 3 * (0.1e1 - math.cos(phi)) - 0.840e3 * (0.1e1 + math.cos(phi)) ** 4
    out_tvalues[14, :] = exp(complex(0, 4) * phi2) * math.sqrt(0.70e2) * (0.1e1 + math.cos(phi)) ** 2 * (0.1e1 - math.cos(phi)) ** 2 / 0.16e2

    return out_tvalues
