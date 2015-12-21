import numpy as np
import time
import euler_to_gsh as gsh
import calibration
import validation
import results
import functions as rr
from pymks_share import DataManager

manager = DataManager('pymks.me.gatech.edu')
print manager.list_datasets()
X, y  = manager.fetch_data('random hexagonal orientations')

print X.shape
print y.shape

el = X.shape[1]
H = 15
ns_cal = 40
ns_val = 10
set_id_val = 'val'
set_id_cal = 'cal'
wrt_file = 'log_file.txt'

X_cal = X[0:ns_cal, ...]
X_val = X[ns_cal:, ...]

y_cal = y[0:ns_cal, ...]
y_val = y[ns_cal:, ...]

# take fft of response fields
y_fft_cal = np.fft.fftn(y_cal, axes=[1, 2, 3])
y_fft_val = np.fft.fftn(y_val, axes=[1, 2, 3])

# Convert the orientations from the calibration datasets from bunge euler
# angles to GSH coefficients
M_cal = gsh.euler_to_gsh(X_cal, el, H, ns_cal, set_id_cal, wrt_file)

# Convert the orientations from the validation datasets from bunge euler
# angles to GSH coefficients
M_val = gsh.euler_to_gsh(X_val, el, H, ns_val, set_id_val, wrt_file)

# Perform the calibration
infl_coef = calibration.calibration_procedure(M_cal, y_fft_cal, el, H, ns_cal, wrt_file)

# Perform the validation
y_mks = validation.validation(M_val, infl_coef, el, wrt_file)

results.results(infl_coef, y_val, y_mks, el, ns_val)