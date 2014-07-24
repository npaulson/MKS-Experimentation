# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 20:20:42 2014

@author: Noah
"""

from IPython.parallel import Client
import numpy as np
import time
from functools import partial

n = 5
m = 250
rc = Client()
dview = rc[:]

def f_open(ii,f):
    filename = 'R_%s' % ii
    ii_name = 'a' + str(ii)
    f[ii_name] = open(filename, 'a')

def f_write(ii,f,T):  
    ii_name = 'a' + str(ii)
    f[ii_name].write(str(T[ii]) + '\n')    

def f_close(ii,f):
    ii_name = 'a' + str(ii)    
    f[ii_name].close()

            
start = time.time()

f = dict()

#rc[:]['f_open'] = f_open
f_open_par = partial(f_open, f=f)
#rc[:]['f_open_par'] = f_open_par
map(f_open_par, range(n))
#dview.map_sync(f_open_par, range(n))

dview.push(dict(f = f))
ar = dview.pull('f')
print ar.get()

print f

end = time.time()
print "file open, elapsed time: %s s" % (end - start)



#start = time.time()
#
##rc[:]['f_write'] = f_write
#
#for jj in xrange(m):
#    T = np.linspace(n*jj, n*jj + (n - 1), num = n)
#
#    f_write_par = partial(f_write, f=f, T=T)            
##    map(f_write_par, range(n))
#    dview.map_sync(f_write_par, range(n))
#
#end = time.time()
#print "file write, elapsed time: %s s" % (end - start)



start = time.time()

rc[:]['f_close'] = f_close    
f_close_par = partial(f_close, f=f)
#map(f_close_par, range(n))
dview.map_sync(f_close_par, range(n))

end = time.time()
print "file close, elapsed time: %s s" % (end - start)


            
        
 



