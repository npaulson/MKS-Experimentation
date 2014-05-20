# -*- coding: utf-8 -*-
"""
Created on Wed May 14 15:39:09 2014

@author: nhpnp3
"""
from multiprocessing import Pool


def multiply(a,b,c):
    return a*b*c
    
def pre_multiply(c):
    return multiply(1,2,c)

print multiply(1,2,3)
print pre_multiply(3)

if __name__ == '__main__':
    pool = Pool()    
    results = pool.map(pre_multiply,range(4))
    print results