import read_micr as rm
import get_strain as gs
import get_mf as gm
import get_neighbors as gn
import get_features as gf
import get_regression as gr
import get_validation as gv
# import alljobs_functions as af
from constants import const
import h5py

C = const()

ns_cal = C['ns_cal']
strt_cal = C['strt_cal']
set_id_cal = C['set_id_cal']
dir_cal = C['dir_cal']

ns_val = C['ns_val']
strt_val = C['strt_val']
set_id_val = C['set_id_val']
dir_val = C['dir_val']

f = h5py.File("spatial.hdf5", 'w')
f.close()

"""Gather data from vtk files"""
rm.read(ns_cal, strt_cal, set_id_cal, dir_cal)
rm.read(ns_val, strt_val, set_id_val, dir_val)

"""get the data for the linkage"""
f = h5py.File("responses.hdf5", 'w')
f.close()

gs.fegrab(ns_cal, strt_cal, set_id_cal, dir_cal)
gs.fegrab(ns_val, strt_val, set_id_val, dir_val)

"""Compute GSH coefficients to create microstructure function in real and
fourier space"""

gm.get_mf(ns_cal, set_id_cal)
gm.get_mf(ns_val, set_id_val)

"""find the gsh coefficient sets associated with the nearest neighbors in
the calibration and validation microstructures"""

gn.neighbors(ns_cal, set_id_cal)
gn.neighbors(ns_val, set_id_val)

"""run scripts prepare for regression"""
gf.features(ns_cal, set_id_cal)
gf.features(ns_val, set_id_val)

"""perform the regression to calibrate the real-space, limited range
MKS function"""
gr.regress(ns_cal, set_id_cal)

"""perform the validation of the regression"""
gv.validate(ns_cal, set_id_cal)
gv.validate(ns_val, set_id_val)
