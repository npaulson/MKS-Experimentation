import numpy as np
import matplotlib.pyplot as plt


"""initialize randomly distributed points in square"""
rawdata = np.random.random((500, 2))-np.array([[.5, .5]])

"""plot intial points"""
plt.figure()
plt.scatter(rawdata[:, 0], rawdata[:, 1],
            s=40, c='k', edgecolors=None,
            linewidths=0.0, alpha=0.25)

"""identify all points within a selected area"""
tmpLX = rawdata[:, 0] > -0.25
tmpUX = rawdata[:, 0] < 0.25
tmpLY = rawdata[:, 1] > -0.25
tmpUY = rawdata[:, 1] < 0.25
tmpSET = tmpLX*tmpUX*tmpLY*tmpUY

dataSS = rawdata[tmpSET, :]  # selected subset of rawdata

plt.scatter(dataSS[:, 0], dataSS[:, 1],
            s=40, c='r', edgecolors=None,
            linewidths=0.0, alpha=0.25)

"""identify a desired number of points within selected area"""
Npnts = 10

indx = np.zeros((dataSS.shape[0],), dtype=bool)
indx[:Npnts] = True
np.random.shuffle(indx)

dataSSR = dataSS[indx, :]  # randomly selected Npnts in dataSS

plt.scatter(dataSSR[:, 0], dataSSR[:, 1],
            marker='x', s=80, c='b', edgecolors=None,
            linewidths=4.0, alpha=0.5)

plt.show()
