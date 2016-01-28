import numpy as np
import matplotlib.pyplot as plt
import numpy.polynomial.legendre as leg
import h5py


def real2comm(x, a, b):
    return 2*((x-a)/(b-a))-1


def comm2real(x, a, b):
    return 0.5*(x+1)*(b-a)+a


""" generate test function """

n_l = 6

# here we determine the sampling for en
a = 0.00495  # start for en range
b = 0.00855  # end for en range
# a = 0.0050  # start for en range
# b = 0.0086  # end for en range

f = h5py.File('Results_tensor_01.hdf5', 'r')
fip = f.get('sim0000032')[:, 19]
f.close

en_inc = 0.0001  # en increment
et_norm = np.linspace(.0001, .0100, 100)
ai = np.int64(np.round(a/en_inc))-1  # index for start of en range
bi = np.int64(np.round(b/en_inc))-1  # index for end of en range

sample_indx = np.arange(ai, bi)
# sample_indx = np.arange(ai+1, bi+1, 2)

n_en = sample_indx.size

# xnode: en values for nodes
envec = et_norm[sample_indx]
print envec

y = fip[sample_indx]

""" perform integration for coefficients """

coeff = np.zeros(n_l, dtype='float64')

bsz_leg = 2./n_en

for ii in xrange(n_l):

    p_vec = np.zeros(ii+1)
    p_vec[ii] = 1

    ep_set = leg.legval(real2comm(envec, a, b), p_vec)

    c_leg = (2*ii+1)/2.

    c_tot = c_leg * bsz_leg

    coeff[ii] = c_tot*np.sum(y*ep_set)

print "coefficients from integration: %s" % np.str(coeff)

""" reconstruct the function """

en_plt = np.linspace(0.0, b, 500)

y_ = np.zeros(en_plt.size, dtype='float64')

for ii in xrange(n_l):

    p_vec = np.zeros(ii+1)
    p_vec[ii] = 1

    y_ += coeff[ii]*leg.legval(real2comm(en_plt, a, b), p_vec)


""" plot function and reconstruction """

plt.figure(1)

plt.plot(et_norm, fip, 'b-')
plt.plot(envec, y, 'bo')
plt.plot(en_plt, y_, 'r-')
plt.axis([a, b, -0.1*y.max(), 1.1*y.max()])

plt.show()
