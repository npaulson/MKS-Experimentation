# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 20:20:42 2014

@author: Noah
"""

from IPython.parallel import Client
import numpy as np
import time
from functools import partial

n = 100
m = 25
rc = Client()
dview = rc[:]

def f_open(ii,f):
    filename = 'R_%s' % ii
    f[ii] = open(filename, 'a')
#    f.append(open(filename, 'a'))

def f_write(ii,f,T):  
    f[ii].write(str(T[ii]) + '\n')    

def f_close(ii,f):
    f[ii].close()

            
start = time.time()

f = []
for ii in xrange(n):
    f.append(ii)
    
print f


#rc[:]['f_open'] = f_open
f_open_par = partial(f_open, f=f)
rc[:]['f_open_par'] = f_open_par
#map(f_open_par, range(n))
dview.map_sync(f_open_par, range(n))

print f


for jj in xrange(m):
    T = np.linspace(n*jj, n*jj + (n - 1), num = n)

    f_write_par = partial(f_write, f=f, T=T)        
    map(f_write_par, range(n))
#    dview.map_sync(f_write_par, range(n))


#f_close_par = partial(f_close, f=f)      
#map(f_close_par, range(n))
##dview.map_sync(f_close_par, range(n))
#
#end = time.time()
#print "elapsed time: %s s" % (end - start)
            
        
 



