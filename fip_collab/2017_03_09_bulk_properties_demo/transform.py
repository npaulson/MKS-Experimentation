import h5py


def transform(C, ns, set_id, pca):

    n_corr = C['cmax']

    f_red = h5py.File("spatial_reduced_L%s.hdf5" % C['H'], 'a')
    f_stats = h5py.File("spatial_L%s.hdf5" % C['H'], 'r')

    ff = f_stats.get('ff_%s' % set_id)[...]
    ff = ff.reshape(ns, n_corr*C['vmax']**3)

    ff_red = pca.transform(ff)

    f_red.create_dataset('reduced_%s' % set_id,
                         data=ff_red,
                         dtype='float64')

    f_red.close()
    f_stats.close()


if __name__ == '__main__':
    ns = 10
    set_id = 'random'

    reduce(ns, set_id)
