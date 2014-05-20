# -*- coding: utf-8 -*-
"""
Created on Wed Apr 09 15:03:10 2014

This code examines the standard indexing order of N-D arrays and the use of
the roll function in numpy

@author: nhpnp3
"""
import numpy as np

# generate a 3x3x3 array with values ranging from 0 to 26
lin = np.arange(3**3)
micr = np.reshape(lin,[3,3,3])

# with the next two lines I proved to myself that python chooses to use the 
# first index (call it the x index) to show slices of a 3-D array
print micr
#print micr[0,:,:]

# the roll function allows you to choose a number of increments (+ or -) and a 
# direction where 0 rolls in x, 1 rolls in y and 2 rolls in z. When looking at
# a 3-D array sliced in the x direction, choosing roll(~,~,0) cycles the
# slices, roll(~,~,1) shifts the numbers in each slice down, and roll(~,~,2)
# shifts the numbers in each slice to the right.
roll_micr = np.roll(micr,1,0)
print roll_micr

print "specific case"

print micr[0,:,:]
print roll_micr[1,:,:]