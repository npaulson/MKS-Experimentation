import alljobs_functions as af
import db_functions as fn
import combine_input_data as cid
import Xcalc_cos as xcos
import combine_Xcalc as cxc
import combine_coef_old as cc
import constants_old
import time


C = constants_old.const()
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

"""run scripts to calculate X for GSH"""

af.job_submit(njobs=C['XcalcGSH_njobs'],
              mem=C['XcalcGSH_mem'],
              walltime=C['XcalcGSH_walltime'],
              path=C['path'],
              scriptname=C['XcalcGSH_scriptname'])

"""run scripts to calculate X for the cosine bases"""

xcos.calculate()
fn.WP('X calculated for the cosine bases', logfile)

"""check to see that the jobs for XcalcGSH have completed"""

af.job_check(n_jobs=C['XcalcGSH_njobs'],
             walltime=C['XcalcGSH_walltime'],
             scriptname=C['XcalcGSH_scriptname'],
             logfile=logfile)

"""combine the X calculations"""

cxc.combine()
fn.WP('X combined for all bases', logfile)

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
