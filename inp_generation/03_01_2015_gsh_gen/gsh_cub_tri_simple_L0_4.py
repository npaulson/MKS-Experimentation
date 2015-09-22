t43 = np.cos(phi)
t79 = np.sqrt((1 - t43)) * ((1 + t43) ** (-0.1e1 / 0.2e1))
t42 = t43 ** 2
t41 = t43 * t42
t70 = t43 - t41
t40 = t42 ** 2
t78 = 14 * t40
t77 = -1 + t40
t76 = 1 + t40
t46 = np.sqrt(0.5e1)
t47 = np.sqrt(0.3e1)
t75 = t46 * t47
t74 = t46 * np.sqrt(0.2e1)
t73 = t40 - t42
t72 = -4 * t41 - 4 * t43
t71 = 2 * t70
t69 = t78 - 6 * t42
t68 = -14 * t41 + 6 * t43
t67 = 6 * t42 + t76
t66 = -2 * t42 + t76
t65 = t78 - 16 * t42 + 2
t64 = t78 - 28 * t42 + 14
t63 = t71 + t77
t62 = -t71 + t77
t61 = t67 + t72
t60 = t67 - t72
t59 = 0.3e1 / 0.32e2 * np.sqrt(0.21e2) * t74
t58 = 0.3e1 / 0.64e2 * t47 * t74
t57 = (-0.3e1 / 0.16e2*1j) * t75 * t79
t56 = (0.3e1 / 0.16e2*1j) * t75 / t79
t51 = 3 * phi1
t50 = -4 * phi2
t49 = 4 * phi2
t45 = np.sqrt(0.7e1)
t39 = phi1 + t50
t38 = phi1 - 2 * phi2
t37 = phi1 - phi2
t36 = phi1 + phi2
t35 = phi1 + 2 * phi2
t34 = phi1 + t49
t33 = t51 + t50
t32 = t51 + t49
out_tvalues[0, :] = 1
out_tvalues[1, :] = (t64 * np.exp((-4*1j) * phi1) + t61 * np.exp((-4*1j) * t37) + t60 * np.exp((-4*1j) * t36)) * t58
out_tvalues[2, :] = (t62 * np.exp((-1*1j) * t32) + 14 * (t70 + t73) * np.exp((-3*1j) * phi1) + t61 * np.exp((-1*1j) * t33)) * t56
out_tvalues[3, :] = (t65 * np.exp((-2*1j) * phi1) + t63 * np.exp((-2*1j) * t38) + t62 * np.exp((-2*1j) * t35)) * t59
out_tvalues[4, :] = t45 * (t66 * np.exp((-1*1j) * t34) + t63 * np.exp((-1*1j) * t39) + (t68 + t69) * np.exp((-1*1j) * phi1)) * t56
out_tvalues[5, :] = 0.3e1 / 0.16e2 * t45 * t47 * ((35 * t40) - (30 * t42) + 0.3e1 + (5 * t40 - 10 * t42 + 5) * np.cos(t49))
out_tvalues[6, :] = t45 * (t66 * np.exp((1j) * t39) + t62 * np.exp((1j) * t34) + (-t68 + t69) * np.exp((1j) * phi1)) * t57
out_tvalues[7, :] = (t63 * np.exp((2*1j) * t38) + t62 * np.exp((2*1j) * t35) + t65 * np.exp((2*1j) * phi1)) * t59
out_tvalues[8, :] = (t63 * np.exp((1j) * t33) + t60 * np.exp((1j) * t32) + 14 * (-t70 + t73) * np.exp((3*1j) * phi1)) * t57
out_tvalues[9, :] = (t64 * np.exp((4*1j) * phi1) + t61 * np.exp((4*1j) * t37) + t60 * np.exp((4*1j) * t36)) * t58

[0, 0, 1]
[4, -4, 1]
[4, -3, 1]
[4, -2, 1]
[4, -1, 1]
[4, 0, 1]
[4, 1, 1]
[4, 2, 1]
[4, 3, 1]
[4, 4, 1]
