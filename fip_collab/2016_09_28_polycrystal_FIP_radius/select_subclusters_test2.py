import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

n_cloud = 200
n_sample = 100

np.random.seed(3)

"""generate the raw cloud"""
rawdata_ = np.zeros((n_cloud, 2))
rawdata_[:, 0] = np.random.normal(loc=0,
                                  scale=.2+np.random.rand(),
                                  size=n_cloud)
rawdata_[:, 1] = np.random.normal(loc=0,
                                  scale=1.2+np.random.rand(),
                                  size=n_cloud)

"""rotate the cloud"""
ang = 2*np.pi*np.random.rand()
rmat = np.array([[np.cos(ang), -np.sin(ang)],
                 [np.sin(ang), np.cos(ang)]])

rawdata = np.einsum('ij,jk', rawdata_, rmat)

"""plot the cloud"""
fig, ax = plt.subplots()
plt.plot(rawdata[:, 0], rawdata[:, 1],
         marker='o', markersize=5, color='none',
         markeredgecolor='k', linestyle='')

"""identify center of original point cloud"""
center = np.mean(rawdata, 0)

"""create set of unmarked points"""
unmarked = rawdata

"""create a large random colormap"""
tmp = np.linspace(0, 0.75, n_cloud)
np.random.shuffle(tmp)
colormat = cm.rainbow(tmp)

ii = 0
while unmarked.size > 0:

    """find the closest unmarked point to the center"""
    dist2center = np.sqrt(np.sum((unmarked - center)**2, 1))
    seed_inx = np.argmin(dist2center)
    seed = unmarked[seed_inx, :]

    """remove the seed from the set of unmarked points"""
    unmarked = np.delete(unmarked, seed_inx, 0)

    """idenfify closest n_cluster points to seed"""
    dist2seed = np.sqrt(np.sum((rawdata - seed)**2, 1))
    sort_inx = np.argsort(dist2seed)
    filler = rawdata[sort_inx[:n_sample], :]

    """identify radius"""
    radius = dist2seed[sort_inx[n_sample-1]]

    """remove newly marked points from the set of unmarked points"""
    dist2seed = np.sqrt(np.sum((unmarked - seed)**2, 1))
    tmp = dist2seed <= 0.75*radius
    remove_inx = np.arange(unmarked.shape[0])[tmp]
    unmarked = np.delete(unmarked, remove_inx, 0)

    """plot the filler points"""
    plt.plot(filler[:, 0], filler[:, 1],
             marker='o', markersize=5, color=colormat[ii, :],
             alpha=.5, linestyle='')

    """plot the seed"""
    plt.plot(seed[0], seed[1],
             marker='o', markersize=8, color='r',
             linestyle='')

    circ = plt.Circle(seed, radius, color='k', fill=False)
    ax.add_artist(circ)

    ii += 1

plt.margins(.05)
plt.axis('equal')

plt.show()
