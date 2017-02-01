import numpy as np
import time
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_predict
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline


def linkage(red_c, red_v, cvec, y_c, y_v, n_pc_max, n_poly_max):

    st = time.time()

    np.random.seed(0)

    ns_c = y_c.size
    ns_v = y_v.size

    """perform the regressions"""

    Rpred_c_T = np.zeros((n_pc_max*n_poly_max, ns_c))
    Rpred_cv_T = np.zeros((n_pc_max*n_poly_max, ns_c))
    Rpred_v_T = np.zeros((n_pc_max*n_poly_max, ns_v))
    order = np.zeros((n_pc_max*n_poly_max, 2))

    c = 0
    for ii in xrange(n_pc_max):
        for jj in xrange(n_poly_max):
            n_pc = ii+1
            deg = jj+1

            order[c, 0] = n_pc
            order[c, 1] = deg

            # when alpha=0 Ridge becomes standard linear regression
            model = Ridge(alpha=0)
            poly = PolynomialFeatures(deg)
            red_c_ = poly.fit_transform(red_c[:, :n_pc])
            red_v_ = poly.fit_transform(red_v[:, :n_pc])

            Rpred_cv = cross_val_predict(model, red_c_,
                                         y_c, cv=10)

            Rpred_cv_T[c, :] = Rpred_cv

            # Rpred_cv_alt = cross_val_predict(model, red_c_,
            #                                  y_c, groups=cvec, cv=10)
            # meanc = y_c.mean()
            # print "number of PCs: %s" % n_pc
            # print "degree of polynomial: %s" % deg
            # print "cv.mean(): %s" % str(np.mean(np.abs(Rpred_cv - y_c))/meanc)
            # print "cv.mean() alt: %s" % str(np.mean(np.abs(Rpred_cv_alt - y_c))/meanc)

            model.fit(red_c_, y_c)
            Rpred_c_T[c, :] = model.predict(red_c_)
            Rpred_v_T[c, :] = model.predict(red_v_)

            c += 1

    timeE = np.round(time.time()-st, 1)
    print "regressions and cross-validations completed: %s s" % timeE

    return Rpred_c_T, Rpred_cv_T, Rpred_v_T, order


if __name__ == '__main__':
    par = 'c0'

    linkage(par)
