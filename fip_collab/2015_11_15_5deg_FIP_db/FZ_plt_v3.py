import numpy as np
import euler_func as ef
import matplotlib.pyplot as plt


# load the symmetry operators for hexagonal crystal symmetry
symhex = ef.symhex()

# n_FZ: total number of sampled orientations in FZ
n_FZ = 1

# FZ_euler: array of euler angles of sampled orientations in FZ
# FZ_euler = np.hstack([360.*np.random.rand(n_FZ, 1),
#                       90.*np.pi*np.random.rand(n_FZ, 1),
#                       60.*np.pi*np.random.rand(n_FZ, 1)])

FZ_euler = np.array([[0, 0, 160]])
FZ_euler = np.round(FZ_euler, -1)*(np.pi/180.)

# g: array of orientation matrices (sample to crystal frame rotation
# matrices) for orientations in fundamental zone
g = ef.bunge2g(FZ_euler[:, 0],
               FZ_euler[:, 1],
               FZ_euler[:, 2])
# FZ_euler_sym: array of euler angles of sampled orientations in
# FZ and their symmetric equivalents
FZ_euler_sym = np.zeros((12, n_FZ, 3))

print FZ_euler_sym.shape

# find the symmetric equivalents to the euler angle within the FZ
for sym in xrange(12):
    op = symhex[sym, ...]  # symmetry operator
    g_sym = np.einsum('ik,...kj', op, g)  # perform tensor product

    print g_sym

    # convert back to euler angles
    tmp = np.array(ef.g2bunge(g_sym)).transpose()

    FZ_euler_sym[sym, ...] = tmp

for sym in xrange(12):
    print FZ_euler_sym[sym, ...]*(180./np.pi)
print "\n"

for ii in xrange(3):
    ltz = FZ_euler_sym[..., ii] < 0.0
    FZ_euler_sym[..., ii] += 2*np.pi*ltz

FZ_euler_sym = FZ_euler_sym*(180./np.pi)

# plot the symmetric orientations in euler space

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

for ii in xrange(n_FZ):

    plt.figure(1)
    plt.plot(FZ_euler_sym[0, ii, 0], FZ_euler_sym[0, ii, 1],
             c=color[ii], marker='s', linestyle='none')
    plt.figure(2)
    plt.plot(FZ_euler_sym[0, ii, 1], FZ_euler_sym[0, ii, 2],
             c=color[ii], marker='s', linestyle='none')

    plt.figure(1)
    plt.plot(FZ_euler_sym[1:, ii, 0], FZ_euler_sym[1:, ii, 1],
             c=color[ii], marker='o', linestyle='none')
    plt.figure(2)
    plt.plot(FZ_euler_sym[1:, ii, 1], FZ_euler_sym[1:, ii, 2],
             c=color[ii], marker='o', linestyle='none')

plt.show()
