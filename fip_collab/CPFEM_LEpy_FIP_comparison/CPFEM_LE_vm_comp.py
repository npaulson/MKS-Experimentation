# -*- coding: utf-8 -*-
"""
Created on Thursday, August 14th, 2014


@author: nhpnp3
"""

import numpy as np
import functions_comparison as rr
import matplotlib.pyplot as plt
import time

typ = 'ePl'
comp = 'VM' # the strain component to be analyzed
cyc = 3 # the current strain cycle
st_comp = "%s%s" %(typ,comp)
comp_latex = "$\epsilon_{%sp}$" %comp


## el is the # of elements per side of the cube 
el = 21 
    
## specify the file to write messages to 
wrt_file = 'data_%s%s_cyc%s_%s.txt' %(typ,comp,cyc,time.strftime("%Y-%m-%d_h%Hm%M"))


### READ DATA FROM TEXT FILE ###
filename = "Results_Prebuilt_HCP_SinglePhase_Output_FakeMatl_1_0mm_9261el_PowerLaw_data_strain_pl_max_C3.txt"
C_CPFEM = rr.file_read_vm(filename)

filename = "Results_Prebuilt_HCP_SinglePhase_Output_FakeMatl_1_0mm_9261el_LinElast_data_strain_pl_max_C3.txt"
C_LE = rr.file_read_vm(filename)


MASE,MAX_ERR = rr.data_gen(C_CPFEM=C_CPFEM,C_LE=C_LE,cyc=cyc,typ=typ,comp=comp,comp_latex=comp_latex,st_comp=st_comp,wrt_file=wrt_file)




    







