import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import PCA
# import matplotlib.cm as cm

n_pts = 100
n_pts_hlf = np.floor(n_pts/2.)

rawdata_ = np.zeros((n_pts, 3))
rawdata_[:, 0] = np.random.normal(loc=0,
                                  scale=.25,
                                  size=n_pts)
rawdata_[:, 1] = np.random.normal(loc=0,
                                  scale=.5,
                                  size=n_pts)
rawdata_[:, 2] = np.random.normal(loc=0,
                                  scale=2,
                                  size=n_pts)


fig = plt.figure(1)
ax = fig.add_subplot(111, projection='3d')

ax.scatter(rawdata_[:, 0], rawdata_[:, 1], rawdata_[:, 2],
           c='b', marker='o', s=40, alpha=.3)

X = rawdata_[:, 0]
Y = rawdata_[:, 1]
Z = rawdata_[:, 2]
max_range = np.array([X.max()-X.min(), Y.max()-Y.min(), Z.max()-Z.min()]).max()
Xb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(X.max()+X.min())
Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(Y.max()+Y.min())
Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(Z.max()+Z.min())
# Comment or uncomment following both lines to test the fake bounding box:
for xb, yb, zb in zip(Xb, Yb, Zb):
   ax.plot([xb], [yb], [zb], 'w')

"""rotate the cluster"""
ang = 2*np.pi*.1
rmat = np.array([[np.cos(ang), -np.sin(ang), 0],
                 [np.sin(ang), np.cos(ang), 0],
                 [0, 0, 1]])
tmp = np.einsum('ij,jk', rawdata_, rmat)

ang = 2*np.pi*0.05
rmat = np.array([[np.cos(ang), 0, -np.sin(ang)],
                 [0, 1, 0],
                 [np.sin(ang),0, np.cos(ang)]])
rawdata = np.einsum('ij,jk', tmp, rmat)

"""plot the cluster"""

fig = plt.figure(2, figsize=[5,4])
ax = fig.add_subplot(111, projection='3d')

ax.scatter(rawdata[:, 0], rawdata[:, 1], rawdata[:, 2],
           c='b', marker='o', s=40, alpha=.3)

X = rawdata[:, 0]
Y = rawdata[:, 1]
Z = rawdata[:, 2]
max_range = np.array([X.max()-X.min(), Y.max()-Y.min(), Z.max()-Z.min()]).max()
Xb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(X.max()+X.min())
Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(Y.max()+Y.min())
Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(Z.max()+Z.min())
# Comment or uncomment following both lines to test the fake bounding box:
for xb, yb, zb in zip(Xb, Yb, Zb):
   ax.plot([xb], [yb], [zb], 'w')

ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
fig.tight_layout()

"""Isolate the cluster and perform PCA"""
pca = PCA(n_components=3)
pca.fit(rawdata)
data = pca.transform(rawdata)

"""plot the cluster"""
fig = plt.figure(3)
ax = fig.add_subplot(111, projection='3d')

ax.scatter(data[:, 0], data[:, 1], data[:, 2],
           c='b', marker='o', s=40, alpha=.3)

X = data[:, 0]
Y = data[:, 1]
Z = data[:, 2]
max_range = np.array([X.max()-X.min(), Y.max()-Y.min(), Z.max()-Z.min()]).max()
Xb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(X.max()+X.min())
Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(Y.max()+Y.min())
Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(Z.max()+Z.min())
# Comment or uncomment following both lines to test the fake bounding box:
for xb, yb, zb in zip(Xb, Yb, Zb):
   ax.plot([xb], [yb], [zb], 'w')

ax.set_xlabel('PC1 axis')
ax.set_ylabel('PC2 axis')
ax.set_zlabel('PC3 axis')


fig = plt.figure(4, figsize=[5,4])

plt.plot(data[:, 0], data[:, 1],
         marker='o', markersize=8, color='b',
         linestyle='', alpha=.3)

plt.xlabel('PC1 axis')
plt.ylabel('PC2 axis')

plt.margins(.05)
plt.axis('equal')
fig.tight_layout()

plt.show()
