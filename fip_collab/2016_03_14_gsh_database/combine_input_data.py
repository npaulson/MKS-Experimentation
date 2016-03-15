import h5py
import numpy as np
import constants


C = constants.const()

n_par = C['n_eul']*C['n_en']

f1 = h5py.File('var_extract_total.hdf5', 'w')
alldata = f1.create_dataset("var_set", (n_par*C['n_th'], 6))

c = 0

for tt in xrange(0, C['n_th']):

    print "Deformation Mode: %s deg" % str((tt+0.5)*C['inc_th'])

    # create file for pre-database outputs
    f2 = h5py.File('var_extract_%s.hdf5' % str(tt+1).zfill(2), 'r')

    ep_tmp = f2.get("var_set")

    stt = (c)*n_par
    print "start index: %s" % stt

    end = (c+1)*n_par
    print "end index: %s" % end

    alldata[stt:end, :] = ep_tmp

    f2.close()

    c += 1

print alldata.shape

f1.close()
