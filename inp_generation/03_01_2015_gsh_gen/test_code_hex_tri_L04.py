phi1 = .1
phi = .2
phi2 = .3

import math
import numpy

t1 = math.sin(phi)
t2 = math.sin(phi1)
t3 = math.cos(phi1)
t4 = t1 ** 2
t5 = -t3 ** 2 * t4 + 0.1e1
t6 = t5 ** (-0.1e1 / 0.2e1)
t7 = math.cos(phi)
t8 = t7 * t6
t9 = t1 * t2
t10 = t9 * t6
t5 = t5 * t6
t1 = t1 * t3
t11 = phi - math.atan2(t5, t1)
t12 = math.cos(phi2)
t13 = math.sin(phi2)
t14 = t13 * t3
t15 = t12 * t2
t3 = t12 * t3
t12 = t13 * t2
t13 = (t14 * t7 + t15) * t6
t6 = (-t3 * t7 + t12) * t6
t16 = phi2 - math.atan2(-t13, t6)
t5 = phi - math.atan2(t5, -t1)
t6 = phi2 - math.atan2(t13, -t6)
t2 = -t4 * t2 ** 2 + 0.1e1
t4 = t2 ** (-0.1e1 / 0.2e1)
t13 = t7 * t4
t1 = t1 * t4
t2 = t2 * t4
t17 = phi - math.atan2(t2, -t9)
t3 = (-t12 * t7 + t3) * t4
t4 = (t15 * t7 + t14) * t4
t7 = phi2 - math.atan2(-t3, t4)
t2 = phi - math.atan2(t2, t9)
t3 = phi2 - math.atan2(t3, -t4)
t4 = -0.2e1 * phi1
t9 = math.pi / 0.2e1
TempExpr = numpy.mat([[-phi1 + math.atan2(t10, -t8),-t11,-t16],[-phi1 + math.atan2(t10, t8),-t5,-t6],[0,0,0],[-phi1 + math.atan2(-t8, -t10),-t11,-t16],[-phi1 + math.atan2(-t13, -t1),-t17,-t7],[-phi1 + math.atan2(-t8, t10),-t5,-t6],[-phi1 + math.atan2(-t13, t1),-t2,-t3],[t4 - t9,-math.pi,0],[-phi1 + math.atan2(t1, -t13),-t17,-t7],[t9,0,0],[-phi1 + math.atan2(t1, t13),-t2,-t3],[math.pi + t4,-math.pi,0],[-phi1 + math.atan2(-t10, t8),-t11,-t16],[-math.pi,0,0],[-phi1 + math.atan2(-t10, -t8),-t5,-t6],[-phi1 + math.atan2(t8, t10),-t11,-t16],[-phi1 + math.atan2(t13, t1),-t17,-t7],[-phi1 + math.atan2(t8, -t10),-t5,-t6],[-phi1 + math.atan2(t13, -t1),-t2,-t3],[t4 + t9,-math.pi,0],[-phi1 + math.atan2(-t1, t13),-t17,-t7],[-t9,0,0],[-phi1 + math.atan2(-t1, -t13),-t2,-t3],[t4,-math.pi,0]])

print TempExpr
