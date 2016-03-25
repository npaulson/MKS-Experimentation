import alljobs_functions as af
import db_functions as fn
import combine_input_data as cid
import basis_eval_cos as bcos
import combine_basis as bc
import combine_coef as cc
import constants
import time


C = constants.const()
logfile = 'log_%s.txt' % time.strftime("%Y-%m-%d_h%Hm%M")

# """run scripts to read files"""

# af.job_submit(njobs=C['read_njobs'],
#               mem=C['read_mem'],
#               walltime=C['read_walltime'],
#               path=C['path'],
#               scriptname=C['read_scriptname'])

# """check that the read jobs have completed"""

# af.job_check(n_jobs=C['read_njobs'],
#              walltime=C['read_walltime'],
#              scriptname=C['read_scriptname'],
#              logfile=logfile)

# """combine the files to read"""

# cid.combine()
# fn.WP('input files combined', logfile)

"""run scripts to evalute basis for GSH"""

af.job_submit(njobs=C['basisgsh_njobs'],
              mem=C['basisgsh_mem'],
              walltime=C['basisgsh_walltime'],
              path=C['path'],
              scriptname=C['basisgsh_scriptname'])

"""run scripts to calculate X for the cosine bases"""

bcos.calculate()
fn.WP('cosine bases evaluated', logfile)

"""check to see that the jobs for XcalcGSH have completed"""

af.job_check(n_jobs=C['basisgsh_njobs'],
             walltime=C['basisgsh_walltime'],
             scriptname=C['basisgsh_scriptname'],
             logfile=logfile)

fn.WP('gsh bases evaluated', logfile)

"""combine the basis evaluations"""

bc.combine()
fn.WP('all bases combined', logfile)

"""run scripts to perform the integration for coefficients"""

af.job_submit(njobs=C['integrate_njobs'],
              mem=C['integrate_mem'],
              walltime=C['integrate_walltime'],
              path=C['path'],
              scriptname=C['integrate_scriptname'])

"""check to see that the jobs for integrate_parallel have completed"""

af.job_check(n_jobs=C['integrate_njobs'],
             walltime=C['integrate_walltime'],
             scriptname=C['integrate_scriptname'],
             logfile=logfile)

"""combine the coefficients"""

cc.combine()
fn.WP('coefficients combined', logfile)
