import numpy as np
import scipy.stats as ss
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from sklearn.cluster import KMeans


# np.random.seed(6)

"""initialize randomly distributed points in square"""
sl = 2  # side length of square
rawdata = sl*np.random.random((1000, 2))-np.array([[sl/2., sl/2.]])
n_pts = 150
n_sel = 100
dof = 2  # number of spatial dimensions
rawdata = rawdata[:n_pts, :]

"""plot intial points"""
fig = plt.figure()
plt.scatter(rawdata[:, 0], rawdata[:, 1],
            marker='o', s=20,
            color='k', linewidths=0.0, edgecolors=None, alpha=.3,
            label='original')


"""perform kmeans to identify seeds"""
kmeans = KMeans(n_clusters=n_sel).fit(rawdata)
seeds = kmeans.cluster_centers_

plt.scatter(seeds[:, 0], seeds[:, 1],
            marker='s', s=15,
            color='b', linewidths=0.0, edgecolors=None, alpha=.5,
            label='targets')


"""find the point closest to each seed"""
rawdata_ = rawdata
selected = np.zeros((n_sel, 2))

for ii in xrange(n_sel):
    dist = np.sum((rawdata_-seeds[ii, :])**2, 1)
    indx = np.argmin(dist)

    selected[ii, :] = rawdata_[indx, :]
    rawdata_ = np.delete(rawdata_, indx, axis=0)

    x = np.array([seeds[ii, 0], selected[ii, 0]])
    y = np.array([seeds[ii, 1], selected[ii, 1]])
    plt.plot(x, y, 'r:')


"""plot the selected points"""
plt.scatter(selected[:, 0], selected[:, 1],
            marker='x', s=40, c='r', edgecolors=None,
            linewidths=1.0, alpha=0.5,
            label='selected')


tgt = 0.5
plt.axis(tgt*np.array([-sl, sl, -sl, sl]))

plt.axes().set_aspect('equal')
plt.legend(loc='upper right', shadow=True, fontsize='medium', ncol=1)
fig.tight_layout()

plt.show()
