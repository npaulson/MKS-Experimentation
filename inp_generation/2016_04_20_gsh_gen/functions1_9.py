        if Bindx == 0:
            t3 = np.sin(phi)
            t1 = t3 ** 2
            tfunc[..., c] = (0.9e1 / 0.16e2) * np.exp((-4*1j) * phi1) * np.sqrt(0.70e2) * t1 ** 2

        if Bindx == 1:
            t4 = np.cos(phi)
            tfunc[..., c] = (0.9e1 / 0.4e1*1j) * t4 * (1 + (-2 + t4) * t4) * ((1 + t4) ** (0.3e1 / 0.2e1)) * np.sqrt(0.35e2) * np.exp((-3*1j) * phi1) * ((1 - t4) ** (-0.1e1 / 0.2e1))

        if Bindx == 2:
            t6 = np.cos(phi)
            t5 = np.sin(phi)
            tfunc[..., c] = -(0.9e1 / 0.8e1) * np.exp((-2*1j) * phi1) * np.sqrt(0.10e2) * t5 ** 2 * (7 * t6 ** 2 - 1)

        if Bindx == 3:
            t7 = np.cos(phi)
            tfunc[..., c] = (-0.9e1 / 0.4e1*1j) * np.exp((-1*1j) * phi1) * np.sqrt(0.5e1) * np.sqrt((1 + t7)) * t7 * np.sqrt((1 - t7)) * (7 * t7 ** 2 - 3)

        if Bindx == 4:
            t12 = np.cos(phi)
            t13 = t12 ** 2
            tfunc[..., c] = 0.27e2 / 0.8e1 + (-0.135e3 / 0.4e1 + 0.315e3 / 0.8e1 * t13) * t13

        if Bindx == 5:
            t15 = np.cos(phi)
            tfunc[..., c] = (-0.9e1 / 0.4e1*1j) * np.exp((1j) * phi1) * np.sqrt(0.5e1) * np.sqrt((1 - t15)) * np.sqrt((1 + t15)) * t15 * (7 * t15 ** 2 - 3)

        if Bindx == 6:
            t17 = np.cos(phi)
            t16 = np.sin(phi)
            tfunc[..., c] = -(0.9e1 / 0.8e1) * np.exp((2*1j) * phi1) * np.sqrt(0.10e2) * t16 ** 2 * (7 * t17 ** 2 - 1)

        if Bindx == 7:
            t18 = np.cos(phi)
            tfunc[..., c] = (0.9e1 / 0.4e1*1j) * np.exp((3*1j) * phi1) * np.sqrt(0.35e2) * ((1 - t18) ** (0.3e1 / 0.2e1)) * ((1 + t18) ** (0.3e1 / 0.2e1)) * t18

        if Bindx == 8:
            t21 = np.sin(phi)
            t19 = t21 ** 2
            tfunc[..., c] = (0.9e1 / 0.16e2) * np.exp((4*1j) * phi1) * np.sqrt(0.70e2) * t19 ** 2


