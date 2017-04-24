import vtk_read as vtk
import get_response as gr
from constants import const
import h5py

C = const()
dir_fip = 'fip'
ns_max = 500

# """get the data for the linkage"""
# f = h5py.File("raw_responses.hdf5", 'w')
# f.close()

# """Gather data from vtk files"""
# vtk.read_fip('BaTrTr', ns_max, dir_fip)

f = h5py.File("responses.hdf5", 'w')
f.create_dataset("gamma_coefs", (ns_max, 4))
f.close()

"""get the fitting coefficients for the linkage"""
for ns in xrange(1, ns_max+1):
    gr.resp(ns, ns_max, 'BaTrTr')
