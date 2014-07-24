# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 20:20:42 2014

@author: Noah
"""

import numpy as np
import time

n = 1000
m = 25
#R = np.random.rand(n,m)

#### Save each row of R in '.npy' format
#start = time.time()
#for ii in range(len(R[:,0])):
#    filename = 'R_%s' % ii    
#    np.save(filename,R[ii,:])    
#end = time.time()
#timeE = np.round((end - start),5)
#print "time to save each row in '.npy' format: %s seconds" % timeE
#
#### Save each row of R in '.txt' format using numpy
#start = time.time()
#for ii in range(len(R[:,0])):
#    filename = 'R_%s' % ii    
#    np.savetxt(filename,R[ii,:])    
#end = time.time()
#timeE = np.round((end - start),5)
#print "time to save each row in '.txt' format: %s seconds" % timeE
#
#### Save each row of R in '.txt' format by opening and writing individually
#start = time.time()
#for ii in range(len(R[:,0])):
#    filename = 'R_%s' % ii    
#    f = open(filename, 'a')    
#    for jj in xrange(len(R[0,:])):    
#        f.write(str(R[ii,jj]) + '\n')
#    f.close()
#end = time.time()
#timeE = np.round((end - start),5)
#print "time to save each row in '.txt' format: %s seconds" % timeE


def keep_open():
#### The task is append each value in the vector T (of length n) to a file
#### matching its index for m randomly generated T's.
    f = []
    
    for ii in xrange(n):
        filename = 'R_%s' % ii    
        f.append(open(filename, 'a'))
    
    for jj in xrange(m):
    
        T = np.random.rand(n)    
        
        for ii in xrange(n):
            filename = 'R_%s' % ii    
            f[ii].write(str(T[ii]) + '\n')
    
    for ii in xrange(n):
        f[ii].close()

    
def closed():  
    c = 0    
    for jj in xrange(m):
    
        T = np.random.rand(n)    
        
        for ii in xrange(n):
            c += 1            
            filename = 'Rr_%s' % c    
            f = open(filename, 'a')
            f.write(str(T[ii]) + '\n')
            f.close()
            
if __name__ == "__main__":
    start = time.time()
    keep_open()
    end = time.time()
    print "elapsed time: %s" % (end - start)
            
        
 



