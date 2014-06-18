import time
import subprocess as sp
import numpy

sp.call('ipcluster start -n 4 &', shell=True)

from IPython.parallel import Client


time.sleep(120)

rc = Client()
lview = rc.load_balanced_view()
lview.block = True
serial_result = map(lambda x:x**10, range(32))
parallel_result = lview.map(lambda x:x**10, range(32))
print serial_result == parallel_result

#sp.call('ipcluster stop', shell=True)