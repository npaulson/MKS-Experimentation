from joblib import Parallel, delayed


def stupidcalc(ii):
    return ii**2

rrr = Parallel(n_jobs=1)(delayed(stupidcalc)(ii) for ii in xrange(10))

print rrr
