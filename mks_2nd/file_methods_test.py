# -*- coding: utf-8 -*-
"""
Created on Tue Apr 08 15:02:51 2014

@author: nhpnp3
"""
import os

# return the working directory
cwd = os.getcwd()
print cwd

# change the working directory
os.chdir("C:/Users/nhpnp3/Documents/GitHub/MKS_repository/MKS_2nd/noah_sq_dat_files")
cwd = os.getcwd()
print cwd

# go back to the original directory
os.chdir("C:/Users/nhpnp3/Documents/GitHub/MKS_repository/MKS_2nd")
cwd = os.getcwd()
print cwd
