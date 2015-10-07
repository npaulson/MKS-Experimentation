import numpy as np
import time


def check(s_list, f_list):

    Lset = np.array([120., 360., 360., 360.])*(np.pi/180.)

    st = time.time()

    xi = np.array([5., 5., 5., 5.])*3*(np.pi/180)

    Pvec = f_list[:, -1] * \
        np.exp((2*np.pi*1j*s_list[:, 0]*xi[0])/Lset[0]) * \
        np.exp((2*np.pi*1j*s_list[:, 1]*xi[1])/Lset[1]) * \
        np.exp((2*np.pi*1j*s_list[:, 2]*xi[2])/Lset[2]) * \
        np.exp((2*np.pi*1j*s_list[:, 3]*xi[3])/Lset[3])

    Numel = 40*120*120*120

    db_res = np.real(np.sum(Pvec, 0)/Numel)

    interp_time = time.time()-st

    return db_res, interp_time
