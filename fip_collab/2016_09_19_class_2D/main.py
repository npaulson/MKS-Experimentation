import sve_gen as gen
import get_M as gm
import correlate as corr
import plot_correlation as pltcorr
import pca_on_correlations as pcaC
import plot_pc_map as pltPC
import time
import h5py


ns_cal = [20, 20, 20, 20, 20, 20]
set_id_cal = ['inclusion', 'bicrystal', 'gaussian', 'delta', 'bicrystal2', 'inclusion2']

# ns_cal = [30, 30, 30]
# set_id_cal = ['incl1', 'incl2', 'incl3']

el = 21
H = 2

wrt_file = 'log_%s.txt' % (time.strftime("%Y-%m-%d_h%Hm%M"))


"""Generate microstructures"""

f = h5py.File("spatial_stats.hdf5", 'w')
f.close()

vfrac = [.1]
gen.inclusion_red(el, ns_cal[0], H, set_id_cal[0], wrt_file, vfrac)

gen.bicrystal_orthog(el, ns_cal[1], H, set_id_cal[1], wrt_file)
gen.improcess(el, ns_cal[2], H, set_id_cal[2], wrt_file)

gen.delta(el, ns_cal[3], H, set_id_cal[3], wrt_file)
gen.bicrystal(el, ns_cal[4], H, set_id_cal[4], wrt_file)
gen.inclusion(el, ns_cal[5], H, set_id_cal[5], wrt_file, vfrac)


# vfrac = [.075, .125]
# gen.inclusion_red(el, ns_cal[0], H, set_id_cal[0], wrt_file, vfrac)
# vfrac = [.100, .100]
# gen.inclusion_red(el, ns_cal[1], H, set_id_cal[1], wrt_file, vfrac)
# vfrac = [.125, .075]
# gen.inclusion_red(el, ns_cal[2], H, set_id_cal[2], wrt_file, vfrac)

# gen.bicrystal_orthog(el, ns_cal[1], H, set_id_cal[1], wrt_file)
# gen.improcess(el, ns_cal[2], H, set_id_cal[2], wrt_file)

"""Generate the fourier space microstructure functions"""

for ii in xrange(len(set_id_cal)):
    gm.get_M(el, ns_cal[ii], H, set_id_cal[ii], wrt_file)

"""Compute the periodic statistics for the microstructures"""
for ii in xrange(len(set_id_cal)):
    corr.correlate(el, ns_cal[ii], H, set_id_cal[ii], wrt_file)

"""Perform PCA on autocorrelations"""
pcaC.doPCA(el, ns_cal, H, set_id_cal, wrt_file)

"""Plot an autocorrelation"""
set_num = 2
sn = 0
iA = 0
iB = 0
pltcorr.pltcorr(el, ns_cal[set_num], set_id_cal[set_num], sn, iA, iB)

"""Plot the microstructures in PC space"""
pcA = 0
pcB = 1
pltPC.pltmap(ns_cal, set_id_cal, pcA, pcB)
