import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm


"""initialize randomly distributed points in square"""
rawdata = np.random.random((500, 2))-np.array([[.5, .5]])

"""plot intial points"""
plt.figure()
plt.scatter(rawdata[:, 0], rawdata[:, 1],
            s=40, c='k', edgecolors=None,
            linewidths=0.0, alpha=0.25)

"""identify all points within a selected area"""
sc = 1

regions = np.array([[-.3, -.1, .1, .3, 2*sc],
                    [-.1, .1, .1, .3, 5*sc],
                    [.1, .3, .1, .3, 2*sc],
                    [-.3, -.1, -.1, .1, 5*sc],
                    [-.1, .1, -.1, .1, 20*sc],
                    [.1, .3, -.1, .1, 5*sc],
                    [-.3, -.1, -.3, -.1, 2*sc],
                    [-.1, .1, -.3, -.1, 5*sc],
                    [.1, .3, -.3, -.1, 2*sc]])

tmp = np.linspace(0, 1, regions.shape[0])
np.random.shuffle(tmp)
colormat = cm.rainbow(tmp)

for ii in xrange(regions.shape[0]):

    tmpLX = rawdata[:, 0] > regions[ii, 0]
    tmpUX = rawdata[:, 0] < regions[ii, 1]
    tmpLY = rawdata[:, 1] > regions[ii, 2]
    tmpUY = rawdata[:, 1] < regions[ii, 3]
    tmpSET = tmpLX*tmpUX*tmpLY*tmpUY

    dataSS = rawdata[tmpSET, :]  # selected subset of rawdata

    plt.scatter(dataSS[:, 0], dataSS[:, 1],
                s=40, c=colormat[ii, :], edgecolors=None,
                linewidths=0.0, alpha=0.5)

    indx = np.zeros((dataSS.shape[0],), dtype=bool)
    indx[:np.int16(regions[ii, 4])] = True
    np.random.shuffle(indx)

    dataSSR = dataSS[indx, :]  # randomly selected Npnts in dataSS

    plt.scatter(dataSSR[:, 0], dataSSR[:, 1],
                marker='o', s=60, c='', edgecolors='k',
                linewidths=1.5, alpha=1.0)

plt.show()
