import numpy as np
import h5py
import time


def WP(msg, filename):
    """
    Summary:
        This function takes an input message and a filename, and appends that
        message to the file. This function also prints the message
    Inputs:
        msg (string): the message to write and print.
        filename (string): the full name of the file to append to.
    Outputs:
        both prints the message and writes the message to the specified file
    """
    fil = open(filename, 'a')
    print msg
    fil.write(msg)
    fil.write('\n')
    fil.close()


fname = "log_check_db_loop.txt"

""" initialize the variables of interest """

inc = 5  # degree increment for angular variables

n_th_max = 120/inc  # number of theta samples in FOS
n_max = 360/inc  # number of phi1, Phi and phi2 samples in FOS
n_hlf = 180/inc  # half n_max

n_th = (60/inc)+1  # number of theta samples for FZ
n_p1 = 360/inc  # number of phi1 samples for FZ
n_P = (90/inc)+1  # number of Phi samples for FZ
n_p2 = 60/inc  # number of phi2 samples for FZ

# the total number positions in the first 4 dimensions of the database
Numel = n_th_max*n_max**3

# vector of the ranges of the first 4 dimensions in radians
Lset = np.array([(1./3.), 2., 2., 2.])*np.pi

""" get data from the spectral coefficients file """

# open the spectral coefficients file
f_db = h5py.File("final_db.hdf5", 'r')
# retrieve the list of indices
tmp = f_db.get("s_list")
s_list = tmp[...]
# retrieve associated list of fourier coefficients
tmp = f_db.get("f_list")
f_list = tmp[...]
# close the spectral coefficients file
f_db.close()

""" get data from the validation data file """

# open the error checking file
f_err = h5py.File('var_val.hdf5', 'r')
# retrieve the array of plastic strain values for various combination of input
# parameters
var_set = f_err.get("var_set")[...]
# close the error checking file
f_err.close()

# the columns of xi contain the position in degrees for each of the first four
# angular dimensions of interest
xi = var_set[:, :4]
n_S = xi.shape[0]  # number of samples

""" perform the interpolation """

err = np.zeros([n_S, 8])
err[:, :4] = var_set[:, :4]
err[:, 4] = var_set[:, -1]

# for ii in xrange(n_S):
for ii in xrange(0, 100):

    # start timing the interpolation
    st = time.time()

    Pvec = f_list[:, -1] * \
        np.exp((2*np.pi*1j*s_list[:, 0]*xi[ii, 0])/Lset[0]) * \
        np.exp((2*np.pi*1j*s_list[:, 1]*xi[ii, 1])/Lset[1]) * \
        np.exp((2*np.pi*1j*s_list[:, 2]*xi[ii, 2])/Lset[2]) * \
        np.exp((2*np.pi*1j*s_list[:, 3]*xi[ii, 3])/Lset[3])

    result = np.real(np.sum(Pvec, 0)/Numel)
    err[ii, 5] = result

    err[ii, 6] = np.abs(result-var_set[ii, -1])

    # end timing
    timeE = np.round(time.time() - st, 5)
    err[ii, 7] = timeE

    msg = "true value: %s, predicted value: %s, time: %ss" % \
          (var_set[ii, -1], result, timeE)

    WP(msg, fname)

""" analyze the results """

print "mean db value: %s" % np.mean(var_set[:, -1])
print "minimum db value: %s" % np.min(var_set[:, -1])
print "maximum db value: %s" % np.max(var_set[:, -1])
