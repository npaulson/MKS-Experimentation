import numpy as np
import matplotlib.pyplot as plt
import scipy.special as sp
import sympy as sy
import sympy.functions.combinatorial.factorials as fac
from sympy import init_printing
from sympy import symbols

l, m, n, x = symbols('l m n x')
init_printing(use_unicode=True)

expr = ((2)**(l-m))
print expr
expr = n*expr
print expr
print expr.subs([(l, 1), (m, 2), (n, 0.5)])

tmp1 = (-1)**(l-m)
tmp2 = (1j)**(n-m)
tmp3 = tmp1*tmp2

print tmp3

tmp4 = (2**l)*fac.factorial(l-m)

print tmp3/tmp4

rrr = sy.sqrt(l/m)
print rrr

# tmp5 = sy.Rational(tmp3, tmp4)

# print tmp5

# lmax = 16
# inc = 0.01
# x = np.arange(-1, 1+inc, inc)

# """ generate Imat """

# Imat = np.zeros([lmax, 2], dtype='int64')

# c = 0
# for n in xrange(lmax):
# 	for m in xrange(-n, n+1):
# 		Imat[c, :] = [m, n]
# 		c +=1
# 		if c == lmax:
# 			break
# 	if c == lmax:
# 		break

# print Imat

# """ calculate XhX """

# XhX = np.zeros((lmax, lmax), dtype='complex128')

# for ii in xrange(lmax):
#     print ii
#     for jj in xrange(lmax):

#     	m_ii, n_ii = Imat[ii, :]
#     	m_jj, n_jj = Imat[jj, :]

#         xii = sp.lpmn(m_ii, n_ii, x)
#         xjj = sp.lpmn(m_jj, n_jj, x)

#         XhX[ii, jj] = np.dot(xii.conj(), xjj)


# """ plot the XhX matrix """

# plt.figure(1)

# plt.subplot(121)

# ax = plt.imshow(np.real(XhX), origin='lower',
#                 interpolation='none', cmap='jet')
# plt.title("real(XhX): GSH")
# plt.colorbar(ax)

# plt.subplot(122)

# ax = plt.imshow(np.imag(XhX), origin='lower',
#                 interpolation='none', cmap='jet')
# plt.title("imag(XhX): GSH")
# plt.colorbar(ax)

# plt.show()
