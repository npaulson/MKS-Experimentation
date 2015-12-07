import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


inc = 5
a = 0.005
b = 0.0085

n_th_max = 120/inc  # number of theta samples in FOS
n_max = 360/inc  # number of phi1, Phi and phi2 samples in FOS
n_hlf = 180/inc  # half n_max

n_th = (60/inc)+1  # number of theta samples for FZ
n_p1 = 360/inc  # number of phi1 samples for FZ
n_P = (90/inc)+1  # number of Phi samples for FZ
n_p2 = 60/inc  # number of phi2 samples for FZ
n_en = 10

pre_fft = np.load("pre_fft.npy")

print "FZ shape: %s" % str(np.array([n_th, n_p1, n_P, n_p2, 10]))
print "symmetric shape: %s" % str(pre_fft.shape)

# plot one of the variables while all other variables are held constant
fig = plt.figure(num=1, figsize=[10, 6])
ax = fig.add_subplot(111, projection='3d')

th_l = 7
th_u = 8
p1_l = 0
p1_u = n_p1
P_l = 0
P_u = n_P
p2_l = 6
p2_u = 7
en_l = 0
en_u = 1

X, Y = np.meshgrid(np.arange(p1_l, p1_u), np.arange(P_l, P_u))

Z = np.squeeze(pre_fft[th_l:th_u,
               p1_l:p1_u,
               P_l:P_u,
               p2_l:p2_u,
               en_l:en_u])

X = inc*X.T
Y = inc*Y.T

ax.plot_surface(X, Y, np.log(Z), rstride=1, cstride=1, color=(0.3, 0.4, 1.0))

msg = "theta=%s-%s, phi1=%s-%s, Phi=%s-%s, phi2=%s-%s" % \
     (th_l*inc, (th_u-1)*inc,
      p1_l*inc, (p1_u-1)*inc,
      P_l*inc, (P_u-1)*inc,
      p2_l*inc, (p2_u-1)*inc)
plt.title(msg)

print np.max(pre_fft)
print np.unravel_index(np.argmax(pre_fft), pre_fft.shape)

plt.show()
