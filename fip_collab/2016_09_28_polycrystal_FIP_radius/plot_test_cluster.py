import numpy as np
import matplotlib.pyplot as plt

n_cloud = 30

np.random.seed(11)

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

plt.figure(1, figsize=[3, 3])
plt.plot(rawdata[:, 0], rawdata[:, 1],
         marker='o', markersize=7, color='b', linestyle='', alpha=0.7)
plt.xlabel('PC1', fontsize='large')
plt.ylabel('PC2', fontsize='large')
plt.margins(0.1)
plt.axis('equal')
plt.tight_layout()

plt.show()
