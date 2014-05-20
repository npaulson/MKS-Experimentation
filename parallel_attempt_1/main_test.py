# -*- coding: utf-8 -*-
"""
Created on Wed May 14 15:39:09 2014

@author: nhpnp3
"""

import multiprocessing as mult
from functools import partial

def fart(c,b):
    return b*c


if __name__ == '__main__':
    
    fart_part = partial(fart,b=1)    
    
    po = mult.Pool()
#    result = map(fart_part, range(5))
    result = po.map(fart_part, range(5))        
    
    po.close()
    po.join()    
    
    print result