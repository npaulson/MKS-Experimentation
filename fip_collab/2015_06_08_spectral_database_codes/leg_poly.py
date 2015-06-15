# -*- coding: utf-8 -*-
"""
"""

import numpy as np
import vtk


def leg_poly(n, X):

    if n == 0:
        PnX = np.oneslike(X)
    elif n == 1:
        PnX = X
    elif n == 2:
        PnX = 0.5*(3*X**2-1)
    elif n == 3:
        PnX = 0.5*X*(5*X**2-3)
    elif n == 4:
        PnX = (1/8)*(35*X**4-30*X**2+3)
    elif n == 5:
        PnX = (1/8)*X*(63*X**4-70*X**2+15)
    elif n == 6:
        PnX = (1/16)*(231*X**6-315*X**4+105*X**2-5)
    elif n == 7:
        PnX = (1/16)*X*(429*X**6-693*X**4+315*X**2-35)
    elif n == 8:
        PnX = (1/128)*(6435*X**8-12012*X**6+6930*X**4-1260*X**2+35)

return PnX