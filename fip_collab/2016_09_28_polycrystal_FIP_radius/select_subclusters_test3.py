import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

n_cloud = 200
n_clusters = 10
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

"""use KMeans to identify clusters"""
kmeans = KMeans(n_clusters=n_clusters).fit(rawdata)

# Step size of the mesh. Decrease to increase the quality of the VQ.
h = .02     # point in the mesh [x_min, x_max]x[y_min, y_max].

# Plot the decision boundary. For that, we will assign a color to each
x_min, x_max = rawdata[:, 0].min() - 1, rawdata[:, 0].max() + 1
y_min, y_max = rawdata[:, 1].min() - 1, rawdata[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

# Obtain labels for each point in mesh. Use last trained model.
Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

# Put the result into a color plot
Z = Z.reshape(xx.shape)
plt.figure(1)
plt.clf()
plt.imshow(Z, interpolation='nearest',
           extent=(xx.min(), xx.max(), yy.min(), yy.max()),
           cmap=plt.cm.Paired,
           aspect='auto', origin='lower')

plt.plot(rawdata[:, 0], rawdata[:, 1], 'k.', markersize=2)
# Plot the centroids as a white X
centroids = kmeans.cluster_centers_
plt.scatter(centroids[:, 0], centroids[:, 1],
            marker='x', s=169, linewidths=3,
            color='w', zorder=10)
plt.title('K-means clustering \n'
          'Centroids are marked with white cross')
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.xticks(())
plt.yticks(())

plt.show()

"""find the subsamples for each seed"""
"""plot the cloud"""
fig, ax = plt.subplots()
plt.plot(rawdata[:, 0], rawdata[:, 1],
         marker='o', markersize=5, color='none',
         markeredgecolor='k', linestyle='')

"""create set of unmarked points"""
unmarked = rawdata

for ii in xrange(n_clusters):

    """idenfify closest n_cluster points to seed"""
    dist2seed = np.sqrt(np.sum((rawdata - centroids[ii, :])**2, 1))
    sort_inx = np.argsort(dist2seed)
    filler = rawdata[sort_inx[:n_sample], :]

    """identify radius"""
    radius = dist2seed[sort_inx[n_sample-1]]

    """plot the seed"""
    plt.plot(centroids[ii, 0], centroids[ii, 1],
             marker='o', markersize=8, color='r',
             linestyle='')

    circ = plt.Circle(centroids[ii, :], radius, color='k', fill=False)
    ax.add_artist(circ)

plt.margins(.05)
plt.axis('equal')

plt.show()
