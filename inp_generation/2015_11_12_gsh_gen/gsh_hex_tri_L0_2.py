    phi1 = e_angles[0, :]
    phi = e_angles[1, :]
    phi2 = e_angles[2, :]

    zvec = np.abs(phi) < 10e-17
    zvec = zvec.astype(int)
    randvec = np.round(np.random.rand(zvec.shape[0]))
    randvecopp = np.ones(zvec.shape[0]) - randvec
    phi += (1e-7)*zvec*(randvec - randvecopp)

    out_tvalues = np.zeros([6, e_angles.shape[1]], dtype = 'complex128')

    t36 = np.sin(phi)
    t38 = np.sqrt(0.6e1)
    t40 = -0.5e1 / 0.4e1 * t36 ** 2 * t38
    t37 = np.cos(phi)
    t39 = (-0.5e1 / 0.2e1*1j) * np.sqrt((1 + t37)) * np.sqrt((1 - t37)) * t37 * t38
    out_tvalues[0, :] = 1
    out_tvalues[1, :] = np.exp((-2*1j) * phi1) * t40
    out_tvalues[2, :] = np.exp((-1*1j) * phi1) * t39
    out_tvalues[3, :] = 0.15e2 / 0.2e1 * t37 ** 2 - 0.5e1 / 0.2e1
    out_tvalues[4, :] = np.exp((1j) * phi1) * t39
    out_tvalues[5, :] = np.exp((2*1j) * phi1) * t40

    return out_tvalues

if __name__ == '__main__':
    tvals = gsh(np.array([[.1], [.2], [.3]]))
    print tvals

