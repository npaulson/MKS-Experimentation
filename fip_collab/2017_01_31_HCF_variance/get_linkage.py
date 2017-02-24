import numpy as np
import functions as rr
import reg_functions as rf
from constants import const
import h5py
import time
from sklearn.preprocessing import PolynomialFeatures


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
    loc_tot = np.zeros((ns_tot, C['n_pc_tot']), dtype='float64')
    var_tot = np.zeros((ns_tot, C['n_pc_tot']), dtype='float64')
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

        tmp = f_link.get('samp_%s' % sid)[...]

        loc_tot[c:c_, :] = np.mean(tmp, 1)
        var_tot[c:c_, :] = np.std(tmp, 1)

        c = c_

    f_link.close()

    return groups, response_tot, loc_tot, var_tot, iscal


def preanalysis(n_pc, deg, loc_tot, var_tot):

    poly = PolynomialFeatures(deg)
    tmpl = poly.fit_transform(loc_tot[:, :n_pc])
    tmpv = poly.fit_transform(var_tot[:, :n_pc])

    # """include variances"""
    # X = np.zeros((tmpl.shape[0], tmpl.shape[1]+1))
    # X[:, 0] = np.sum(var_tot, 1)
    # X[:, 1:] = tmpl

    """include standard deviations with polynomial order"""
    X = np.zeros((tmpl.shape[0], tmpl.shape[1]+tmpv.shape[1]))
    X[:, :tmpl.shape[1]] = tmpl
    X[:, tmpl.shape[1]:] = tmpv

    # """include standard deviations with linear dependence"""
    # X = np.zeros((tmpl.shape[0], tmpl.shape[1]+n_pc))
    # X[:, :tmpl.shape[1]] = tmpl
    # X[:, tmpl.shape[1]:] = var_tot[:, :n_pc]

    # """don't include variances"""
    # X = tmpl

    return X


def analysis(n_pc, deg, precursors):

    groups = precursors[0]
    response_tot = precursors[1]
    loc_tot = precursors[2]
    var_tot = precursors[3]
    iscal = precursors[4]

    X = preanalysis(n_pc, deg, loc_tot, var_tot)

    RpredCV = rf.cv(X[iscal, :], response_tot[iscal], groups[iscal])

    coef = rf.regression(X[iscal, :], response_tot[iscal])

    Rpred = rf.prediction(X, coef)

    return coef, RpredCV, Rpred


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

    """perform the regressions"""
    f_reg = h5py.File("regression_results_L%s.hdf5" % C['H'], 'a')

    f_reg.create_dataset('Rsim_%s' % par, data=response_tot)

    f_reg.create_dataset('iscal_%s' % par, data=iscal)

    Rpred_set = f_reg.create_dataset('Rpred_%s' % par,
                                     (C['pcdeg'].shape[0], ns_tot),
                                     dtype='float64')

    RpredCV_set = f_reg.create_dataset('RpredCV_%s' % par,
                                       (C['pcdeg'].shape[0],
                                        p*len(C['sid_cal'])),
                                       dtype='float64')

    # meanc = response_tot[iscal].mean()

    for ii in xrange(C['pcdeg'].shape[0]):

        n_pc = C['pcdeg'][ii, 0]
        deg = C['pcdeg'][ii, 1]

        coef, RpredCV, Rpred = analysis(n_pc, deg, precursors)

        RpredCV_set[ii, :] = RpredCV
        Rpred_set[ii, :] = Rpred

        msg = "[deg, #PCs]: " + str(deg) + ", " + str(n_pc) + " complete"
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
