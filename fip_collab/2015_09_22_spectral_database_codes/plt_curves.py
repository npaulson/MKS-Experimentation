import numpy as np
import matplotlib.pyplot as plt
import sys


tnum = sys.argv

ep11 = np.load("ep11_%s.npy" % tnum[1])
I2 = np.load("I2_%s.npy" % tnum[1])
I3 = np.load("I3_%s.npy" % tnum[1])

etvec = np.linspace(.0001, .0100, 100)

# plot one of the variables while all other variables are held constant
plt.figure(num=1, figsize=[9, 5])

plt.plot(etvec[63:96], ep11[63:96])
plt.xlabel("et_norm")
plt.ylabel("ep11")
plt.title("et_norm vs ep11")
plt.savefig("ep11_%s.png" % tnum[1])

plt.figure(num=2, figsize=[9, 5])

plt.plot(etvec[63:96], I2[63:96])
plt.xlabel("et_norm")
plt.ylabel("I2")
plt.title("et_norm vs I2")
plt.savefig("I2_%s.png" % tnum[1])

plt.figure(num=3, figsize=[9, 5])

plt.plot(etvec[63:96], I3[63:96])
plt.xlabel("et_norm")
plt.ylabel("I3")
plt.title("et_norm vs I3")
plt.savefig("I3_%s.png" % tnum[1])


plt.show()
