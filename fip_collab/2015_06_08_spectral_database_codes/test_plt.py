import numpy as np
import matplotlib.pyplot as plt


pre_fft = np.load("pre_fft.npy")

plt.plot(np.arange(0, 72), pre_fft[:, 30, 30, 30, -1])

plt.show()
