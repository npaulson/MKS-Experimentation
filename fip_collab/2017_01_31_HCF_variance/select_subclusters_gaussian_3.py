import numpy as np
import matplotlib.pyplot as plt


def neg1to1():
    return 2*np.random.random((1,))-1


n_cloud = 200
n_tgt = 100

"""generate the original point cloud"""
original = np.zeros((n_cloud, 2))
original[:, 0] = np.random.normal(loc=0,
                                  scale=3,
                                  size=n_cloud)
original[:, 1] = np.random.normal(loc=0,
                                  scale=1,
                                  size=n_cloud)

sigPC1 = original[:, 0].std()
sigPC2 = original[:, 1].std()
muPC1 = original[:, 0].mean()
muPC2 = original[:, 1].mean()

print "original std, PC1: " + str(sigPC1)
print "original std, PC2: " + str(sigPC2)

plt.scatter(original[:, 0], original[:, 1],
            marker='o', s=20,
            color='k', linewidths=0.0, edgecolors=None, alpha=.3)

"""randomly select a secondary point cloud"""
muPC1_ = muPC1 + sigPC1*neg1to1()
muPC2_ = muPC2 + sigPC2*neg1to1()
sigPC1_ = 0.5*sigPC1 + 0.5*np.random.rand()*(sigPC1-np.abs(muPC1-muPC1_))
sigPC2_ = 0.5*sigPC2 + 0.5*np.random.rand()*(sigPC2-np.abs(muPC2-muPC2_))

print muPC1_
print sigPC1_

"""generate the new point cloud"""
target = np.zeros((n_tgt, 2))
target[:, 0] = np.random.normal(loc=muPC1_,
                                scale=sigPC1_,
                                size=n_tgt)
target[:, 1] = np.random.normal(loc=muPC2_,
                                scale=sigPC2_,
                                size=n_tgt)

# plt.scatter(target[:, 0], target[:, 1],
#             marker='s', s=15,
#             color='b', linewidths=0.0, edgecolors=None, alpha=.5)


"""identify closest original points to each target point
each time an original point is selected remove it from the pool so
that points are not double counted. Randomly selelect target points
so that there is no bias."""

newpts = np.zeros((n_tgt, 2))
original_ = original

for ii in xrange(n_tgt):
    dist = np.sum((original_-target[ii, :])**2, 1)
    indx = np.argmin(dist)
    newpts[ii, :] = original_[indx, :]
    original_ = np.delete(original_, indx, axis=0)

    x = np.array([target[ii, 0], newpts[ii, 0]])
    y = np.array([target[ii, 1], newpts[ii, 1]])
    # plt.plot(x, y, 'r:')

plt.scatter(newpts[:, 0], newpts[:, 1],
            marker='x', s=40, c='r', edgecolors=None,
            linewidths=1.0, alpha=0.5,
            label='selected')

print "covariance of target points:"
print np.cov(target, rowvar=False)
print "covariance of selected points:"
print np.cov(newpts, rowvar=False)

x_min, x_max = original[:, 0].min() - 1, original[:, 0].max() + 1
y_min, y_max = original[:, 1].min() - 1, original[:, 1].max() + 1
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)

plt.axes().set_aspect('equal')
plt.tight_layout()

plt.show()
