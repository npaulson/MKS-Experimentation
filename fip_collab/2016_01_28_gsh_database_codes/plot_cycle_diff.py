import matplotlib.pyplot as plt
import numpy as np
import h5py

en_vec = np.array([0.0050, 0.0055, 0.0060, 0.0065, 0.0070, 0.0075, 0.0080])
cvec = np.array(['r', 'g', 'b', 'k', 'y', 'm', 'c'])

for ii in xrange(en_vec.size):

    f = h5py.File('slice_%s.hdf5' % str(ii).zfill(2), 'r')
    diffvec = f.get('diffvec')[...]
    f.close()

    fig = plt.figure(num=ii, figsize=[10, 7])

    plt.plot(np.arange(1, diffvec.size + 1), diffvec, 'bx-')
    plt.title('FIP evolution versus number of cycles, en = %s' % en_vec[ii])
    plt.xlabel('cycle number, n')
    plt.ylabel('$mean(| {FIP}_n-{FIP}_{n-1}|/{FIP}_n)$')

    # plt.savefig('fip_evolution_en_%s.png' % en_vec[ii])

    fig = plt.figure(num=en_vec.size+1, figsize=[10, 7])
    plt.plot(np.arange(1, diffvec.size + 1),
             diffvec,
             marker='x',
             ls='-',
             color=cvec[ii],
             label=en_vec[ii])

fig = plt.figure(num=en_vec.size+1, figsize=[10, 7])
plt.title('FIP evolution versus number of cycles, en = %s' % en_vec[ii])
plt.xlabel('cycle number, n')
plt.ylabel('$mean(| {FIP}_n-{FIP}_{n-1}|/{FIP}_n)$')
plt.legend(loc='upper center', shadow=True)

plt.show()
