import numpy as np


"""intialize random points"""
npts = 10000
ndist = 100
mu = 0.
sig = 1.

rawdata = 2.*(2.*np.random.random(size=(npts,))-1.)+0.5

"""randomly select ndist points from rawdata"""
tmp = np.zeros(rawdata.shape, dtype=bool)
tmp[:ndist] = True
np.random.shuffle(tmp)

sorig = rawdata[tmp]

"""in each iteration randomly replace one point
with another from rawdata. Keep this switch if the
mean and standard dev are closer to the target values"""

sold = sorig
snew = sold
muold = sorig.mean()
muDold = np.abs(mu-muold)
sigold = sorig.std()
sigDold = np.abs(sig-sigold)

print muold
print sigold

for ii in xrange(np.int32(1e4)):

    snew = sold

    idx1 = np.random.randint(ndist)
    idx2 = np.random.randint(npts)
    snew[idx1] = rawdata[idx2]

    munew = snew.mean()
    muDnew = np.abs(mu-munew)
    signew = snew.std()
    sigDnew = np.abs(sig-signew)

    cost = np.random.rand()*(muDnew - muDold) + np.random.rand()*(sigDnew - sigDold)

    if cost < 0:
        # print "better point selected"
        # print "new mu: " + str(munew)
        # print "new sig: " + str(signew)

        muold = munew
        muDold = muDnew
        sigold = signew
        sigDold = sigDnew
        sold = snew

print munew
print signew
