import numpy as np
import h5py


def fip_sort(el, ns, set_id, step, parID):

    f = h5py.File("fip_%s%s_s%s.hdf5" % (ns, set_id, step), 'r')
    fip = f.get('%sb' % parID)[...]
    f.close()

    maxfip = np.sort(np.max(fip, 1))

    f = h5py.File("pltout.hdf5", 'a')
    f.create_dataset('max%s_%s' % (parID, set_id), data=maxfip)
    f.close()

if __name__ == '__main__':
    el = 21
    ns = 100
    set_id = 'val'
    step = 5
    parID = 'fip'

    fip_sort(el, ns, set_id, step, parID)
