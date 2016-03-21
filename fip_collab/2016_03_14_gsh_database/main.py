import subprocess as sp
import write_jobsub as wj
import constants
import time


C = constants.const()

for ii in xrange(C['n_jobs_read']):
    filename = 'read_input.pbs'
    mem = C['read_mem']
    walltime = C['read_walltime']
    path = C['path']
    script_etc = '%s %s' % (C['read_scriptname'], str(ii+1))
    wj.writefile(filename, mem, walltime, path, script_etc)

    sp.call('msub %s' % filename)

while True:
    for ii in xrange(C['n_jobs_read']):
    	

    time.sleep(5)
