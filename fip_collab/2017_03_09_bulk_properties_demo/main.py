import select_euler_response as ser
import get_M
import correlate as corr
import plot_correlation as pltcorr
import get_new_space as gns
import transform as tf
import plot_explained_variance_all as pev
import plot_pc_map_label as pltmap
import plot_pc_map_3d as pltmap3d
import plot_dendrogram as pd
import get_linkage as gl
import get_linkage_GPR as glGPR
import get_response as gr
import plot_err_v_pc as pevp
import plot_linkage_check_gray as plc
import plot_linkage_check_sigma as plc_sig
import h5py
import numpy as np
import matplotlib.pyplot as plt
import urllib
import ssl

C = {}

C['el'] = 21  # SVEs have el^3 cells
C['vmax'] = 21  # each 2-pt correlation has vmax^3 cells
C['H'] = 15  # max number of gsh functions


C['set_id'] = ['Ac', 'BaTr', 'Di', 'Id', 'Od',
               'Ra', 'Tr', 'Dd', 'BaTrTr', 'DdTr', 'DiTr', 'OdTr']
C['names'] = ['A', 'B', 'C', 'D',
              'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']


C['names_cal'] = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
C['set_id_cal'] = [s + '_cal' for s in C['names_cal']]
C['strt_cal'] = list(np.zeros(len(C['names_cal']), dtype='int16'))
C['ns_cal'] = list(20*np.ones(len(C['names_cal']), dtype='int16'))
C['dir_cal'] = C['names_cal']

C['names_val'] =  ['H', 'I', 'J', 'K', 'L']
C['set_id_val'] = [s + '_val' for s in C['names_val']]
C['strt_val'] = list(np.zeros(len(C['names_val']), dtype='int16'))
C['ns_val'] = list(20*np.ones(len(C['names_val']), dtype='int16'))
C['dir_val'] = C['names_val']
C['dir_resp'] = "response"

C['bc'] = 'bc3'

"""select which correlations to include in the spatial statistics set"""
cmat = []
for ii in xrange(C['H']):
    cmat.append([0, ii])
for ii in xrange(1, C['H']):
    cmat.append([1, ii])
cmat = np.array(cmat)

C['cmat'] = cmat
C['cmax'] = cmat.shape[0]

C['n_pc_tot'] = np.sum(C['ns_cal'])
# C['n_pc_max'] = 10
# C['n_poly_max'] = 3

"""make a set of #s of PC and deg"""
pcdeg = []
for ii in xrange(1, 50):
    pcdeg.append([ii, 1])
for ii in xrange(1, 19):
    pcdeg.append([ii, 2])
for ii in xrange(1, 13):
    pcdeg.append([ii, 3])
C['pcdeg'] = np.array(pcdeg)


# """download data files"""
# context = ssl._create_unverified_context()

# eulerfile = urllib.URLopener(context=context)
# eulerfile.retrieve("https://matin.gatech.edu/resources/61/download/euler_all.hdf5", "euler_all.hdf5")
# print "microstructure data retrieved"

# responsesfile = urllib.URLopener(context=context)
# responsesfile.retrieve("https://matin.gatech.edu/resources/62/download/responses_all.hdf5", "responses_all.hdf5")
# print "response data retrieved"

# """select the desired euler angle and response sets"""
# f = h5py.File("euler.hdf5", 'w')
# f.close()
# f = h5py.File("responses.hdf5", 'w')
# f.close()
# for ii in xrange(len(C['set_id_cal'])):
#     ser.select(C, C['ns_cal'][ii], C['strt_cal'][ii],
#                C['names_cal'][ii], C['set_id_cal'][ii], C['bc'])
# print "calibration data selected"
# for ii in xrange(len(C['set_id_val'])):
#     ser.select(C, C['ns_val'][ii], C['strt_val'][ii],
#                C['names_val'][ii], C['set_id_val'][ii], C['bc'])
# print "validation data selected"

# f = h5py.File("spatial_L%s.hdf5" % C['H'], 'w')
# f.close()

# """Compute GSH coefficients to create microstructure function in real and
# fourier space"""
# for ii in xrange(len(C['set_id_cal'])):
#     get_M.get_M(C, C['ns_cal'][ii], C['set_id_cal'][ii])
# print "microstructure function generated for calibration data"

# for ii in xrange(len(C['set_id_val'])):
#     get_M.get_M(C, C['ns_val'][ii], C['set_id_val'][ii])
# print "microstructure function generated for validation data"

# """Compute the periodic statistics for the microstructures"""
# for ii in xrange(len(C['set_id_cal'])):
#     corr.correlate(C, C['ns_cal'][ii], C['set_id_cal'][ii])
# print "correlations computed for calibration data"

# for ii in xrange(len(C['set_id_val'])):
#     corr.correlate(C, C['ns_val'][ii], C['set_id_val'][ii])
# print "correlations computed for validation data"

# set_id = C['set_id_val'][3]  # index for the microstructure of interest
# sn = 0  # index for the SVE of interest
# iA = 10  # index for the correlation of interest
# pltcorr.pltcorr(C, set_id=set_id, sn=sn, iA=iA)

# """Perform PCA on correlations"""
# pca = gns.new_space(C, C['ns_cal'], C['set_id_cal'])
# print "Principal Component Analysis (PCA) performed"

# """transform statistics to reduced dimensionality space"""
# f = h5py.File("spatial_reduced_L%s.hdf5" % C['H'], 'w')
# f.close()

# for ii in xrange(len(C['set_id_cal'])):
#     tf.transform(C, C['ns_cal'][ii], C['set_id_cal'][ii], pca)
# print "calibration SVEs transformed to PC representation"

# for ii in xrange(len(C['set_id_val'])):
#     tf.transform(C, C['ns_val'][ii], C['set_id_val'][ii], pca)
# print "validation SVEs transformed to PC representation"

# """Plot the percentage explained variance"""
# pev.variance(C, [0, 7, 86, 102], [C['H']])

# """Plot the microstructures in PC space"""
# pcA = 0
# pcB = 1
# pltmap.pltmap(C, C['H'], pcA, pcB)

# """create the specified array of linkages and cross validate"""

# f = h5py.File("regression_results_L%s.hdf5" % C['H'], 'w')
# f.close()

# mtype = 'Ridge'

# # gl.linkage(C, 'modulus', mtype)
# gl.linkage(C, 'modulus')
# print "linkage for elastic stiffness performed"

# # gl.linkage(C, 'strength', mtype)
# gl.linkage(C, 'strength')
# print "linkage for yield strength performed"

"""plot cross validation error for elastic stiffness """

deg = 1

upbnd = 10
pevp.plterr(C, 'modulus', upbnd, deg, ['cv'], [C['H']])
pevp.plterr(C, 'modulus', upbnd, deg, ['val'], [C['H']])

"""plot cross validation error for yield strength """
err_bnd = 20
pevp.plterr(C, 'strength', upbnd, deg, ['cv'], [C['H']])
pevp.plterr(C, 'strength', upbnd, deg, ['val'], [C['H']])

plc.plot_check(C, 'modulus', n_pc=4, deg=1, H=C['H'], erv=1)
plc.plot_check(C, 'strength', n_pc=5, deg=1, H=C['H'], erv=5)

plt.show()
