import cPickle as pickle
import numpy as np

el = 21
el_t = el**3

r_10val = np.load("r_10val.npy")
r_40cal = np.load("r_40cal.npy")
euler_10val = np.load("euler_10val.npy")
euler_40cal = np.load("euler_40cal.npy")

print r_10val.shape
print euler_10val.shape

r_10val = r_10val.reshape(10, el, el, el)
r_40cal = r_40cal.reshape(40, el, el, el)

euler_10val = np.transpose(euler_10val, [1, 0, 2]).reshape(10, el, el, el, 3)
euler_40cal = np.transpose(euler_40cal, [1, 0, 2]).reshape(40, el, el, el, 3)
print euler_10val.shape

X = np.concatenate((euler_10val, euler_40cal))
y = np.concatenate((r_10val, r_40cal))

pickle.dump([X, y], open('calibration.pkl', 'wb'), protocol=2)
# pickle.dump([euler_10val, r_10val], open('calibration.pkl', 'wb'), protocol=2)