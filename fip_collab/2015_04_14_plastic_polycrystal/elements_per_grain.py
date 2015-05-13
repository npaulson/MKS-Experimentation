import os
import vtk
import numpy as np


def read_scalar(el, ns):

    grain = np.zeros([ns, el**3])
    avg_GS = np.zeros([ns, 1])

    wd = os.getcwd()

    sn = 0
    for filename in os.listdir(wd):
        if filename.endswith('.vtk'):
            grain[sn, :] = read_vtk_scalar(filename=filename)
            avg_GS[sn] = el**3 / np.max(grain[sn, :])
            sn += 1

    print np.mean(avg_GS)
    print np.std(avg_GS)


def read_vtk_scalar(filename):

    # Initialize the reading of the VTK microstructure created by Dream3D
    reader = vtk.vtkDataSetReader()
    reader.SetFileName(filename)
    reader.ReadAllTensorsOn()
    reader.ReadAllVectorsOn()
    reader.ReadAllScalarsOn()
    reader.Update()
    data = reader.GetOutput()
    dim = data.GetDimensions()
    vec = list(dim)
    vec = [i-1 for i in dim]

    el = vec[0]

    # Calculate the total number of elements
    el_total = el**3

    Scalar = data.GetCellData().GetArray(reader.GetScalarsNameInFile(0))

    scalar_py = np.zeros([el_total])

    for ii in xrange(el_total):
        scalar_py[ii] = Scalar.GetValue(ii)

    return scalar_py


if __name__ == "__main__":
    read_scalar(21, 300)
