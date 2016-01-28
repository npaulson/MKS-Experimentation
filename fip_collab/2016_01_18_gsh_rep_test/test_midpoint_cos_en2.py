import numpy as np
import matplotlib.pyplot as plt
import h5py


def integrate_cos(x, y, a, b, n_l):

    coeff = np.zeros(n_l, dtype='float64')

    L = b - a

    bsz_cos = L/envec.size

    for ii in xrange(n_l):

        ep_set = np.cos(ii*np.pi*(x-a)/L)

        if ii == 0:
            c_cos = 1./L
        else:
            c_cos = 2./L

        c_tot = c_cos * bsz_cos

        coeff[ii] = c_tot*np.sum(y*ep_set)

    return coeff


def predict(coeff, x, a, b):

    L = b-a
    y = np.zeros(x.size, dtype='float64')

    for ii in xrange(n_l):
        y += coeff[ii]*np.cos(ii*np.pi*(x-a)/L)

    return y


""" generate test function """

n_l = 14

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

f = h5py.File('Results_tensor_01.hdf5', 'r')
# fip = f.get('sim0000032')[:, 19]
fip = f.get('sim0000041')[:, 19]
f.close

en_inc = 0.0001  # en increment
et_norm = np.linspace(.0001, .0100, 100)
ai = np.int64(np.round(a_std/en_inc))-1  # index for start of en range
bi = np.int64(np.round(b_std/en_inc))-1  # index for end of en range

# sample_indx = np.arange(ai, bi+1)
# sample_indx = np.arange(ai+1, bi+1, 2)
sample_indx = np.arange(ai, bi+5, 3)
# sample_indx = np.arange(ai, bi+6, 4)

n_en = sample_indx.size

# xnode: en values for nodes
envec = et_norm[sample_indx]
print envec

y = fip[sample_indx]

""" perform integration for coefficients """

coeff = integrate_cos(envec, y, a, b, n_l)

print "coefficients from integration: %s" % np.str(coeff)

""" calculate error in prediction """

std_indx = np.arange(ai, bi+1)
en_err = et_norm[std_indx]
y_err = fip[std_indx]

error = np.abs(y_err - predict(coeff, en_err, a, b))

print "mean error: %s" % error.mean()
print "maxiumum error: %s" % error.max()


""" plot function and reconstruction """

en_plt = np.linspace(0.0, b, 500)
y_ = predict(coeff, en_plt, a, b)

plt.figure(1)

plt.plot(et_norm, fip, 'bx-')
plt.plot(envec, y, 'bo')
plt.plot(en_plt, y_, 'r-')
plt.axis([a_std, b_std, -0.1*y_err.max(), 1.1*y_err.max()])

plt.show()
