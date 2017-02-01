import numpy as np
from sklearn.decomposition import PCA
import time


def new_space(ff):

    st = time.time()
    ns = ff.shape[0]
    el = ff.shape[1]

    ff_ = ff.reshape([ns, el**2])

    pca = PCA(n_components=el**2-1)
    pca.fit(ff_)
    reduced = pca.transform(ff_)
    ratios = 100*pca.explained_variance_ratio_
    ratios = np.round(ratios, 1)

    print "PCA completed: %ss" % np.round(time.time()-st, 5)

    return pca, reduced, ratios


if __name__ == '__main__':
    ns_set = [10, 10, 10]
    set_id_set = ['random', 'transverse', 'basaltrans']

    reduce(ns_set, set_id_set)
