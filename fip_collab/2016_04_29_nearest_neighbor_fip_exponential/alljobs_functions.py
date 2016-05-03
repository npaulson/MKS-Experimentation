import numpy as np
import functions as rr
import subprocess as sp
import time
import os


def job_check(n_jobs, walltime, scriptname, logfile):

    flag_sum = 0
    st = time.time()

    while flag_sum < n_jobs:

        time.sleep(5)
        flag_sum = 0

        for ii in xrange(n_jobs):

            flag_file = "flag%s" % str(ii).zfill(5)

            if os.path.isfile(flag_file):
                flag_sum += 1
            else:
                break

        if (time.time()-st)/3600. > walltime:
            raise RuntimeError("walltime exceeded for %s" % scriptname)

    for ii in xrange(n_jobs):
        os.remove("flag%s" % str(ii).zfill(5))

    rr.WP('all jobs completed', logfile)


def job_submit(njobs, mem, walltime, path, scriptname):

    for ii in xrange(njobs):

        filename = 'temp.sh'

        writefile(filename,
                  mem,
                  walltime,
                  path,
                  '%s %s' % (scriptname, ii))

        sp.call('msub %s' % filename, shell=True)


def writefile(filename, mem, walltime, path, script_etc):

    f = open(filename, 'w')
    f.write('#PBS -N calfem\n')
    f.write('#PBS -l nodes=1:ppn=1\n')
    f.write('#PBS -l mem=%sgb\n' % np.int64(mem))
    f.write('#PBS -q iw-shared-6\n')
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
    path = '\\foo\\bar'
    script_etc = 'test.py 9'
    writefile(filename, mem, walltime, path, script_etc)
