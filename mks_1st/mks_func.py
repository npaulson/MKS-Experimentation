# -*- coding: utf-8 -*-
"""
Created on Tue Mar 25 13:06:24 2014

@author: nhpnp3
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio

def pha_loc(filename = "msf.txt"):
    
    f = open(filename, "r")

    linelist = f.readlines()
    
    pre_micr1 = np.zeros((21**3,3))    
    
    for ii in range(21**3):
        for jj in range(3):
            pre_micr1[ii,jj] = linelist[ii].split()[jj]

    f.close()
            
    # element 4630 is at the centroid of a 21x21x21 dataset
    #print e11cond[4630]

    # here we reshape the data from a 9261 length vector to a 21x21x21 3D matrix
        
    pre_micr2 = np.zeros((21,21,21,3))
    micr = pre_micr2
    
    for jj in range(3):    
        pre_micr2 = np.reshape(np.flipud(pre_micr1[:,jj]), [21,21,21])
        micr[:,:,:,jj] = np.swapaxes(pre_micr2,1,2)
        
    return micr
    
def gen_micr(file_name, read_dat, ns, el):
    """
    Summary:
        This function reads the microstructures for all samples (calibration
        and validation) from a matlab data file, rearanges them into ns # of
        el x el x el cubes, and saves them in the .npy file format
    Inputs:
        file_name (string): the filename for the matlab '.mat' file
        read_dat (int): if read_dat = 1 the '.mat' file is read and rearanged,
        if read_dat = 0 micr is simply loaded from the '.npy' file
        ns (int): the total number of microstructures (for calibration and 
        validation)
        el (int): the number of elements per side of the microstructure cube
    Output:
        micr ([el,el,el,ns],int8): The binary microstructures for calibration
        and validation
    """
    if read_dat == 1:        
        ## convert the matlab file to an array in python        
        pre_micr = sio.loadmat(file_name)    
        pre_micr = pre_micr['micr'].astype(int)   
        
        ## here we perform flips and reshapes to enact the proper arrangement 
        ## of spatial locations in the 3D cub
        micr = np.zeros((el,el,el,ns),dtype = 'int8') 
        for jj in range(ns):    
            micr[:,:,:,jj] = np.swapaxes(np.reshape(np.flipud(pre_micr[:,jj]), [el,el,el]),1,2)
    
        ## save the microstructure array
        np.save('micr_%s' %ns,micr)
    else:        
        micr = np.load('micr_%s.npy' %ns)
    
    return micr
    

def res_red(filename = "21_1_noah.dat", slice=10):
    
    f = open(filename, "r")

    linelist = f.readlines()

    # finds a location several lines above the start of the data
    # linelist[n] reads the entire line at location n
    for n in range(1000):
        if 'THE FOLLOWING TABLE' in linelist[n]:
            break

    # line0 is the index of first line of the data
    line0 = n + 5;      

    e11 = np.zeros((21**3,8))
    c = 0

    # this series of loops generates a 9261x8 dataset of E11s (element x integration point) 
    for ii in range(21**3):
        for jj in range(8):
            e11pre = linelist[line0 + c].split()[2]
            c = c + 1
            e11[ii,jj] = float(e11pre)

    # here we average all 8 integration points in each element cell
    e11cond = np.flipud(np.mean(e11, axis=1))
    # element 4630 is at the centroid of a 21x21x21 dataset
    #print e11cond[4630]

    # here we reshape the data from a 9261 length vector to a 21x21x21 3D matrix
    pre_e11mat = np.reshape(e11cond, [21,21,21])
    e11mat = np.swapaxes(pre_e11mat,1,2)


    # here we generate an image and scalebar for a particular slice of the 3D matrix
    if __name__ == '__main__':
        
        plt.clf()        
                
        plt.imshow(e11mat[slice,:,:], origin='lower', interpolation='none',
                   cmap='jet')
        
        plt.colorbar()
        
    else:
        return e11mat


def independent_columns(A, tol = 1e-05):
    """
    The following code is comes from: http://stackoverflow.com/q/13312498

    Return an array composed of independent columns of A.

    Note the answer may not be unique; this function returns one of many
    possible answers.
    """
    Q, R = np.linalg.qr(A)
    independent = np.where(np.abs(R.diagonal()) > tol)[0]
    #return A[:, independent]
    return independent
    
    
def remzer(r_ini):  
    
    c = 0
    r = np.zeros(len(r_ini))
    for ii in range(len(r_ini)):
        if r_ini[ii] != 0:
            
            r[c] = r_ini[ii]        
            
            c = c + 1
    
    return np.trim_zeros(r)

    
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
