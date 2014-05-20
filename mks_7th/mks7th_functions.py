# -*- coding: utf-8 -*-
"""
ABAQUS .dat to 21x21x21 dataset

Noah Paulson, 3/27/2014
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio

def gen_micr(file_name, read_dat, ns, el):
    """
    generate the microstructure array from the matlab file
    """
    if read_dat == 1:        
        pre_micr = sio.loadmat(file_name)    
        pre_micr = pre_micr['M'].astype(int)   
        
        micr = np.zeros((el,el,el,ns)) 
        for jj in range(ns):    
            micr[:,:,:,jj] = np.swapaxes(np.reshape(np.flipud(pre_micr[:,jj]), [el,el,el]),1,2)
    
        np.save('micr',micr)
    else:        
        micr = np.load('micr.npy')
    return micr

def independent_columns(A, tol = 1e-05):
    """
    This function is from: http://stackoverflow.com/q/13312498

    Returns an array composed of independent columns of A.

    Note that answer may not be unique; this function returns one of many
    possible answers.
    """
    Q, R = np.linalg.qr(A)
    independent = np.where(np.abs(R.diagonal()) > tol)[0]
    #return A[:, independent]
    return independent


def pha_loc(filename = "msf.txt", el = 21):   
    """
    Opens file with microstructure info where is column represents a single
    microstructure. Converts each microstructure column vector into a 
    cube data structure with indexing which matches that of the 
    Finite Element structure
    
    Inputs: 'filename', 'ns'== number of microstructures

    Output: 21x21x21xns array where ns is the microstructure index    
    
    """
    
    f = open(filename, "r")

    linelist = f.readlines()
    
    ns = len(linelist[0].split())    
    pre_micr1 = np.zeros((21**3,ns))    
    
    for ii in range(21**3):
        for jj in range(ns):
            pre_micr1[ii,jj] = linelist[ii].split()[jj]

    f.close()
            
    # element 4630 is at the centroid of a 21x21x21 dataset
    #print e11cond[4630]

    # here we reshape the data from a 9261 length vector to a 21x21x21 3D matrix
        
    pre_micr2 = np.zeros((21,21,21,ns))
    micr = pre_micr2
    
    for jj in range(ns):    
        pre_micr2 = np.reshape(np.flipud(pre_micr1[:,jj]), [21,21,21])
        micr[:,:,:,jj] = np.swapaxes(pre_micr2,1,2)
        
    return [micr, ns]

   
def remzer(r_ini):  
    """
    This function shrinks a vector by removing the zeros.
    NOTE: Find a better way to do this    
    """
    c = 0
    r = np.zeros(len(r_ini))
    for ii in range(len(r_ini)):
        if r_ini[ii] != 0:
            
            r[c] = r_ini[ii]        
            
            c = c + 1
    
    return np.trim_zeros(r)


def res_red(filename = "21_1_noah.dat", el = 21, slc = 10):
    """
    This function reads the E11 values from a .dat file and reorganizes the
    data into a el x el x el array with the correct organization
    
    It will also plot a certain x-slice in the dataset if called within this
    script
    """
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
    
    f.close()    
    
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
                
        plt.imshow(e11mat[slc,:,:], origin='lower', interpolation='none',
                   cmap='jet')
        
        plt.colorbar()
        
    else:
        return e11mat

res_red