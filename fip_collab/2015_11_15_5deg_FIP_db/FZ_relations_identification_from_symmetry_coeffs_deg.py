import numpy as np
import euler_func as ef
import matplotlib.pyplot as plt

symhex = ef.symhex()

plt.figure(1)

plt.plot(np.array([0, 360, 360, 0, 0]), np.array([0, 0, 180, 180, 0]), 'k-')
plt.plot(np.array([0, 360]), np.array([90, 90]), 'k-')

plt.xlabel('$\phi_1$')
plt.ylabel('$\Phi$')

sc = 1.05

plt.axis([-(sc-1)*360, sc*360, -(sc-1)*180, sc*180])

plt.figure(2)

plt.plot(np.array([0, 180, 180, 0, 0]), np.array([0, 0, 360, 360, 0]), 'k-')
plt.plot(np.array([90, 90]), np.array([0, 360]), 'k-')
plt.plot(np.array([0, 180]), np.array([60, 60]), 'k-')
plt.plot(np.array([0, 180]), np.array([120, 120]), 'k-')
plt.plot(np.array([0, 180]), np.array([180, 180]), 'k-')
plt.plot(np.array([0, 180]), np.array([240, 240]), 'k-')
plt.plot(np.array([0, 180]), np.array([300, 300]), 'k-')


plt.xlabel('$\Phi$')
plt.ylabel('$\phi2$')

sc = 1.05

plt.axis([-(sc-1)*180, sc*180, -(sc-1)*360, sc*360])

color = ['b', 'g', 'r', 'c']

for jj in xrange(4):

    randloc = np.array([2*np.pi*np.random.rand(),
                        0.5*np.pi*np.random.rand(),
                        (1./3.)*np.pi*np.random.rand()])
    g = ef.bunge2g(randloc[0], randloc[1], randloc[2])

    tmp = np.zeros([12, 3])

    for ii in xrange(12):
        g_sym = np.dot(symhex[:, :, ii], g)
        tmp[ii, :] = ef.g2bunge(g_sym)

    euler = np.zeros([12, 3])

    euler[:, 0] = tmp[:, 0]
    ltz = euler[:, 0] < 0
    euler[:, 0] = euler[:, 0] + 2*np.pi*ltz

    euler[:, 1] = tmp[:, 1]
    ltz = euler[:, 1] < 0
    euler[:, 1] = euler[:, 1] + 2*np.pi*ltz

    euler[:, 2] = tmp[:, 2]
    ltz = euler[:, 2] < 0
    euler[:, 2] = euler[:, 2] + 2*np.pi*ltz

    eulerdeg = euler * (180./np.pi)

    plt.figure(1)
    plt.plot(euler[:, 0], euler[:, 1], c=color[jj], marker='o')
    plt.figure(2)
    plt.plot(euler[:, 1], euler[:, 2], c=color[jj], marker='o')

plt.show()
