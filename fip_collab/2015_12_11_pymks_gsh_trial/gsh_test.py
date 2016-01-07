import numpy as np
from pymks.bases import GSHBasis

X = np.array([[0.1, 0.2, 0.3],
              [6.5, 2.3, 3.4]])

gsh_basis = GSHBasis(n_states = [1], domain='hex')
def q(x):
   phi1 = x[..., 0]
   phi = x[..., 1]
   phi2 = x[..., 2]
   t913 = np.sin(phi)
   x_GSH = -(0.5e1 / 0.4e1) * np.exp((-2*1j) * phi1) * np.sqrt(0.6e1) * t913 ** 2
   return x_GSH

assert(np.allclose(np.squeeze(gsh_basis.discretize(X)), q(X)))

gsh_basis = GSHBasis(n_states = [1], domain='squishy')