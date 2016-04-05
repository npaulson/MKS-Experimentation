import numpy as np
import functions as rr
import vtk_read as read
import h5py


def modulus(el, ns, set_id, step, newdir, wrt_file):

    """
    The tensorID determines the type of tensor data read from the .vtk file
    if tensorID == 0, we read the stress tensor
    if tensorID == 1, we read the strain tensor
    if tensorID == 2, we read the plastic strain tensor

    compd = {'11': 0, '22': 4, '33': 8, '12': 1, '13': 6, '23': 5}
    """
    comp = '11'

    # get the stress tensors
    tensor_id = 0
    read.read_meas(el, ns, set_id, step, comp, tensor_id, newdir, wrt_file)
    # get the strain tensors
    tensor_id = 1
    read.read_meas(el, ns, set_id, step, comp, tensor_id, newdir, wrt_file)

    """get the mean stresses and strains (11 component) for each SVE"""

    typ = ['sigma', 'epsilon_t', 'epsilon_p']

    f = h5py.File("responses.hdf5", 'a')

    print '%s_%s' % (typ[0], set_id)
    sig = f.get('%s_%s' % (typ[0], set_id))[...]
    sig_mean = np.mean(sig, axis=(1, 2, 3))

    print '%s_%s' % (typ[1], set_id)
    eps = f.get('%s_%s' % (typ[1], set_id))[...]
    eps_mean = np.mean(eps, axis=(1, 2, 3))

    f.close()

    """calculate the effective modulus for a particular component"""

    Eeff = sig_mean/eps_mean

    msg = 'Eeff set: %s' % str(Eeff)
    rr.WP(msg, wrt_file)

    f = h5py.File("linkage.hdf5", 'a')
    f.create_dataset('Eeff_%s' % set_id, data=Eeff)
    f.close()


if __name__ == '__main__':
    el = 21
    ns = 10
    set_id = 'transverseD3D'
    step = 1
    newdir = 'transverseD3D'
    wrt_file = 'test.txt'

    modulus(el, ns, set_id, step, newdir, wrt_file)
