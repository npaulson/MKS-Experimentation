from pymks_share import DataManager
import matplotlib.pylab as plt
import time

st = time.time()

manager = DataManager('pymks.me.gatech.edu')
X = manager.fetch_data(manager.list_datasets()[0])

print "fetch time: %s" % (time.time()-st)

for x in X:
    plt.imshow(x, cmap='gray')
    plt.show()