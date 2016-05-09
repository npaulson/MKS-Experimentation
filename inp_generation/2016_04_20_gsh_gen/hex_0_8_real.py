import numpy as np


def gsh_basis_info():

    indxvec = np.array([[0, 0, 1],
                        [2, 0, 1],
                        [2, 1, 1],
                        [2, 2, 1],
                        [4, 0, 1],
                        [4, 1, 1],
                        [4, 2, 1],
                        [4, 3, 1],
                        [4, 4, 1],
                        [6, 0, 1],
                        [6, 0, 2],
                        [6, 1, 1],
                        [6, 1, 2],
                        [6, 2, 1],
                        [6, 2, 2],
                        [6, 3, 1],
                        [6, 3, 2],
                        [6, 4, 1],
                        [6, 4, 2],
                        [6, 5, 1],
                        [6, 5, 2],
                        [6, 6, 1],
                        [6, 6, 2],
                        [7, 0, 1],
                        [7, 1, 1],
                        [7, 2, 1],
                        [7, 3, 1],
                        [7, 4, 1],
                        [7, 5, 1],
                        [7, 6, 1],
                        [7, 7, 1],
                        [8, 0, 1],
                        [8, 0, 2],
                        [8, 1, 1],
                        [8, 1, 2],
                        [8, 2, 1],
                        [8, 2, 2],
                        [8, 3, 1],
                        [8, 3, 2],
                        [8, 4, 1],
                        [8, 4, 2],
                        [8, 5, 1],
                        [8, 5, 2],
                        [8, 6, 1],
                        [8, 6, 2],
                        [8, 7, 1],
                        [8, 7, 2],
                        [8, 8, 1],
                        [8, 8, 2]])

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
            t1 = np.cos(phi)
            tfunc[..., c] = 0.15e2 / 0.2e1 * t1 ** 2 - 0.5e1 / 0.2e1

        if Bindx == 2:
            t3 = np.cos(phi)
            t2 = np.sin(phi)
            tfunc[..., c] = -0.5e1 * np.sqrt(0.3e1) * t3 * t2 ** 2 * np.sin(phi1) * ((1 + t3) ** (-0.1e1 / 0.2e1)) * ((1 - t3) ** (-0.1e1 / 0.2e1))

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

        if Bindx == 9:
            t20 = np.cos(phi)
            t21 = t20 ** 2
            t22 = t21 ** 2
            tfunc[..., c] = -0.4095e4 / 0.16e2 * t22 - 0.65e2 / 0.16e2 + (0.3003e4 / 0.16e2 * t22 + 0.1365e4 / 0.16e2) * t21

        if Bindx == 10:
            t24 = np.cos(phi)
            t25 = t24 ** 2
            t26 = t25 ** 2
            tfunc[..., c] = -0.13e2 / 0.32e2 * np.sqrt(0.2e1) * np.sqrt(0.231e3) * np.cos((6 * phi2)) * (-3 * t26 - 1 + (t26 + 3) * t25)

        if Bindx == 11:
            t29 = np.cos(phi)
            t30 = t29 ** 2
            t28 = np.sin(phi)
            tfunc[..., c] = -0.13e2 / 0.8e1 * np.sqrt(0.21e2) * t29 * t28 ** 2 * (5 + (-30 + 33 * t30) * t30) * np.sin(phi1) * ((1 + t29) ** (-0.1e1 / 0.2e1)) * ((1 - t29) ** (-0.1e1 / 0.2e1))

        if Bindx == 12:
            t38 = np.cos(phi)
            t37 = t38 ** 2
            t44 = 1 + (-2 + t37) * t37
            t42 = t44 * t38
            tfunc[..., c] = 0.39e2 / 0.32e2 * np.sqrt(0.22e2) * np.sqrt((1 - t38)) * np.sqrt((1 + t38)) * ((t42 - t44) * np.sin((phi1 - 6 * phi2)) + (t42 + t44) * np.sin((phi1 + 6 * phi2)))

        if Bindx == 13:
            t45 = np.cos(phi)
            t46 = t45 ** 2
            t47 = t46 ** 2
            tfunc[..., c] = -0.13e2 / 0.32e2 * np.sqrt(0.2e1) * np.sqrt(0.105e3) * (-51 * t47 - 1 + (33 * t47 + 19) * t46) * np.cos((2 * phi1))

        if Bindx == 14:
            t56 = np.cos(phi)
            t55 = t56 ** 2
            t58 = t56 * t55
            t59 = t55 ** 2
            t63 = -2 * t56 * t59 - 2 * t56 + 4 * t58
            t62 = t58 ** 2 - t55 - t59 + 1
            t57 = 2 * phi1
            tfunc[..., c] = 0.39e2 / 0.64e2 * np.sqrt(0.55e2) * ((t62 + t63) * np.cos((-t57 + 6 * phi2)) + (t62 - t63) * np.cos((t57 + 6 * phi2)))

        if Bindx == 15:
            t67 = np.sin(phi)
            t65 = t67 ** 2
            t64 = np.cos(phi)
            tfunc[..., c] = -0.13e2 / 0.16e2 * np.sqrt(0.2e1) * np.sqrt(0.105e3) * t64 * t65 ** 2 * (11 * t64 ** 2 - 3) * np.sin((3 * phi1)) * ((1 + t64) ** (-0.1e1 / 0.2e1)) * ((1 - t64) ** (-0.1e1 / 0.2e1))

        if Bindx == 16:
            t74 = np.cos(phi)
            t73 = t74 ** 2
            t81 = 2 * t73
            t77 = t73 ** 2
            t80 = 1 + t81 - 3 * t77
            t79 = (t77 + t81 - 3) * t74
            t75 = 3 * phi1
            tfunc[..., c] = -0.13e2 / 0.32e2 * np.sqrt(0.55e2) * np.sqrt((1 - t74)) * np.sqrt((1 + t74)) * (-(t79 + t80) * np.sin((-t75 + 6 * phi2)) + (t79 - t80) * np.sin((t75 + 6 * phi2)))

        if Bindx == 17:
            t82 = np.cos(phi)
            t83 = t82 ** 2
            t84 = t83 ** 2
            tfunc[..., c] = 0.39e2 / 0.16e2 * np.sqrt(0.7e1) * (-23 * t84 - 1 + (11 * t84 + 13) * t83) * np.cos((4 * phi1))

        if Bindx == 18:
            t92 = np.cos(phi)
            t91 = t92 ** 2
            t94 = t91 ** 2
            t95 = t92 * t94
            t98 = 4 * t92 - 4 * t95
            t97 = t92 * t95 - 5 * t91 + 5 * t94 - 1
            t93 = 4 * phi1
            tfunc[..., c] = -0.13e2 / 0.64e2 * np.sqrt(0.66e2) * ((t97 + t98) * np.cos((-t93 + 6 * phi2)) + (t97 - t98) * np.cos((t93 + 6 * phi2)))

        if Bindx == 19:
            t103 = np.sin(phi)
            t100 = t103 ** 2
            t101 = t103 * t100
            t99 = np.cos(phi)
            tfunc[..., c] = -0.39e2 / 0.16e2 * np.sqrt(0.2e1) * np.sqrt(0.77e2) * t99 * t101 ** 2 * np.sin((5 * phi1)) * ((1 + t99) ** (-0.1e1 / 0.2e1)) * ((1 - t99) ** (-0.1e1 / 0.2e1))

        if Bindx == 20:
            t110 = np.cos(phi)
            t109 = t110 ** 2
            t113 = t109 ** 2
            t116 = -1 - 10 * t109 - 5 * t113
            t115 = (10 * t109 + t113 + 5) * t110
            t111 = 5 * phi1
            tfunc[..., c] = 0.13e2 / 0.32e2 * np.sqrt(0.3e1) * np.sqrt((1 - t110)) * np.sqrt((1 + t110)) * (-(t115 + t116) * np.sin((-t111 + 6 * phi2)) + (t115 - t116) * np.sin((t111 + 6 * phi2)))

        if Bindx == 21:
            t117 = np.cos(phi)
            t118 = t117 ** 2
            t119 = t118 ** 2
            tfunc[..., c] = -0.13e2 / 0.32e2 * np.sqrt(0.2e1) * np.sqrt(0.231e3) * np.cos((6 * phi1)) * (-3 * t119 - 1 + (t119 + 3) * t118)

        if Bindx == 22:
            t128 = np.cos(phi)
            t135 = -0.39e2 / 0.32e2 * t128
            t127 = t128 ** 2
            t129 = t128 * t127
            t130 = t127 ** 2
            t134 = -0.65e2 / 0.16e2 * t129 + t130 * t135 + t135
            t133 = 0.13e2 / 0.64e2 * t129 ** 2 + 0.13e2 / 0.64e2 + 0.195e3 / 0.64e2 * t130 + 0.195e3 / 0.64e2 * t127
            tfunc[..., c] = (t133 + t134) * np.cos((6 * phi1 - 6 * phi2)) + (t133 - t134) * np.cos((6 * phi1 + 6 * phi2))

        if Bindx == 23:
            t136 = np.cos(phi)
            t137 = t136 ** 2
            t138 = t137 ** 2
            tfunc[..., c] = -0.15e2 / 0.32e2 * np.sqrt(0.2e1) * np.sqrt(0.3003e4) * t136 * np.cos((6 * phi2)) * (-3 * t138 - 1 + (t138 + 3) * t137)

        if Bindx == 24:
            t149 = np.cos(phi)
            t148 = t149 ** 2
            t150 = t149 * t148
            t151 = t148 ** 2
            t153 = t150 ** 2
            t157 = -18 * t150 + 6 * (3 * t151 - t153 + 1) * t149
            t156 = 10 * t148 + 22 * t153 - 1 + (-24 - 7 * t151) * t151
            tfunc[..., c] = 0.15e2 / 0.128e3 * np.sqrt(0.858e3) * ((-t156 + t157) * np.sin((phi1 - 6 * phi2)) + (t156 + t157) * np.sin((phi1 + 6 * phi2))) * ((1 + t149) ** (-0.1e1 / 0.2e1)) * ((1 - t149) ** (-0.1e1 / 0.2e1))

        if Bindx == 25:
            t166 = np.cos(phi)
            t165 = t166 ** 2
            t169 = t165 ** 2
            t168 = t166 * t165
            t171 = t168 ** 2
            t174 = 2 - 16 * t165 + 26 * t169 - 12 * t171
            t173 = -t168 + (11 * t169 - 7 * t171 - 3) * t166
            t167 = 2 * phi1
            tfunc[..., c] = -0.15e2 / 0.64e2 * np.sqrt(0.143e3) * ((-t173 + t174) * np.cos((-t167 + 6 * phi2)) + (t173 + t174) * np.cos((t167 + 6 * phi2)))

        if Bindx == 26:
            t184 = np.cos(phi)
            t183 = t184 ** 2
            t186 = t184 * t183
            t187 = t183 ** 2
            t189 = t186 ** 2
            t193 = -22 * t186 + (38 * t187 - 18 * t189 + 2) * t184
            t192 = -18 * t183 + 2 * t189 + 3 + (20 - 7 * t187) * t187
            t185 = 3 * phi1
            tfunc[..., c] = -0.15e2 / 0.128e3 * np.sqrt(0.286e3) * (-(-t192 + t193) * np.sin((-t185 + 6 * phi2)) + (t192 + t193) * np.sin((t185 + 6 * phi2))) * ((1 + t184) ** (-0.1e1 / 0.2e1)) * ((1 - t184) ** (-0.1e1 / 0.2e1))

        if Bindx == 27:
            t202 = np.cos(phi)
            t201 = t202 ** 2
            t205 = t201 ** 2
            t204 = t202 * t201
            t207 = t204 ** 2
            t210 = 4 - 8 * t201 - 20 * t205 + 24 * t207
            t209 = 35 * t204 + (-19 * t205 - 7 * t207 - 9) * t202
            t203 = 4 * phi1
            tfunc[..., c] = -0.15e2 / 0.64e2 * np.sqrt(0.26e2) * ((t209 + t210) * np.cos((-t203 + 6 * phi2)) + (-t209 + t210) * np.cos((t203 + 6 * phi2)))

        if Bindx == 28:
            t220 = np.cos(phi)
            t219 = t220 ** 2
            t222 = t220 * t219
            t223 = t219 ** 2
            t225 = t222 ** 2
            t229 = 38 * t222 + (10 * t223 - 30 * t225 - 18) * t220
            t228 = -10 * t219 - 38 * t225 - 5 + (60 - 7 * t223) * t223
            t221 = 5 * phi1
            tfunc[..., c] = 0.15e2 / 0.128e3 * np.sqrt(0.26e2) * (-(-t228 + t229) * np.sin((-t221 + 6 * phi2)) + (t228 + t229) * np.sin((t221 + 6 * phi2))) * ((1 + t220) ** (-0.1e1 / 0.2e1)) * ((1 - t220) ** (-0.1e1 / 0.2e1))

        if Bindx == 29:
            t238 = np.cos(phi)
            t237 = t238 ** 2
            t240 = t237 ** 2
            t239 = t238 * t237
            t242 = t239 ** 2
            t245 = 0.375e3 / 0.32e2 * t240 + 0.135e3 / 0.16e2 * t242 - 0.45e2 / 0.4e1 * t237 - 0.45e2 / 0.32e2
            t244 = 0.225e3 / 0.64e2 * t239 + (-0.1035e4 / 0.64e2 * t240 - 0.105e3 / 0.64e2 * t242 + 0.435e3 / 0.64e2) * t238
            tfunc[..., c] = (t244 + t245) * np.cos((6 * phi1 - 6 * phi2)) + (-t244 + t245) * np.cos((6 * phi1 + 6 * phi2))

        if Bindx == 30:
            t254 = np.cos(phi)
            t253 = t254 ** 2
            t263 = 14 * t253
            t256 = t254 * t253
            t258 = t256 ** 2
            t259 = t254 * t258
            t262 = -t254 * t259 - 14 * t258 + t263 + 1
            t261 = -6 * t254 + 6 * t259 + (t263 - 14) * t256
            t255 = 7 * phi1
            tfunc[..., c] = 0.15e2 / 0.128e3 * np.sqrt(0.14e2) * (-(t261 + t262) * np.sin((-t255 + 6 * phi2)) + (t261 - t262) * np.sin((t255 + 6 * phi2))) * ((1 + t254) ** (-0.1e1 / 0.2e1)) * ((1 - t254) ** (-0.1e1 / 0.2e1))

        if Bindx == 31:
            t264 = np.cos(phi)
            t265 = t264 ** 2
            t266 = t265 ** 2
            tfunc[..., c] = -0.5355e4 / 0.32e2 * t265 + 0.595e3 / 0.128e3 + (-0.51051e5 / 0.32e2 * t265 + 0.58905e5 / 0.64e2 + 0.109395e6 / 0.128e3 * t266) * t266

        if Bindx == 32:
            t269 = np.cos(phi)
            t270 = t269 ** 2
            t271 = t270 ** 2
            tfunc[..., c] = -0.17e2 / 0.64e2 * np.sqrt(0.2e1) * np.sqrt(0.429e3) * (-18 * t270 + 1 + (-46 * t270 + 48 + 15 * t271) * t271) * np.cos((6 * phi2))

        if Bindx == 33:
            t275 = np.cos(phi)
            t276 = t275 ** 2
            t277 = t276 ** 2
            t274 = np.sin(phi)
            tfunc[..., c] = -0.51e2 / 0.32e2 * t275 * t274 ** 2 * (-1001 * t277 - 35 + (715 * t277 + 385) * t276) * np.sin(phi1) * ((1 + t275) ** (-0.1e1 / 0.2e1)) * ((1 - t275) ** (-0.1e1 / 0.2e1))

        if Bindx == 34:
            t289 = np.cos(phi)
            t288 = t289 ** 2
            t291 = t288 ** 2
            t290 = t289 * t288
            t293 = t290 ** 2
            t295 = t291 ** 2
            t298 = -1 + 18 * t288 - 48 * t291 + 46 * t293 - 15 * t295
            t297 = -38 * t290 + (78 * t291 - 66 * t293 + 20 * t295 + 6) * t289
            tfunc[..., c] = -0.17e2 / 0.128e3 * np.sqrt(0.858e3) * ((t297 + t298) * np.sin((phi1 - 6 * phi2)) + (t297 - t298) * np.sin((phi1 + 6 * phi2))) * ((1 + t289) ** (-0.1e1 / 0.2e1)) * ((1 - t289) ** (-0.1e1 / 0.2e1))

        if Bindx == 35:
            t299 = np.cos(phi)
            t300 = t299 ** 2
            t301 = t300 ** 2
            tfunc[..., c] = -0.51e2 / 0.64e2 * np.sqrt(0.2e1) * np.sqrt(0.35e2) * (-34 * t300 + 1 + (-286 * t300 + 176 + 143 * t301) * t301) * np.cos((2 * phi1))

        if Bindx == 36:
            t312 = np.cos(phi)
            t311 = t312 ** 2
            t314 = t312 * t311
            t315 = t311 ** 2
            t317 = t314 ** 2
            t320 = 2 * t314 + 2 * (-2 * t315 + t317) * t312
            t319 = 1 - 5 * t311 + 7 * t315 - 3 * t317
            t313 = 2 * phi1
            tfunc[..., c] = 0.17e2 / 0.64e2 * np.sqrt(0.15015e5) * t312 * ((t319 + t320) * np.cos((-t313 + 6 * phi2)) + (-t319 + t320) * np.cos((t313 + 6 * phi2)))

        if Bindx == 37:
            t326 = np.sin(phi)
            t324 = t326 ** 2
            t321 = np.cos(phi)
            t322 = t321 ** 2
            tfunc[..., c] = -0.17e2 / 0.32e2 * np.sqrt(0.1155e4) * t321 * t324 ** 2 * (3 + (-26 + 39 * t322) * t322) * np.sin((3 * phi1)) * ((1 + t321) ** (-0.1e1 / 0.2e1)) * ((1 - t321) ** (-0.1e1 / 0.2e1))

        if Bindx == 38:
            t337 = np.cos(phi)
            t336 = t337 ** 2
            t340 = t336 ** 2
            t339 = t337 * t336
            t342 = t339 ** 2
            t344 = t340 ** 2
            t347 = -1 + 14 * t336 - 52 * t340 + 66 * t342 - 27 * t344
            t346 = 22 * t339 - 14 * (t340 + t342) * t337 + (12 * t344 - 6) * t337
            t338 = 3 * phi1
            tfunc[..., c] = 0.17e2 / 0.128e3 * np.sqrt(0.910e3) * (-(t346 + t347) * np.sin((-t338 + 6 * phi2)) + (t346 - t347) * np.sin((t338 + 6 * phi2))) * ((1 + t337) ** (-0.1e1 / 0.2e1)) * ((1 - t337) ** (-0.1e1 / 0.2e1))

        if Bindx == 39:
            t349 = np.cos(phi)
            t350 = t349 ** 2
            t351 = t350 ** 2
            tfunc[..., c] = 0.51e2 / 0.64e2 * np.sqrt(0.77e2) * (-28 * t350 + 1 + (-156 * t350 + 118 + 65 * t351) * t351) * np.cos((4 * phi1))

        if Bindx == 40:
            t363 = np.cos(phi)
            t362 = t363 ** 2
            t365 = t363 * t362
            t366 = t362 ** 2
            t368 = t365 ** 2
            t372 = -5 * t365 + (21 * t366 - 15 * t368 - 1) * t363
            t371 = 10 * t362 + 6 * t368 - 1 + (-20 + 5 * t366) * t366
            t364 = 4 * phi1
            tfunc[..., c] = -0.17e2 / 0.64e2 * np.sqrt(0.546e3) * ((t371 + t372) * np.cos((-t364 + 6 * phi2)) + (t371 - t372) * np.cos((t364 + 6 * phi2)))

        if Bindx == 41:
            t377 = np.sin(phi)
            t374 = t377 ** 2
            t375 = t377 * t374
            t373 = np.cos(phi)
            tfunc[..., c] = -0.51e2 / 0.32e2 * np.sqrt(0.1001e4) * t373 * t375 ** 2 * (5 * t373 ** 2 - 1) * np.sin((5 * phi1)) * ((1 + t373) ** (-0.1e1 / 0.2e1)) * ((1 - t373) ** (-0.1e1 / 0.2e1))

        if Bindx == 42:
            t388 = np.cos(phi)
            t387 = t388 ** 2
            t391 = t387 ** 2
            t390 = t388 * t387
            t393 = t390 ** 2
            t395 = t391 ** 2
            t398 = 7 - 42 * t387 + 20 * t391 + 90 * t393 - 75 * t395
            t397 = 90 * t390 + (-162 * t391 + 62 * t393 + 20 * t395 - 10) * t388
            t389 = 5 * phi1
            tfunc[..., c] = -0.17e2 / 0.128e3 * np.sqrt(0.42e2) * (-(t397 + t398) * np.sin((-t389 + 6 * phi2)) + (t397 - t398) * np.sin((t389 + 6 * phi2))) * ((1 + t388) ** (-0.1e1 / 0.2e1)) * ((1 - t388) ** (-0.1e1 / 0.2e1))

        if Bindx == 43:
            t399 = np.cos(phi)
            t400 = t399 ** 2
            t401 = t400 ** 2
            tfunc[..., c] = -0.17e2 / 0.64e2 * np.sqrt(0.2e1) * np.sqrt(0.429e3) * (-18 * t400 + 1 + (-46 * t400 + 48 + 15 * t401) * t401) * np.cos((6 * phi1))

        if Bindx == 44:
            t412 = np.cos(phi)
            t413 = t412 ** 2
            t415 = t413 ** 2
            t414 = t412 * t413
            t417 = t414 ** 2
            t421 = 0.833e3 / 0.16e2 * t417 + 0.17e2 / 0.4e1 + (-0.1785e4 / 0.32e2 + 0.255e3 / 0.32e2 * t415) * t415
            t420 = 0.2975e4 / 0.64e2 * t414 + (-0.2295e4 / 0.64e2 * t417 - 0.357e3 / 0.64e2 * t415 - 0.867e3 / 0.64e2) * t412
            tfunc[..., c] = (t420 + t421) * np.cos((6 * phi1 - 6 * phi2)) + (-t420 + t421) * np.cos((6 * phi1 + 6 * phi2))

        if Bindx == 45:
            t426 = np.sin(phi)
            t423 = t426 ** 2
            t424 = t423 ** 2
            t422 = np.cos(phi)
            tfunc[..., c] = -0.51e2 / 0.32e2 * np.sqrt(0.715e3) * t422 * t424 ** 2 * np.sin((7 * phi1)) * ((1 - t422) ** (-0.1e1 / 0.2e1)) * ((1 + t422) ** (-0.1e1 / 0.2e1))

        if Bindx == 46:
            t437 = np.cos(phi)
            t436 = t437 ** 2
            t440 = t436 ** 2
            t439 = t437 * t436
            t442 = t439 ** 2
            t444 = t440 ** 2
            t447 = -3 - 18 * t436 + 56 * t440 - 14 * t442 - 21 * t444
            t446 = -14 * t439 + (-42 * t440 + 38 * t442 + 4 * t444 + 14) * t437
            t438 = 7 * phi1
            tfunc[..., c] = 0.17e2 / 0.128e3 * np.sqrt(0.30e2) * (-(t446 + t447) * np.sin((-t438 + 6 * phi2)) + (t446 - t447) * np.sin((t438 + 6 * phi2))) * ((1 - t437) ** (-0.1e1 / 0.2e1)) * ((1 + t437) ** (-0.1e1 / 0.2e1))

        if Bindx == 47:
            t448 = np.cos(phi)
            t449 = t448 ** 2
            t453 = -4 * t449
            t450 = t449 ** 2
            tfunc[..., c] = 0.51e2 / 0.128e3 * np.sqrt(0.715e3) * np.cos((8 * phi1)) * (t453 + 1 + (t453 + 6 + t450) * t450)

        if Bindx == 48:
            t462 = np.cos(phi)
            t461 = t462 ** 2
            t471 = -14 * t461
            t464 = t462 * t461
            t466 = t464 ** 2
            t467 = t462 * t466
            t470 = t462 * t467 + 14 * t466 + t471 - 1
            t469 = 6 * t462 - 6 * t467 + (t471 + 14) * t464
            t463 = 8 * phi1
            tfunc[..., c] = -0.17e2 / 0.128e3 * np.sqrt(0.30e2) * ((t469 + t470) * np.cos((-t463 + 6 * phi2)) + (-t469 + t470) * np.cos((t463 + 6 * phi2)))

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

