import numpy as np


def writefile(filename, mem, walltime, path, script_etc):

    f = open(filename, 'w')
    f.write('#PBS -N calfem\n')
    f.write('#PBS -l nodes=1:ppn=1\n')
    f.write('#PBS -l mem=%sgb\n' % np.int64(mem))
    f.write('#PBS -q granulous\n')
    f.write('#PBS -l walltime=%s:00:00\n' % str(walltime).zfill(2))
    f.write('#PBS -j oe\n')
    f.write('#PBS -o out.$PBS_JOBID\n\n')
    f.write('cd %s\n' % path)
    f.write('module purge\n')
    f.write('module load anaconda2\n')
    f.write('python %s' % script_etc)
    f.close()


if __name__ == '__main__':
    filename = 'test.pbs'
    mem = 1
    walltime = 5
    path = '\\blahblahblah\\newbloh'
    script_etc = 'test.py 9'
    writefile(filename, mem, walltime, path, script_etc)
