import numpy as np
import matplotlib.pyplot as plt


def test_func(xsamp):

    ysamp = (1e-10)*(np.exp(2000*xsamp)-1.)

    return ysamp


""" generate test function """

n_l = 50

# here we determine the sampling for en
a = 0.0050  # start for en range
b = 0.0085  # end for en range
L_en = b - a

# en_inc = 0.0001  # en increment
# et_norm = np.linspace(.0001, .0100, 100)
# ai = np.int64(np.round(a/en_inc))-1  # index for start of en range
# bi = np.int64(np.round(b/en_inc))-1  # index for end of en range
# sample_indx = np.arange(ai+1, bi, 3)
# n_en = sample_indx.size

# # xnode: en values for nodes
# envec = et_norm[sample_indx]

envec = np.linspace(a, b, 100)

print envec

y = test_func(envec)

""" perform integration for coefficients """

coeff = np.zeros(n_l, dtype='float64')

bsz_cos = (b-a)/envec.size

for ii in xrange(n_l):

    ep_set = np.cos(ii*np.pi*(envec-a)/L_en)

    if ii == 0:
        c_cos = 1./L_en
    else:
        c_cos = 2./L_en

    c_tot = c_cos * bsz_cos

    coeff[ii] = c_tot*np.sum(y*ep_set)

print "coefficients from integration: %s" % np.str(coeff)

""" reconstruct the function """

en_plt = np.linspace(0.0, b, 100)
y_plt = test_func(en_plt)

y_ = np.zeros(en_plt.size, dtype='float64')

for ii in xrange(n_l):

    y_ += coeff[ii]*np.cos(ii*np.pi*(en_plt-a)/L_en)


""" plot function and reconstruction """

plt.figure(1)

plt.plot(envec, y, 'bo')
plt.plot(en_plt, y_plt, 'bx-')
plt.plot(en_plt, y_, 'rx-')
plt.axis([a, b, -0.1*y_plt.max(), 1.1*y_plt.max()])

plt.show()
