import numpy as np
import matplotlib.pyplot as plt

from pymks_share import DataManager

manager = DataManager('pymks.me.gatech.edu')
print manager.list_datasets()
X, y  = manager.fetch_data('random hexagonal orientations')

print X.shape
print y.shape

n = X.shape[1]
center = (n-1) / 2

X_cal = X[0:40, ...]
X_val = X[40:, ...]
y_cal = y[0:40, ...]
y_val = y[40:, ...]

from pymks import MKSLocalizationModel
from pymks.bases import GSHBasisHexagonal

gsh_hex_basis = GSHBasisHexagonal(n_states=15)
model = MKSLocalizationModel(basis=gsh_hex_basis)

model.fit(X_cal, y_cal)