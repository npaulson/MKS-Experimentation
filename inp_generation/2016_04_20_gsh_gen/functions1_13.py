        if Bindx == 0:
            tfunc[..., c] = 1

        if Bindx == 1:
            t5 = np.sqrt(0.2e1)
            t4 = np.cos(phi)
            t3 = t4 ** 2
            t2 = t3 ** 2
            tfunc[..., c] = 0.9e1 / 0.304e3 * t5 * np.sqrt(0.19e2) * np.sqrt(0.7e1) * ((70 * t2) - (60 * t3) + 0.6e1 + (5 * t2 - 10 * t3 + 5) * t5 * np.cos((4 * phi2)))

        if Bindx == 2:
            t14 = np.cos(phi)
            t12 = t14 ** 2
            t16 = t12 ** 2
            t19 = -1 + 2 * t12 - t16
            t11 = t14 * t12
            t9 = t14 * t16
            t18 = t14 + t9 - 2 * t11
            tfunc[..., c] = 0.3e1 / 0.16e2 * np.sqrt(0.7e1) * np.sqrt(0.3e1) * np.sqrt(0.5e1) * np.sqrt(0.2e1) * ((-20 * t11 + 6 * t14 + 14 * t9) * np.sin(phi1) + (t18 + t19) * np.sin(phi1 - (4 * phi2)) + (t18 - t19) * np.sin(phi1 + (4 * phi2))) * ((1 + t14) ** (-0.1e1 / 0.2e1)) * ((1 - t14) ** (-0.1e1 / 0.2e1))

        if Bindx == 3:
            t25 = np.cos(phi)
            t27 = t25 ** 2
            t23 = t27 ** 2
            t31 = -1 + t23
            t30 = 2 * (-t27 + 1) * t25
            t26 = 2 * phi1
            tfunc[..., c] = -0.3e1 / 0.16e2 * np.sqrt(0.5e1) * np.sqrt(0.21e2) * ((14 * t23 - 16 * t27 + 2) * np.cos(t26) + (t30 + t31) * np.cos(-t26 + (4 * phi2)) + (-t30 + t31) * np.cos(t26 + (4 * phi2)))

        if Bindx == 4:
            t39 = np.cos(phi)
            t38 = t39 ** 2
            t42 = t38 ** 2
            t45 = 1 + 2 * t38 - 3 * t42
            t35 = t39 * t42
            t37 = t39 * t38
            t44 = t35 + 2 * t37 - 3 * t39
            t40 = 3 * phi1
            tfunc[..., c] = -0.3e1 / 0.16e2 * np.sqrt(0.2e1) * np.sqrt(0.3e1) * np.sqrt(0.5e1) * (0.14e2 * (t35 - 2 * t37 + t39) * np.sin(t40) - (t44 + t45) * np.sin(-t40 + (4 * phi2)) + (t44 - t45) * np.sin(t40 + (4 * phi2))) * ((1 + t39) ** (-0.1e1 / 0.2e1)) * ((1 - t39) ** (-0.1e1 / 0.2e1))

        if Bindx == 5:
            t52 = np.cos(phi)
            t51 = t52 ** 2
            t56 = 4 * (-t51 - 1) * t52
            t49 = t51 ** 2
            t55 = 1 + t49 + 6 * t51
            tfunc[..., c] = 0.3e1 / 0.32e2 * np.sqrt(0.5e1) * np.sqrt(0.3e1) * ((14 * t49 - 28 * t51 + 14) * np.cos((4 * phi1)) + (t55 + t56) * np.cos((4 * phi1 - 4 * phi2)) + (t55 - t56) * np.cos((4 * phi1 + 4 * phi2)))

        if Bindx == 6:
            t61 = np.cos(phi)
            t60 = t61 ** 2
            t63 = t60 ** 2
            t65 = 0.1001e4 / 0.16e2 * t60 * t63
            tfunc[..., c] = (t65 - 0.1365e4 / 0.16e2 * t63 + 0.455e3 / 0.16e2 * t60 - 0.65e2 / 0.48e2) * np.sqrt(0.2e1) + (-t65 + 0.2093e4 / 0.16e2 * t63 - 0.1183e4 / 0.16e2 * t60 + 0.91e2 / 0.16e2) * np.cos((4 * phi2))

        if Bindx == 7:
            t75 = np.cos(phi)
            t73 = t75 ** 2
            t77 = t73 ** 2
            t76 = t75 * t73
            t79 = t76 ** 2
            t82 = 2 - 26 * t73 + 46 * t77 - 22 * t79
            t68 = t75 * t79
            t70 = t75 * t77
            t81 = -33 * t68 + 79 * t70 + 13 * t75 - 59 * t76
            tfunc[..., c] = 0.13e2 / 0.64e2 * np.sqrt(0.3e1) * np.sqrt(0.14e2) * ((66 * t68 - 126 * t70 + 70 * t76 - 10 * t75) * np.sin(phi1) + (t81 - t82) * np.sin(phi1 - (4 * phi2)) + (t81 + t82) * np.sin(phi1 + (4 * phi2))) * ((1 + t75) ** (-0.1e1 / 0.2e1)) * ((1 - t75) ** (-0.1e1 / 0.2e1))

        if Bindx == 8:
            t91 = np.cos(phi)
            t90 = t91 ** 2
            t93 = t91 * t90
            t94 = t90 ** 2
            t98 = 64 * t93 + (-44 * t94 - 20) * t91
            t86 = t93 ** 2
            t97 = -1 + 33 * t86 + 11 * t90 - 43 * t94
            t92 = 2 * phi1
            tfunc[..., c] = 0.13e2 / 0.128e3 * np.sqrt(0.7e1) * np.sqrt(0.15e2) * ((-66 * t86 + 102 * t94 - 38 * t90 + 2) * np.cos(t92) + (t97 + t98) * np.cos(-t92 + (4 * phi2)) + (t97 - t98) * np.cos(t92 + (4 * phi2)))

        if Bindx == 9:
            t108 = np.cos(phi)
            t107 = t108 ** 2
            t111 = t107 ** 2
            t110 = t108 * t107
            t113 = t110 ** 2
            t116 = 2 - 18 * t107 + 38 * t111 - 22 * t113
            t102 = t108 * t113
            t104 = t108 * t111
            t115 = 11 * t102 - 9 * t104 + 5 * t108 - 7 * t110
            t109 = 3 * phi1
            tfunc[..., c] = 0.13e2 / 0.64e2 * np.sqrt(0.7e1) * np.sqrt(0.15e2) * ((-22 * t102 + 50 * t104 - 34 * t110 + 6 * t108) * np.sin(t109) + (t115 - t116) * np.sin(t109 + (4 * phi2)) - (t115 + t116) * np.sin(-t109 + (4 * phi2))) * ((1 + t108) ** (-0.1e1 / 0.2e1)) * ((1 - t108) ** (-0.1e1 / 0.2e1))

        if Bindx == 10:
            t125 = np.cos(phi)
            t124 = t125 ** 2
            t126 = t125 * t124
            t127 = t124 ** 2
            t131 = 80 * t126 + (-88 * t127 - 8) * t125
            t120 = t126 ** 2
            t130 = 13 + 33 * t120 - 65 * t124 + 35 * t127
            tfunc[..., c] = -0.13e2 / 0.128e3 * np.sqrt(0.14e2) * ((-66 * t120 + 138 * t127 - 78 * t124 + 6) * np.cos((4 * phi1)) + (t130 + t131) * np.cos((4 * phi1 - 4 * phi2)) + (t130 - t131) * np.cos((4 * phi1 + 4 * phi2)))

        if Bindx == 11:
            t141 = np.cos(phi)
            t140 = t141 ** 2
            t144 = t140 ** 2
            t143 = t141 * t140
            t146 = t143 ** 2
            t149 = -2 + 2 * t140 + 10 * t144 - 10 * t146
            t135 = t141 * t146
            t137 = t141 * t144
            t148 = -3 * t135 - 7 * t137 - 5 * t141 + 15 * t143
            t142 = 5 * phi1
            tfunc[..., c] = 0.13e2 / 0.64e2 * np.sqrt(0.7e1) * np.sqrt(0.11e2) * (0.6e1 * (t135 - 3 * t137 + 3 * t143 - t141) * np.sin(t142) - (t148 - t149) * np.sin(-t142 + (4 * phi2)) + (t148 + t149) * np.sin(t142 + (4 * phi2))) * ((1 + t141) ** (-0.1e1 / 0.2e1)) * ((1 - t141) ** (-0.1e1 / 0.2e1))

        if Bindx == 12:
            t157 = np.cos(phi)
            t156 = t157 ** 2
            t159 = t156 ** 2
            t160 = t157 * t159
            t163 = 4 * t157 - 4 * t160
            t153 = t157 * t160
            t162 = -1 + t153 - 5 * t156 + 5 * t159
            t158 = 6 * phi1
            tfunc[..., c] = 0.13e2 / 0.128e3 * np.sqrt(0.7e1) * np.sqrt(0.33e2) * ((-2 * t153 + 6 * t159 - 6 * t156 + 2) * np.cos(t158) + (t162 + t163) * np.cos(-t158 + (4 * phi2)) + (t162 - t163) * np.cos(t158 + (4 * phi2)))


