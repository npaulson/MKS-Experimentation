#
#  Read_VTK_into_Python.py
#  
#  Created by Matthew Priddy on 6/12/2014.

#  This program will read data from VTK file formats and place the data into arrays for use in Python.
#
# Note: To output numbers with decimal places, input numbers with
#		decimal places.  One strange thing about Python.
#
# Some helpful web pages about VTK and paraview
# http://www.paraview.org/Wiki/Animating_legacy_VTK_file_series
# http://www.earthmodels.org/software/vtk-and-paraview/vtk-file-formats
# 
#
import sys, os
import linecache
import math
from numpy import *
import vtk

# Input values for the mesh generator
filename     = 'CCMD_MgAZ31_ND'
filename_VTK = "Results_Ti64_RandomMicro_21x21x21_AbaqusInput_00025_data_v2_06.vtk"

# Initialize the reading of the VTK microstructure created by Dream3D
reader = vtk.vtkDataSetReader()
reader.SetFileName(filename_VTK)
reader.ReadAllTensorsOn()
reader.ReadAllVectorsOn()
reader.ReadAllScalarsOn()
reader.Update()
data = reader.GetOutput()
dim = data.GetDimensions()
vec = list(dim)
vec = [i-1 for i in dim]

# Input variables for the mesh
elx        = vec[0]													# The number of elements per side of the cube
distance   = (data.GetPoint(1)[0] - data.GetPoint(0)[0])			# sidelength of an individual element (in microns?)
sidelength = distance * elx 										# Length in millimeters (mm)
	
# Calculate the total number of elements, nodes per side, total nodes, nodes per face,
# number of interior nodes per face, and number of perimeter nodes per face
el_total = elx * elx * elx
ndx      = (elx + 1)
nd_total = ndx * ndx * ndx

print reader.GetScalarsNameInFile(0)
print reader.GetScalarsNameInFile(1)
print reader.GetScalarsNameInFile(2)

print reader.GetVectorsNameInFile(0)
print reader.GetVectorsNameInFile(1)

print reader.GetTensorsNameInFile(0)
print reader.GetTensorsNameInFile(1)
print reader.GetTensorsNameInFile(2)
print reader.GetTensorsNameInFile(3)
print reader.GetTensorsNameInFile(4)
print reader.GetTensorsNameInFile(5)
print reader.GetTensorsNameInFile(6)

# Read in variables (scalars, vectors, and tensors) from the Vtk file
GrainID = data.GetCellData().GetArray(reader.GetScalarsNameInFile(0))
FIP_FS  = data.GetCellData().GetArray(reader.GetScalarsNameInFile(1))

Euler   = data.GetCellData().GetArray(reader.GetVectorsNameInFile(0))

StressT_Max  = data.GetCellData().GetArray(reader.GetTensorsNameInFile(0))
StressT_Min  = data.GetCellData().GetArray(reader.GetTensorsNameInFile(1))
StrainT_Max  = data.GetCellData().GetArray(reader.GetTensorsNameInFile(2))
StrainT_Min  = data.GetCellData().GetArray(reader.GetTensorsNameInFile(3))
StrainP_Max  = data.GetCellData().GetArray(reader.GetTensorsNameInFile(4))
StrainP_Min  = data.GetCellData().GetArray(reader.GetTensorsNameInFile(5))

# Illustration of the informationa associated with each CellData set
print GrainID
print Euler
print StressT_Max

scalar1 = zeros((el_total))
vector1 = zeros((el_total, 3))
tensor1 = zeros((el_total, 9))

# Example of storing scalar data
for i in range(el_total):
	scalar1[i] = GrainID.GetValue(i)
	
print scalar1

# Example of storing vector data
# Note: check and make sure this is done correctly.
for i in range(el_total):
	vector1[i,0] = Euler.GetValue(i*3 + 0)
	vector1[i,1] = Euler.GetValue(i*3 + 1)
	vector1[i,2] = Euler.GetValue(i*3 + 2)

print vector1

# Example of storing tensor data
# Note: check and make sure this is done correctly
for i in range(el_total):
	tensor1[i,0] = StressT_Max.GetValue(i*9 + 0)
	tensor1[i,1] = StressT_Max.GetValue(i*9 + 1)
	tensor1[i,2] = StressT_Max.GetValue(i*9 + 2)
	tensor1[i,3] = StressT_Max.GetValue(i*9 + 3)
	tensor1[i,4] = StressT_Max.GetValue(i*9 + 4)
	tensor1[i,5] = StressT_Max.GetValue(i*9 + 5)
	tensor1[i,6] = StressT_Max.GetValue(i*9 + 6)
	tensor1[i,7] = StressT_Max.GetValue(i*9 + 7)
	tensor1[i,8] = StressT_Max.GetValue(i*9 + 8)
	
print tensor1