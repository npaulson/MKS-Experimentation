import numpy as np
import matplotlib.pyplot as plt


pre_fft = np.load("pre_fft.npy")


# plot one of the variables while all other variables are held constant
plt.figure(num=1, figsize=[10, 6])


plt.plot(np.arange(0, 72), pre_fft[5, 15, 26, :, -1], 'r')
plt.plot(np.arange(0, 72), pre_fft[5, 15, 27, :, -1], 'g')
plt.plot(np.arange(0, 72), pre_fft[5, 15, 28, :, -1], 'b')


# sort the frequences by magnitude and plot

# fqsort = np.sort(pre_fft.reshape(pre_fft.size))

# plt.figure(num=2, figsize=[10, 6])

# plt.plot(np.arange(fqsort.size), fqsort)

print np.max(pre_fft)
print np.unravel_index(np.argmax(pre_fft), pre_fft.shape)

plt.show()
