# -*- coding: utf-8 -*-
"""
Functions connected to 3D, isotropic MKS analyses

In general these functions are not for parallel processing or chunking of data

Noah Paulson, 5/28/2014
"""

import numpy as np
import matplotlib.pyplot as plt
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


def file_read_vm(filename):
    
    el = 21    
    
    f = open(filename, "r")
    
    linelist = f.readlines()
    
    # line0 is the index of first line of the data
    line0 = 2;      
    
    Evm_pre = np.zeros((21**3))
    c = -1
    
    ## This reads through all the lines in the file.
     
    for k in xrange(21**3):
        c += 1                        
        
        st = np.zeros(6)
        for jj in range(6):
            st[jj] = linelist[line0 + c].split()[jj + 1]
            
        Evm_pre[k] = np.sqrt( 0.5*( (st[0]-st[1])**2 +(st[1]-st[2])**2 + (st[2]-st[0])**2 + 6*(st[3]**2 + st[4]**2 + st[5]**2) ) )

    
    f.close()    
         
    Evm = np.swapaxes(np.reshape(np.flipud(Evm_pre), [el,el,el]),1,2)

    return Evm


def mase_meas(C_cp,C_py,C_cp_avg):    
    el = 21    
    MASE = 0
    for k in xrange(el**3):
        [u,v,w] = np.unravel_index(k,[el,el,el])
        MASE += ((np.abs(C_cp[u,v,w] - C_py[u,v,w]))/(C_cp_avg * el**3))
        
    return MASE
    
    
def max_err_meas(C_cp,C_py,C_cp_avg):
    max_err = np.amax(C_cp-C_py)/C_cp_avg  
    
    return max_err


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
    
    return [euler_py, E11tot_py]


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


def data_gen(C_CPFEM,C_LE,cyc,typ,comp,comp_latex,st_comp,wrt_file):
### VISUAL COMPARISON OF CPFEM AND LE+PY SIMULATIONS ###

    plt.close('all')
    
    ## pick a slice perpendicular to the z-direction
    slc = 3
    el = 21    
    
    ## Plot slices of the response
    plt.figure(figsize=(11,4))
    
    ## find the min and max of both datasets for the slice of interest
    #(needed to scale both images the same) 
    dmin = np.amin([C_CPFEM[:,:,slc],C_LE[:,:,slc]])
    dmax = np.amax([C_CPFEM[:,:,slc],C_LE[:,:,slc]])
    
    plt.subplot(121)
    ax = plt.imshow(C_CPFEM[:,:,slc], origin='lower', interpolation='none',
        cmap='jet', vmin=dmin, vmax=dmax)
    plt.title('Cycle %s maximum, CPFEM, %s' %(cyc,comp_latex))
    plt.colorbar(ax)  
    
    plt.subplot(122)
    ax = plt.imshow(C_LE[:,:,slc], origin='lower', interpolation='none',
        cmap='jet', vmin=dmin, vmax=dmax)
    plt.title('Cycle %s maximum, LE, %s' %(cyc,comp_latex))
    plt.colorbar(ax)    
    
    plt.savefig('field_%s%s_cyc%s' %(typ,comp,cyc))
    
    # Plot a histogram representing the frequency of strain levels with separate
    # channels for each phase of each type of response.
    plt.figure(num=2,figsize=(11,5))
    
    
    C_CPFEM_lin = np.reshape(C_CPFEM,el**3)
    C_LE_lin = np.reshape(C_LE,el**3)
    
    ## find the min and max of both datasets
    dmin = np.amin([C_CPFEM,C_LE])
    dmax = np.amax([C_CPFEM,C_LE])
    
    # select the desired number of bins in the histogram
    bn = 40
    
    weight = np.ones_like(C_CPFEM_lin)/(el**3)
    
    ## response histograms
    
    n, bins, patches = plt.hist(C_CPFEM_lin, bins = bn, histtype = 'step', hold = True,
                                range = (dmin, dmax), weights=weight, color = 'white')
    bincenters = 0.5*(bins[1:]+bins[:-1])
    
    C_CPFEM_lin, = plt.plot(bincenters,n,'k', marker = 's', linestyle = '-', lw = 2.5)
    
    n, bins, patches = plt.hist(C_LE_lin, bins = bn, histtype = 'step', hold = True,
                                range = (dmin, dmax), weights=weight, color = 'white')
    
    C_LE_lin, = plt.plot(bincenters,n,'r', marker = 'o', linestyle = '-', lw = 1.0)
       
    
    plt.grid(True)
    
    plt.legend([C_CPFEM_lin, C_LE_lin], ["CPFEM", "LE"])
    
    plt.xlabel('%s' %comp_latex)
    plt.ylabel("Number Fraction")
    
    plt.title("Frequency comparison of %s in CPFEM and LE (cycle %s)" %(comp_latex,cyc))
    
    plt.savefig('hist_%s%s_cyc%s' %(typ,comp,cyc))
    
    
    ## Generate data file for statistical summary
    msg = 'Average %s, CPFEM, Cycle %s: %s' %(st_comp,cyc,np.average(C_CPFEM))
    WP(msg,wrt_file)
    msg = 'Average %s, LE, Cycle %s: %s' %(st_comp,cyc,np.average(C_LE))
    WP(msg,wrt_file)
    
    msg = 'Standard deviation %s, CPFEM, Cycle %s: %s' %(st_comp,cyc,np.std(C_CPFEM))
    WP(msg,wrt_file)
    msg = 'Standard deviation %s, LE, Cycle %s: %s' %(st_comp,cyc,np.std(C_LE))
    WP(msg,wrt_file)    
    
    msg = 'Minimum %s, CPFEM, Cycle %s: %s' %(st_comp,cyc,np.min(C_CPFEM))
    WP(msg,wrt_file)
    msg = 'Minimum %s, LE, Cycle %s: %s' %(st_comp,cyc,np.min(C_LE))
    WP(msg,wrt_file)
    
    msg = 'Maximum %s, CPFEM, Cycle %s: %s' %(st_comp,cyc,np.max(C_CPFEM))
    WP(msg,wrt_file)
    msg = 'Maximum %s, LE, Cycle %s: %s' %(st_comp,cyc,np.max(C_LE))
    WP(msg,wrt_file)
    
    MASE = mase_meas(C_CPFEM,C_LE,np.average(C_CPFEM))*100
    msg = 'Mean absolute strain error (MASE), Cycle %s: %s%%' %(cyc,MASE)
    WP(msg,wrt_file)
    
    MAX_ERR = max_err_meas(C_CPFEM,C_LE,np.average(C_CPFEM))*100
    msg = 'Maximum error, Cycle %s: %s%%' %(cyc,MAX_ERR)
    WP(msg,wrt_file)

    return (MASE, MAX_ERR)