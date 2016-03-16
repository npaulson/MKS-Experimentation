import functions as rr
import numpy as np
import time
import h5py


def auto(el, ns, set_id, step, wrt_file):

    st = time.time()

    f = h5py.File("D_%s%s_s%s.hdf5" % (ns, set_id, step), 'a')
    M = f.get('M')[...]

    FF_auto = (1./(el**3))*np.abs(M)**2
    ff_auto = np.fft.ifftn(FF_auto, [el, el, el], [2, 3, 4])

    f.create_dataset('ff_auto', data=ff_auto)
    f.close()

    msg = "autocorrelations computed: %ss" % np.round(time.time()-st, 5)
    rr.WP(msg, wrt_file)


if __name__ == '__main__':
    el = 21
    ns = 10
    set_id = 'random'
    step = 0
    wrt_file = 'test.txt'

    auto(el, ns, set_id, step, wrt_file)
