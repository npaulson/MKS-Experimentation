import vtk_read as vtk
import get_response as gr
from constants import const
import h5py

C = const()

set_id = C['set_id']
strt = C['strt']
ns = C['ns']
direc = C['direc']
names = C['names']

f = h5py.File("data.hdf5", 'w')
f.close()

"""Gather data from vtk files"""
for ii in xrange(len(set_id)):
    vtk.read_euler(strt[ii], ns[ii], names[ii],
                   direc[ii], 0)

    for bc in ['bc1', 'bc2', 'bc3']:
        gr.resp(ns[ii], strt[ii], names[ii],
                set_id[ii], bc, C['dir_resp'])
