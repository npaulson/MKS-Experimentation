import vtk_read as vtk
import get_response as gr
import h5py
import numpy as np


C = {}

C['el'] = 21

C['names'] = ['Ac', 'BaTr', 'Di', 'Id', 'Od', 'Ra', 'Tr',
              'BaTrTr', 'Dd', 'DdTr', 'DiTr', 'OdTr']
# C['names'] = ['Ac', 'BaTr', 'Di', 'Id', 'Od', 'Ra', 'Tr', 'Dd']
C['set_id'] = C['names']
C['strt'] = list(np.zeros(len(C['names']), dtype='int16'))
C['ns'] = list(20*np.ones(len(C['names']), dtype='int16'))
C['dir'] = C['names']
C['dir_resp'] = "response"

f = h5py.File("euler_all.hdf5", 'w')
f.close()

for ii in xrange(len(C['set_id'])):
    vtk.read_euler(C, C['strt'][ii], C['ns'][ii],
                   C['set_id'][ii], C['dir'][ii], 0)

f = h5py.File("responses_all.hdf5", 'w')
f.close()

bc = 'bc1'
for ii in xrange(len(C['set_id'])):
    gr.resp(C, C['ns'][ii], C['strt'][ii], C['names'][ii],
            C['set_id'][ii], bc, C['dir_resp'])
