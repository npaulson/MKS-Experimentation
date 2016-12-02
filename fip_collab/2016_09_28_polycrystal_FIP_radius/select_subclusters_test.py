import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

n_pts = 200
radius = 1.5

"""create a large random colormap"""
tmp = np.linspace(0, 1, n_pts)
np.random.shuffle(tmp)
colormat = cm.rainbow(tmp)

"""generate the raw cloud"""
rawdata_ = np.zeros((n_pts, 2))
rawdata_[:, 0] = np.random.normal(loc=0,
                                  scale=.2+np.random.rand(),
                                  size=n_pts)
rawdata_[:, 1] = np.random.normal(loc=0,
                                  scale=1.2+np.random.rand(),
                                  size=n_pts)

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

ii = 0
while unmarked.size > 0:

    """find the closest unmarked point to the center"""
    dist2center = np.sqrt(np.sum((unmarked - center)**2, 1))
    seed_inx = np.argmin(dist2center)
    seed = unmarked[seed_inx, :]

    """remove the seed from the set of unmarked points"""
    unmarked = np.delete(unmarked, seed_inx, 0)

    """idenfify points within radius of current seed"""
    dist2seed = np.sqrt(np.sum((unmarked - seed)**2, 1))
    tmp = dist2seed < radius
    filler_inx = np.arange(unmarked.shape[0])[tmp]
    filler = unmarked[filler_inx, :]

    """remove the filler points from the set of unmarked points"""
    unmarked = np.delete(unmarked, filler_inx, 0)

    """plot the filler points"""
    plt.plot(filler[:, 0], filler[:, 1],
             marker='o', markersize=5, color=colormat[ii, :],
             alpha=.7, linestyle='')

    """plot the seed"""
    plt.plot(seed[0], seed[1],
             marker='o', markersize=5, color='r',
             linestyle='')

    circ = plt.Circle(seed, radius, color='k', fill=False)
    ax.add_artist(circ)

    ii += 1

plt.margins(.05)
plt.axis('equal')

plt.show()
