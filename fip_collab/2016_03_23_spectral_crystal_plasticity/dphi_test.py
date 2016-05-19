import numpy as np
import sys

degA = np.float32(sys.argv[1])*(np.pi/180.)
degB = np.float32(sys.argv[2])*(np.pi/180.)

d_phi = degB-degA

ver_a = d_phi*np.sin((degA+degB)/2.)
ver_b = (-np.cos(degB))-(-np.cos(degA))

# ver_a = ver_a*d_phi**3
# ver_b = ver_b*d_phi**3

print "ver_a: %s" % ver_a
print "ver_b: %s" % ver_b
