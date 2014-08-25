# -*- coding: utf-8 -*-
"""
Functions connected to 3D, isotropic MKS analyses

In general these functions are not for parallel processing or chunking of data

Noah Paulson, 5/28/2014
"""

import numpy as np
import vtk

def eval_meas(mks_R_indv,resp_indv,el):
    """
    Summary: Calculates the MASE and average error
    Inputs:
        mks_R ([el,el,el],float): The response predicted by the MKS for
        validation microstructures
        resp ([el,el,el],float): the FEM responses of all microstructures
        el (int): The number of elements per side of the 'cube'
    Outputs:
        avgE (float): The average strain value for the microstructure
        MASE (float): Mean Absolute Square Error
    """
    avgE_mks = np.average(mks_R_indv)
    avgE_fe= np.average(resp_indv)
    MASE = 0
    for k in xrange(el**3):
        [u,v,w] = np.unravel_index(k,[el,el,el])
        MASE += ((np.abs(resp_indv[u,v,w] - mks_R_indv[u,v,w]))/(avgE_fe * el**3))
        
    return avgE_fe,avgE_mks, MASE


def file_read(filename, column_num, el):
    
    f = open(filename, "r")
    
    linelist = f.readlines()
    
    # line0 is the index of first line of the data
    line0 = 2;      
    
    E_pre = np.zeros((21**3))
    c = -1
    
    ## This reads through all the lines in the file.
     
    for k in xrange(21**3):
        c += 1                        
        E_pre[k] = linelist[line0 + c].split()[column_num]
    
    f.close()    
         
    E = np.swapaxes(np.reshape(np.flipud(E_pre), [el,el,el]),1,2)

    return E


def read_vtk(filename):
    """
    Summary:
        Much of this code was taken from Matthew Priddy's example
        file.
    Inputs:
    Outputs:
    """
    
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
    
    elx = vec[0]
    	
    # Calculate the total number of elements
    el_total = elx * elx * elx

    Euler   = data.GetCellData().GetArray(reader.GetVectorsNameInFile(0))
#    grain_ID = data.GetCellData().GetArray(reader.GetScalarsNameInFile(0))    
#    FIP_FS  = data.GetCellData().GetArray(reader.GetScalarsNameInFile(1))
    E11tot  = data.GetCellData().GetArray(reader.GetTensorsNameInFile(1))    
#    E11pl = data.GetCellData().GetArray(reader.GetTensorsNameInFile(2))
    
#    fip_py = np.zeros([el_total])
#    grain_id_py = np.zeros([el_total])
    euler_py = np.zeros([el_total, 3])    
    E11tot_py = np.zeros([el_total])        
#    E11pl_py = np.zeros([el_total])    
    
#    for ii in range(el_total):
#        grain_id_py[ii] = grain_ID.GetValue(ii)        
    
#    for ii in xrange(el_total):
#        fip_py[ii] = FIP_FS.GetValue(ii)
    
    # Example of storing vector data# Note: check and make sure this is done correctly.
    for ii in xrange(el_total):
        euler_py[ii,0] = Euler.GetValue(ii*3 + 0)
        euler_py[ii,1] = Euler.GetValue(ii*3 + 1)
        euler_py[ii,2] = Euler.GetValue(ii*3 + 2)
    
    for ii in xrange(el_total):
        E11tot_py[ii] = E11tot.GetValue(ii*9)
#        tensor1[ii,0] = StressT_Max.GetValue(ii*9 + 0)
#        tensor1[ii,1] = StressT_Max.GetValue(ii*9 + 1)
#        tensor1[ii,2] = StressT_Max.GetValue(ii*9 + 2)
#        tensor1[ii,3] = StressT_Max.GetValue(ii*9 + 3)
#        tensor1[ii,4] = StressT_Max.GetValue(ii*9 + 4)
#        tensor1[ii,5] = StressT_Max.GetValue(ii*9 + 5)
#        tensor1[ii,6] = StressT_Max.GetValue(ii*9 + 6)
#        tensor1[ii,7] = StressT_Max.GetValue(ii*9 + 7)
#        tensor1[ii,8] = StressT_Max.GetValue(ii*9 + 8)

#    for ii in xrange(el_total):
#        E11pl_py[ii] = E11pl.GetValue(ii*9)
#
#    E11_py = E11tot_py - E11pl_py    
    
    return euler_py


def res_red(filename):
    """
    Summary:    
        This function reads the E11 values from a .dat file and reorganizes
        the data into a el x el x el array with the correct organization
        It will also plot a certain x-slice in the dataset if called within
        this script.
    Inputs:
        filename (string): the name of the '.dat' file containing the 
        FEM response
        ori_mat ([3,3,el^3,ns],float): an array containing the orientation
        matrices (g) for each spatial location of each RVE in the set      
        el (int): the number of elements per side of the microstructure cube
    Outputs:
        Emat ([el,el,el],float): the FEM response of the '.dat' file of
        interest
    """
    el = 21    
    
    f = open(filename, "r")

    linelist = f.readlines()

    # finds a location several lines above the start of the data
    # linelist[n] reads the entire line at location n
    for ln in xrange(1000):
        if 'THE FOLLOWING TABLE' in linelist[ln]:
            break

    # line0 is the index of first line of the data
    line0 = ln + 5;      

    E = np.zeros(21**3)
    c = -1

    # this series of loops generates a 9261x8 dataset of E11s (element x integration point) 
    for k in xrange(21**3):
        c += 1                        
        E[k] = linelist[line0 + c].split()[3]
    
    f.close()    
    
    # here we reshape the data from a 9261 length vector to a 21x21x21 3D matrix       
    Emat = np.swapaxes(np.reshape(np.flipud(E), [el,el,el]),1,2)

    return Emat
    

def WP(msg,filename):
    """
    Summary:
        This function takes an input message and a filename, and appends that
        message to the file. This function also prints the message
    Inputs:
        msg (string): the message to write and print.
        filename (string): the full name of the file to append to.
    Outputs:
        both prints the message and writes the message to the specified file
    """
    fil = open(filename, 'a')
    print msg
    fil.write(msg)
    fil.write('\n')
    fil.close()
