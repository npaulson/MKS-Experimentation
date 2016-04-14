import plot_correlation as pltcorr
import sve_plot_pc as pltPC
import plot_effective_modulus as pem
import explained_variance as ev
import numpy as np
import time


ns_cal = [10, 10, 10, 10]
set_id_cal = ['randomD3D_cal', 'transverseD3D_cal',
              'basaltransD3D_cal', 'actualD3D_cal']
dir_cal = ['randomD3D_cal', 'transverseD3D_cal',
           'basaltransD3D_cal', 'actualD3D_cal']

ns_val = [10, 10, 10, 10]
set_id_val = ['randomD3D_val', 'transverseD3D_val',
              'basaltransD3D_val', 'actualD3D_val']
dir_val = ['randomD3D_val', 'transverseD3D_val',
           'basaltransD3D_val', 'actualD3D_val']

L = 4
H = 15
el = 21
step = 1

wrt_file = 'log_%s.txt' % (time.strftime("%Y-%m-%d_h%Hm%M"))

"""Plot an autocorrelation"""
sn = 0
iA = 1
iB = 1
pltcorr.pltcorr(el, ns_cal[0], set_id_cal[0], step, sn, iA, iB)

# """Plot the percentage explained variance"""
# ns_tot = np.sum(ns_cal)
# ev.variance(el, ns_tot, step)

"""Plot the microstructures in PC space"""
pcA = 0
pcB = 1
pltPC.pltPC(el, ns_cal, set_id_cal, step, pcA, pcB)

"""Plot the effective modulus versus a PC dimension"""
pcA = 0
pem.plt_modulus(el, ns_cal, set_id_cal, step, pcA)
