import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

n_cloud = 200
n_clusters = 4
n_sample = 100

# np.random.seed(3)

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

"""use KMeans to identify seeds for sub-cluster selection"""
kmeans = KMeans(n_clusters=n_clusters).fit(rawdata)
centroids = kmeans.cluster_centers_


plt.scatter(rawdata[:, 0], rawdata[:, 1],
            marker='o', s=10,
            color='k', linewidths=0.0, edgecolors=None, alpha=.3)

plt.scatter(centroids[:, 0], centroids[:, 1],
            marker='x', s=50, linewidths=3,
            color='r', zorder=10, alpha=.7)
plt.title('title')

x_min, x_max = rawdata[:, 0].min() - 1, rawdata[:, 0].max() + 1
y_min, y_max = rawdata[:, 1].min() - 1, rawdata[:, 1].max() + 1
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)

plt.show()
