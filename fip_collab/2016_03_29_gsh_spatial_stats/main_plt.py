import plot_correlation as pltcorr
import sve_plot_pc as pltPC
import plot_effective_modulus as pem
# import explained_variance as ev
import numpy as np
import time


# ns_cal = [10]
# set_id_cal = ['bicrystal']

# ns_cal = [10, 10, 10, 10]
# set_id_cal = ['randomD3D', 'delta', 'inclusion', 'bicrystal']

# ns_D3D = [10]
# set_id_D3D = ['randomD3D']
# dir_D3D = ['randomD3D']

ns_cal = [10, 10, 10, 10]
set_id_cal = ['randomD3D', 'transverseD3D', 'basaltransD3D', 'actualD3D']
dir_cal = ['randomD3D', 'transverseD3D', 'basaltransD3D', 'actualD3D']

ns_D3D = [10, 10, 10, 10]
set_id_D3D = ['randomD3D', 'transverseD3D', 'basaltransD3D', 'actualD3D']
dir_D3D = ['randomD3D', 'transverseD3D', 'basaltransD3D', 'actualD3D']

L = 4
H = 15
el = 21
step = 6

wrt_file = 'log_%s.txt' % (time.strftime("%Y-%m-%d_h%Hm%M"))

# """Plot an autocorrelation"""
# sn = 0
# iA = 1
# iB = 1
# pltcorr.pltcorr(el, ns_cal[0], set_id_cal[0], step, sn, iA, iB)

# """Plot the percentage explained variance"""
# ns_tot = np.sum(ns_cal)
# ev.variance(el, ns_tot, step)

"""Plot the microstructures in PC space"""
pcA = 3
pcB = 3
pltPC.pltPC(el, ns_cal, set_id_cal, step, pcA, pcB)

"""Plot the effective modulus versus a PC dimension"""
pcA = 0
pem.plt_modulus(el, ns_cal, set_id_cal, step, pcA)
