# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 11:45:46 2014

@author: nhpnp3
"""

import matlab.engine


def matlab_test():
    # start the matlab engine
    eng = matlab.engine.start_matlab()

    # call the desired GSH function in matlab
    tmp = eng.gsh_hex_tri_L2_8(.1, .2, .3)

    print(tmp)

if __name__ == "__main__":
    matlab_test()
