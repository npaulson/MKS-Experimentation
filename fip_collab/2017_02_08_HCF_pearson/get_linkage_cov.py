import numpy as np
import functions as rr
import reg_functions as rf
from constants import const
from scipy.stats import pearsonr
import h5py
import time
from sklearn.preprocessing import PolynomialFeatures


def analysis(X, response_tot, groups, iscal):

    RpredCV = rf.cv(X[iscal, :], response_tot[iscal], groups[iscal])

    coef = rf.regression(X[iscal, :], response_tot[iscal])

    Rpred = rf.prediction(X, coef)

    return coef, RpredCV, Rpred


def pearson_eval(X, y):

    Nfeat = X.shape[1]
    pvec = np.zeros((Nfeat,))
    pvec[0] = 1  # for the constant term
    for ii in xrange(1, Nfeat):
        """ pearsonr returns tuples with the pearson correlation
        and the P-value (chance of observing the data
        if the null hypothesis is true). I'm going to throw away
        the p-value"""
        pvec[ii] = pearsonr(X[:, ii], y)[0]

    return pvec


def preanalysis(loc_tot, cov_tot):

    C = const()
    npc = loc_tot.shape[1]
    ns = loc_tot.shape[0]

    """extract names from mean loc info"""
    mean_only_names = []
    for ii in xrange(npc):
        mean_only_names += ['m%s' % str(ii+1)]

    """extract variance info from covariance matrix"""
    var_only = np.zeros((ns, npc))
    var_only_names = []
    for ii in xrange(npc):
        var_only[:, ii] = cov_tot[:, ii, ii]
        var_only_names += ['c%s_%s' % (str(ii+1), str(ii+1))]

    """extract unique, off-diagonal co-variance info from
    covariance matrix"""
    nc = (npc**2-npc)/2
    cov_only = np.zeros((ns, nc))
    cov_only_names = []
    c = 0
    for ii in xrange(npc):
        for jj in xrange(ii+1, npc):
            cov_only[:, c] = cov_tot[:, ii, jj]
            cov_only_names += ['c%s_%s' % (str(ii+1), str(jj+1))]
            c += 1

    """concatenate all the features into one array"""
    # X_pre = np.concatenate((loc_tot, var_only, cov_only), axis=1)
    X_pre = np.concatenate((loc_tot, var_only), axis=1)

    """get the polynomial features"""
    poly = PolynomialFeatures(C['deg_max'])
    poly.fit(X_pre)
    X = poly.transform(X_pre)

    """get the names of the polynomial features"""
    # names_pre = mean_only_names + var_only_names + cov_only_names
    names_pre = mean_only_names + var_only_names
    names = poly.get_feature_names(names_pre)

    return X, names


def prepare(par):

    np.random.seed(0)

    C = const()
    p = C['n_sc']

    f_link = h5py.File("sample_L%s.hdf5" % C['H'], 'r')

    """gather the calibration data"""

    n_tot = len(C['sid'])
    ns_tot = n_tot*p
    groups = np.zeros(ns_tot, dtype='int16')
    response_tot = np.zeros(ns_tot, dtype='float64')
    loc_tot = np.zeros((ns_tot, C['n_pc_max']), dtype='float64')
    cov_tot = np.zeros((ns_tot, C['n_pc_max'], C['n_pc_max']), dtype='float64')
    iscal = np.zeros((ns_tot,), dtype='bool')

    c = 0

    for ii in xrange(n_tot):
        c_ = c + p
        sid = C['sid'][ii]

        """flag elements of the calibration set"""
        if sid in C['sid_cal']:
            iscal[c:c_] = True

        groups[c:c_] = 2*ii+np.round(np.random.random((p,)))

        dset_name = "%s_%s" % (par, sid)
        response_tot[c:c_] = f_link.get(dset_name)[...]

        tmp = f_link.get('samp_%s' % sid)[:, :, :C['n_pc_max']]

        loc_tot[c:c_, :] = np.mean(tmp, 1)

        for jj in xrange(p):
            cov_tot[c+jj, ...] = np.cov(tmp[jj, ...], rowvar=False)

        c = c_

    f_link.close()

    return groups, response_tot, loc_tot, cov_tot, iscal


def linkage(par):

    st = time.time()

    C = const()
    p = C['n_sc']
    n_tot = len(C['sid'])
    ns_tot = n_tot*p

    """create arrays required for linkage creation"""
    precursors = prepare(par)
    groups = precursors[0]
    response_tot = precursors[1]
    loc_tot = precursors[2]
    var_tot = precursors[3]
    iscal = precursors[4]

    f_reg = h5py.File("regression_results_L%s.hdf5" % C['H'], 'a')

    f_reg.create_dataset('Rsim_%s' % par, data=response_tot)

    f_reg.create_dataset('iscal_%s' % par, data=iscal)

    coef_set = f_reg.create_dataset('coef_%s' % par,
                                    (C['fmax'], C['fmax']),
                                    dtype='float64')

    Rpred_set = f_reg.create_dataset('Rpred_%s' % par,
                                     (C['fmax'], ns_tot),
                                     dtype='float64')

    RpredCV_set = f_reg.create_dataset('RpredCV_%s' % par,
                                       (C['fmax'],
                                        p*len(C['sid_cal'])),
                                       dtype='float64')

    """get the polynomial features"""
    X, names = preanalysis(loc_tot, var_tot)
    f_reg.create_dataset('featurenames_%s' % par, data=names)

    """perform the pearson correlation"""
    pvec = pearson_eval(X[iscal, :], response_tot[iscal])
    f_reg.create_dataset('pearsonscores_%s' % par, data=pvec)

    """select the most highly correlated features"""
    indxv = np.argsort(np.abs(pvec))[::-1]
    indxv = indxv[:C['fmax']]
    f_reg.create_dataset('indxsel_%s' % par, data=indxv)
    Xp = X[:, indxv]

    # import matplotlib.pyplot as plt
    # plt.plot(np.arange(pvec.size), np.abs(pvec[np.argsort(np.abs(pvec))[::-1]]))
    # plt.show()

    print "top 10 scoring features"
    for ii in xrange(10):
        print "%s: %s" % (names[indxv[ii]], pvec[indxv[ii]])

    """create and evaluate the final linkages"""

    # meanc = response_tot[iscal].mean()

    for ii in xrange(C['fmax']):

        coef, RpredCV, Rpred = analysis(Xp[:, :(ii+1)], response_tot,
                                        groups, iscal)

        coef_set[ii, :] = 0
        coef_set[ii, :(ii+1)] = coef

        RpredCV_set[ii, :] = RpredCV
        Rpred_set[ii, :] = Rpred

        msg = "%s feature linkage complete" % str(ii+1)
        rr.WP(msg, C['wrt_file'])
        # print "cv.mean(): %s" % str(np.mean(np.abs(RpredCV -
        #                                            response_tot[iscal]))/meanc)

    f_reg.close()

    timeE = np.round(time.time()-st, 1)
    msg = "regressions and cross-validations completed: %s s" % timeE
    rr.WP(msg, C['wrt_file'])


if __name__ == '__main__':
    par = 'mu'
    linkage(par)
