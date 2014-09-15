# -*- coding: utf-8 -*-
"""
Functions connected to 3D, isotropic MKS analyses

In general these functions are not for parallel processing or chunking of data

Noah Paulson, 5/28/2014
"""

import numpy as np
import time
import scipy.io as sio

def load_fe(ori_file,dat_file,el):
    """    
    Summary:        
        This function loads the finite element (FE) responses from '.dat' 
        files. This version is used for files with orientation information
    Inputs:
        filename (string): The '.mat' file containing orientation information
        for the set of microstructures
        set_id (string): The set - ID        
        ns (int): the total number microstructures (calibration or validation)
        el (int): the number of elements per side of the microstructure cube        
    Outputs:
        resp ([el,el,el,ns],float): The FEM responses of all calibration or 
        validation microstructures
        msg (string): A message detailing how resp was loaded
    """    

    start = time.time()    

    micr_flag_BASE = sio.loadmat(ori_file)
    ## ori_mats contains a 3x3 orientation matrix for each spatial location
    ## in each sample microstructure
    ori_mat = micr_flag_BASE['orientation']

    resp = res_red(dat_file,ori_mat,el)  
    
    end = time.time()
    timeE = np.round((end - start),1)
    msg = "Import FE results: %s seconds" %timeE
    
    return [resp,msg]


def res_red(filename,ori_mat,el):
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
    f = open(filename, "r")

    linelist = f.readlines()

    # finds a location several lines above the start of the data
    # linelist[n] reads the entire line at location n
    for ln in xrange(1000):
        if 'THE FOLLOWING TABLE' in linelist[ln]:
            break

    # line0 is the index of first line of the data
    line0 = ln + 5;      

    E = np.zeros((21**3,8,6))
    c = -1

    # this series of loops generates a 9261x8 dataset of E11s (element x integration point) 
    for k in xrange(21**3):
        for jj in xrange(8):
            c += 1                        
            E[k,jj,:] = linelist[line0 + c].split()[3:]
    
    f.close()    
    
    # here we average all 8 integration points in each element cell
    E = np.mean(E, axis=1)
    
    Etot = np.zeros([el**3])
    # here we convert the strain tensor at each location from crystal to 
    # sample frame
    for k in xrange(21**3):
        # E_ten_cry is the strain tensor at the spatial location of interest
        # in the crystal frame
        E_ten_cry = np.array([[    E[k,0], 0.5*E[k,3], 0.5*E[k,4]],
                              [0.5*E[k,3],     E[k,1], 0.5*E[k,5]],
                              [0.5*E[k,4], 0.5*E[k,5],     E[k,2]]])
        # Here we convert from crystal to sample frame
        E_ten_samp = np.dot(ori_mat[:,:,k].T ,np.dot(E_ten_cry,ori_mat[:,:,k]))
                
        Etot[k] = E_ten_samp[0,0]
#        Etot[k,:] = [E_ten_samp[0,0],E_ten_samp[1,1],E_ten_samp[2,2],
#                     E_ten_samp[0,1],E_ten_samp[1,2],E_ten_samp[1,2]]
    
    # here we reshape the data from a 9261 length vector to a 21x21x21 3D matrix       
    Emat = np.swapaxes(np.reshape(np.flipud(Etot), [el,el,el]),1,2)

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
