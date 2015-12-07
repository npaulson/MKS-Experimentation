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
plt.figure(num=1, figsize=[10, 6])


for ii in xrange(n_th):

    plt.plot(np.arange(0, n_p1), pre_fft[ii, :n_p1, 10, 6, -1], 'r')

# sort the frequences by magnitude and plot

# fqsort = np.sort(pre_fft.reshape(pre_fft.size))

# plt.figure(num=2, figsize=[10, 6])

# plt.plot(np.arange(fqsort.size), fqsort)

print np.max(pre_fft)
print np.unravel_index(np.argmax(pre_fft), pre_fft.shape)

plt.show()
