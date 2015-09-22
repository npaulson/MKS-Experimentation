t18 = np.cos(phi)
t14 = 1 + t18
t22 = t14 / 0.2e1
t15 = 1 - t18
t21 = -t15 / 0.2e1
t20 = (-0.1e1 / 0.2e1*1j) * np.sqrt(t14) * np.sqrt(t15) * np.sqrt(0.2e1)
t17 = phi1 - phi2
t16 = phi1 + phi2
out_tvalues[0, :] = 1
out_tvalues[1, :] = np.exp((-1*1j) * t16) * t22
out_tvalues[2, :] = np.exp((-1*1j) * phi1) * t20
out_tvalues[3, :] = np.exp((-1*1j) * t17) * t21
out_tvalues[4, :] = np.exp((-1*1j) * phi2) * t20
out_tvalues[5, :] = t18
out_tvalues[6, :] = np.exp((1j) * phi2) * t20
out_tvalues[7, :] = np.exp((1j) * t17) * t21
out_tvalues[8, :] = np.exp((1j) * phi1) * t20
out_tvalues[9, :] = np.exp((1j) * t16) * t22

[0, 0, 0]
[1, -1, -1]
[1, -1, 0]
[1, -1, 1]
[1, 0, -1]
[1, 0, 0]
[1, 0, 1]
[1, 1, -1]
[1, 1, 0]
[1, 1, 1]
