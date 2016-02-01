import h5py
import numpy as np
import matplotlib.pyplot as plt


f = h5py.File('var_extract_total.hdf5', 'r')
data = f.get('var_set')[...].real

theta_U = np.unique(data[:, 0])
print "unique theta: %s" % str(theta_U)
phi1_U = np.unique(data[:, 1])
print "unique phi1: %s" % str(phi1_U)
Phi_U = np.unique(data[:, 2])
print "unique Phi: %s" % str(Phi_U)
phi2_U = np.unique(data[:, 3])
print "unique phi2: %s" % str(phi2_U)
en_U = np.unique(data[:, 4])
print "unique en: %s" % str(en_U)

# th = theta_U[np.int64(np.random.rand()*theta_U.size)]
phi1 = phi1_U[np.int64(np.random.rand()*phi1_U.size)]
Phi = Phi_U[np.int64(np.random.rand()*Phi_U.size)]
phi2 = phi2_U[np.int64(np.random.rand()*phi2_U.size)]
en = en_U[-2]
# en = en_U[np.int64(np.random.rand()*en_U.size)]


ang_sel = (data[:, 1] == phi1) * \
    (data[:, 2] == Phi) * \
    (data[:, 3] == phi2) * \
    (data[:, 4] == en)

plt.plot(data[ang_sel, 0], data[ang_sel, 5], 'bx')
plt.title('phi1 = %s, Phi = %s, phi2 = %s, en = %s' %
          (phi1, Phi, phi2, en))
plt.xlabel('theta')
plt.ylabel('FIP')

plt.show()

