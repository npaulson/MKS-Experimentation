# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss
import matplotlib.cm as cm

beta = 1.
mu = 0
sigma = 1

alpha = np.arange(0.5, 1, 0.05)
# alpha = np.log(np.linspace(1, np.exp(1), 6))
# alpha = [0.01, 0.03, 0.05, 0.1, 0.3, 0.5, 1]

colormat = cm.plasma(np.linspace(0, 0.9, len(alpha)))

fig, ax = plt.subplots(num=1, figsize=[6, 4])

Z = [[0, 0], [0, 0]]
levels = alpha
CS3 = plt.contourf(Z, levels, cmap=cm.plasma)
plt.clf()

x = np.linspace(0, 5, 1000)

for ii in xrange(len(alpha)):

    pdf = ss.gamma.pdf(x, a=alpha[ii], loc=mu, scale=sigma)

    plt.plot(x, pdf, color=colormat[ii, :],
             lw=1.5, alpha=.9)

plt.xlabel(r'$x$', fontsize='large')
plt.ylabel(r'$f\left(x\vert \alpha,\mu=%s, \sigma=%s \right)$' % (mu, sigma),
           fontsize='large')

plt.colorbar(CS3)

plt.ylim((0, 2))

plt.tight_layout()

fig, ax = plt.subplots(num=2, figsize=[6, 4])

x = np.linspace(0, 5, 1000)

for ii in xrange(len(alpha)):

    cdf = ss.gamma.cdf(x, a=alpha[ii], loc=mu, scale=sigma)

    plt.plot(x, cdf, color=colormat[ii, :],
             lw=1.5, alpha=.9)

plt.xlabel(r'$x$', fontsize='large')
plt.ylabel(r'$F\left(x\vert \alpha,\mu=%s, \sigma=%s \right)$' % (mu, sigma),
           fontsize='large')

plt.colorbar(CS3)

plt.tight_layout()

plt.show()

# fig_name = 'PDF_alpha%s.png' % alpha
# fig.canvas.set_window_title(fig_name)
# fig.savefig(fig_name)
