# -*- coding: utf-8 -*-
"""
ABAQUS .dat to 21x21x21 dataset

Noah Paulson, 3/27/2014
"""
def pha_loc(filename = "msf.txt"):
    
    import numpy as np    
    
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
    
    

def res_red(filename = "21_1_noah.dat", slice=10):

    import matplotlib.pyplot as plt
    import numpy as np
    
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

res_red(filename = "21_1_noah.dat", slice=10)