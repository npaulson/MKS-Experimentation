import numpy as np
import matplotlib.pyplot as plt
import numpy.polynomial.legendre as leg
import h5py


def integrate(x, y, a, b, n_l, type):

    coeff = np.zeros(n_l, dtype='float64')

    for ii in xrange(n_l):

        if type == 'cosine':
            L = b - a
            ep_set = np.cos(ii*np.pi*(x-a)/L)
            bsz_cos = L/x.size
            if ii == 0:
                c_cos = 1./L
            else:
                c_cos = 2./L
            c_tot = c_cos * bsz_cos

        elif type == 'legendre':
            p_vec = np.zeros(ii+1)
            p_vec[ii] = 1
            ep_set = leg.legval(real2comm(x, a, b), p_vec)
            bsz_leg = 2./x.size
            c_leg = (2*ii+1)/2.
            c_tot = c_leg * bsz_leg

        coeff[ii] = c_tot*np.sum(y*ep_set)

    return coeff


def predict(coeff, x, a, b, type):

    L = b-a
    y = np.zeros(x.size, dtype='float64')

    for ii in xrange(n_l):

        if type == 'cosine':

            y += coeff[ii]*np.cos(ii*np.pi*(x-a)/L)

        elif type == 'legendre':

            p_vec = np.zeros(ii+1)
            p_vec[ii] = 1

            y += coeff[ii]*leg.legval(real2comm(x, a, b), p_vec)

    return y


def real2comm(x, a, b):
    return 2*((x-a)/(b-a))-1


""" generate test function """

n_l = 14
type = 'cosine'

# here we determine the sampling for en
a_std = 0.0050
b_std = 0.0085

# a = 0.00495  # start for en range
# b = 0.00855  # end for en range
# a = 0.0050  # start for en range
# b = 0.0086  # end for en range
a = 0.00485  # start for en range
b = 0.00905  # end for en range
# a = 0.0048  # start for en range
# b = 0.0092  # end for en range
# a = 0.0050
# b = 0.0085


f = h5py.File('Results_tensor_01.hdf5', 'r')
# fip = f.get('sim0000032')[:, 19]
fip = f.get('sim0000049')[:, 19]
f.close

en_inc = 0.0001  # en increment
et_norm = np.linspace(.0001, .0100, 100)
ai = np.int64(np.round(a_std/en_inc))-1  # index for start of en range
bi = np.int64(np.round(b_std/en_inc))-1  # index for end of en range

# sample_indx = np.arange(ai, bi+1)
# sample_indx = np.arange(ai+1, bi+1, 2)
sample_indx = np.arange(ai, bi+5, 3)
# sample_indx = np.arange(ai, bi+6, 4)
# sample_indx = np.arange(ai, bi, 1)

n_en = sample_indx.size

# xnode: en values for nodes
envec = et_norm[sample_indx]
print envec

y = fip[sample_indx]

""" perform integration for coefficients """

coeff = integrate(envec, y, a, b, n_l, type)

print "coefficients from integration: %s" % np.str(coeff)

""" calculate error in prediction """

std_indx = np.arange(ai, bi+1)
en_err = et_norm[std_indx]
y_err = fip[std_indx]

error = np.abs(y_err - predict(coeff, en_err, a, b, type))

print "mean error: %s" % error.mean()
print "maxiumum error: %s" % error.max()


""" plot function and reconstruction """

en_plt = np.linspace(a, b, 500)
y_ = predict(coeff, en_plt, a, b, type)

plt.figure(1)

plt.plot(et_norm, fip, 'bx-')
plt.plot(envec, y, 'bo')
plt.plot(en_plt, y_, 'r-')
plt.axis([a_std, b_std, -0.1*y_err.max(), 1.1*y_err.max()])

plt.title('%s series, %s points' % (type, n_en))
plt.xlabel('total strain')
plt.ylabel('FIP value')

plt.show()
