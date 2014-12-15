# -*- coding: utf-8 -*-
"""
Created on Mon Dec 01 12:33:23 2014

@author: nhpnp3
"""
import sympy as sy


I = sy.eye(3)

print I

e11,e12,e13,e22,e23,e33 = sy.symbols('e11 e12 e13 e22 e23 e33')
f12,f13,f21,f23,f31,f32 = sy.symbols('f12 f13 f21 f23 f31 f32')

Ecauchy = sy.Matrix([[e11,e12,e13],[e12,e22,e23],[e13,e23,e33]])

print Ecauchy

Felast = sy.Matrix([[1+e11,f12,f13],[f21,1+e22,f23],[f31,f32,1+e33]])

print Felast

mateq = 2 * Ecauchy + I - Felast.T * Felast

print mateq

