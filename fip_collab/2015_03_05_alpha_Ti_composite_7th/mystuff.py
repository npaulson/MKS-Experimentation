import numpy as np


class Arraystats(object):

    def __init__(self, arrays):
        self.arrays = arrays

    def printstats(self):
        print self.arrays.shape
        print self.arrays.size
        print self.arrays.nbytes


testarray = np.random.rand(3, 4, 5)

happy_bday = Arraystats(testarray)

happy_bday.printstats()
