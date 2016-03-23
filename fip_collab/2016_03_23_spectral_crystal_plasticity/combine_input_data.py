import h5py
import constants


def combine():

    C = constants.const()

    f1 = h5py.File(C['combineread_output'], 'w')
    alldata = f1.create_dataset("var_set", (C['n_eul']*C['n_th'], 14))

    c = 0

    for tt in xrange(C['n_th']):

        print "Deformation Mode: %s deg" % str((tt+0.5)*C['inc'])

        # create file for pre-database outputs
        f2 = h5py.File(C['read_output'] % str(tt).zfill(5), 'r')

        ep_tmp = f2.get("var_set")

        stt = (c)*C['n_eul']
        print "start index: %s" % stt

        end = (c+1)*C['n_eul']
        print "end index: %s" % end

        alldata[stt:end, :] = ep_tmp

        f2.close()

        c += 1

    print alldata.shape

    f1.close()


if __name__ == '__main__':
    combine()
