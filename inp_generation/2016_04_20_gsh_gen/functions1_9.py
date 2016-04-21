        if Bindx == 0:
            tfunc[..., c] = 1

        if Bindx == 1:
            t1 = np.cos(phi)
            tfunc[..., c] = 0.15e2 / 0.2e1 * t1 ** 2 - 0.5e1 / 0.2e1

        if Bindx == 2:
            t3 = np.cos(phi)
            t2 = np.sin(phi)
            tfunc[..., c] = -0.5e1 * np.sqrt(0.3e1) * t3 * t2 ** 2 * np.sin(phi1) * ((1 - t3) ** (-0.1e1 / 0.2e1)) * ((1 + t3) ** (-0.1e1 / 0.2e1))

        if Bindx == 3:
            t4 = np.cos(phi)
            tfunc[..., c] = -0.5e1 / 0.2e1 * np.sqrt(0.3e1) * (t4 ** 2 - 1) * np.cos((2 * phi1))

        if Bindx == 4:
            t5 = np.cos(phi)
            t6 = t5 ** 2
            tfunc[..., c] = 0.27e2 / 0.8e1 + (-0.135e3 / 0.4e1 + 0.315e3 / 0.8e1 * t6) * t6

        if Bindx == 5:
            t9 = np.cos(phi)
            t8 = np.sin(phi)
            tfunc[..., c] = -0.9e1 / 0.4e1 * np.sqrt(0.2e1) * np.sqrt(0.5e1) * t9 * t8 ** 2 * (7 * t9 ** 2 - 3) * np.sin(phi1) * ((1 + t9) ** (-0.1e1 / 0.2e1)) * ((1 - t9) ** (-0.1e1 / 0.2e1))

        if Bindx == 6:
            t10 = np.cos(phi)
            t11 = t10 ** 2
            tfunc[..., c] = -0.9e1 / 0.4e1 * np.sqrt(0.5e1) * (1 + (-8 + 7 * t11) * t11) * np.cos((2 * phi1))

        if Bindx == 7:
            t16 = np.sin(phi)
            t14 = t16 ** 2
            t13 = np.cos(phi)
            tfunc[..., c] = -0.9e1 / 0.4e1 * np.sqrt(0.2e1) * np.sqrt(0.35e2) * t13 * t14 ** 2 * np.sin((3 * phi1)) * ((1 + t13) ** (-0.1e1 / 0.2e1)) * ((1 - t13) ** (-0.1e1 / 0.2e1))

        if Bindx == 8:
            t17 = np.cos(phi)
            t18 = t17 ** 2
            tfunc[..., c] = 0.9e1 / 0.8e1 * np.sqrt(0.35e2) * np.cos((4 * phi1)) * (1 + (-2 + t18) * t18)


