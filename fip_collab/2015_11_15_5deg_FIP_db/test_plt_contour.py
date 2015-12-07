import numpy as np
import matplotlib.pyplot as plt


inc = 5

n_th_max = 120/inc  # number of theta samples in FOS
n_max = 360/inc  # number of phi1, Phi and phi2 samples in FOS
n_hlf = 180/inc  # half n_max

n_th = (60/inc)+1  # number of theta samples for FZ
n_p1 = 360/inc  # number of phi1 samples for FZ
n_P = (90/inc)+1  # number of Phi samples for FZ
n_p2 = 60/inc  # number of phi2 samples for FZ

pre_fft = np.load("pre_fft.npy")

print "FZ shape: %s" % str(np.array([n_th, n_p1, n_P, n_p2, 10]))
print "symmetric shape: %s" % str(pre_fft.shape)

# plot one of the variables while all other variables are held constant
fig = plt.figure(num=1, figsize=[10, 6])

th_l = 0
th_u = n_th
p1_l = 0
p1_u = n_p1
P_l = 19
P_u = 20
p2_l = 6
p2_u = 7

X, Y = np.meshgrid(np.arange(th_l, th_u), np.arange(p1_l, p1_u))

Z = pre_fft[th_l:th_u,
            p1_l:p1_u,
            P_l:P_u,
            p2_l:p2_u, -1]
Z = np.squeeze(Z)

X = inc*X.T
Y = inc*Y.T

CS = plt.contour(X, Y, Z, linewidths=2)
# plt.clabel(CS, inline=1, fontsize=10)
# CB = plt.colorbar(CS, shrink=0.8, extend='both')
CB = plt.colorbar(CS)

msg = "angular ranges: theta=%s-%s, phi1=%s-%s, Phi=%s-%s, phi2=%s-%s" % \
     (th_l*inc, (th_u-1)*inc,
      p1_l*inc, (p1_u-1)*inc,
      P_l*inc, (P_u-1)*inc,
      p2_l*inc, (p2_u-1)*inc)
plt.title(msg)

# sort the frequences by magnitude and plot
# fqsort = np.sort(pre_fft.reshape(pre_fft.size))
# plt.figure(num=2, figsize=[10, 6])
# plt.plot(np.arange(fqsort.size), fqsort)

print np.max(pre_fft)
print np.unravel_index(np.argmax(pre_fft), pre_fft.shape)

plt.show()
