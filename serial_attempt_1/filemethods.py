# -*- coding: utf-8 -*-
"""
Created on Thu May 08 19:33:25 2014

@author: nhpnp3
"""
import time
import mks_functions_serial as rr



filename = 'output.txt'
msg = 'hi %s. you are the %s' %('fartface','the worst')

rr.WP(msg,filename)

time.sleep(30)

msg = 'fart poop'

rr.WP(msg,filename)