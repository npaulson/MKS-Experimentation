import db_functions as fn
import constants_old
import h5py


def combine():

    C = constants_old.const()

    filename = 'log_Xcalc_combine.txt'

    f_master = h5py.File(C['combineXcalc_output'], 'w')

    """load the cosine basis evaluations"""
    f_cos = h5py.File(C['Xcalccos_output'], 'r')

    for name in f_cos.keys():
        fn.WP(name, filename)
        tmp = f_cos.get(name)[...]
        f_master.create_dataset(name, data=tmp)
        del tmp

    f_cos.close()

    """load the GSH basis evaluations"""
    for jobnum in xrange(C['XcalcGSH_njobs']):

        f_gsh = h5py.File(C['XcalcGSH_output'] % str(jobnum).zfill(5), 'r')

        for name in f_gsh.keys():
            fn.WP(name, filename)
            tmp = f_gsh.get(name)[...]
            f_master.create_dataset(name, data=tmp)
            del tmp

        f_gsh.close()

    f_master.close()


if __name__ == '__main__':
    combine()
