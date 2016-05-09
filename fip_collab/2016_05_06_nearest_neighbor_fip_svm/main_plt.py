import plot_correlation as pltcorr
import plot_pc_map as ppm
import plot_response as pr
import plot_linkage_check as plc
import explained_variance as ev
import numpy as np
import time


ns_cal = [20, 20, 20, 20]
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
vmax = 5
step = 1

wrt_file = 'log_%s.txt' % (time.strftime("%Y-%m-%d_h%Hm%M"))

"""Plot an autocorrelation"""
sn = 0
iA = 1
iB = 1
pltcorr.pltcorr(el, vmax, ns_cal[0], set_id_cal[0], step, sn, iA, iB)

"""Plot the percentage explained variance"""
ev.variance()

"""Plot the microstructures in PC space"""
pcA = 0
pcB = 1
ppm.pltmap(ns_cal, set_id_cal, pcA, pcB)

"""Plot the effective stiffness versus a PC dimension"""
pcA = 0
pr.pltresponse(ns_cal, set_id_cal, 'fip', pcA)

"""Plot the predicted versus actual values of the property of interest"""
plc.pltcheck(ns_val, set_id_val, 'fip')
