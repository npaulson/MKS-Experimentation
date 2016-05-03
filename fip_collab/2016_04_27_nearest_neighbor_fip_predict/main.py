import vtk_read as vr
import get_mf as gm
import get_neighbors as gn
import get_regression_order1 as gr
import get_validation_order1 as gv
import time
import h5py


ns_cal = [2]
set_id_cal = ['cal']
dir_cal = ['cal']

ns_val = [2]
set_id_val = ['val']
dir_val = ['val']

H = 9
el = 21
step = 1
ext = 3

wrt_file = 'log_%s.txt' % (time.strftime("%Y-%m-%d_h%Hm%M"))

f = h5py.File("spatial.hdf5", 'w')
f.close()

"""
The tensorID determines the type of tensor data read from the .vtk file
if tensorID == 0, we read the stress tensor
if tensorID == 1, we read the strain tensor
if tensorID == 2, we read the plastic strain tensor
"""

"""Gather data from vtk files"""
for ii in xrange(len(set_id_cal)):
    vr.read_euler(el, ns_cal[ii], set_id_cal[ii],
                  step, dir_cal[ii], wrt_file, 1)
    vr.read_euler(el, ns_val[ii], set_id_val[ii],
                  step, dir_val[ii], wrt_file, 1)

"""get the data for the linkage"""

f = h5py.File("responses.hdf5", 'w')
f.close()

for ii in xrange(len(set_id_cal)):
    vr.read_fip(el, ns_cal[ii], set_id_cal[ii], step, dir_cal[ii], wrt_file)
    vr.read_fip(el, ns_cal[ii], set_id_val[ii], step, dir_val[ii], wrt_file)

"""Compute GSH coefficients to create microstructure function in real and
fourier space"""

for ii in xrange(len(set_id_cal)):
    gm.get_mf(el, H, ns_cal[ii], set_id_cal[ii], step, wrt_file)
    gm.get_mf(el, H, ns_val[ii], set_id_val[ii], step, wrt_file)

"""find the gsh coefficient sets associated with the nearest neighbors in
the calibration and validation microstructures"""

for ii in xrange(len(set_id_cal)):
    gn.neighbors(el, ns_cal[ii], H, ext, set_id_cal[ii], wrt_file)
    gn.neighbors(el, ns_val[ii], H, ext, set_id_val[ii], wrt_file)

"""perform the regression to calibrate the real-space, limited range
MKS function"""
gr.regress(el, ns_cal[0], H, ext, set_id_cal[0], wrt_file)

"""perform the validation of the regression"""
gv.validate(el, ns_cal[0], H, ext, set_id_cal[0], wrt_file)
gv.validate(el, ns_val[0], H, ext, set_id_val[0], wrt_file)
