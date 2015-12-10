#PBS -N calfem
#PBS -l nodes=1:ppn=2
#PBS -l mem=8000mb
#PBS -q granulous
#PBS -l walltime=00:15:00
#PBS -j oe
#PBS -o out.$PBS_JOBID

cd /panfs/iw-scratch.pace.gatech.edu/v7/nhpnp3/fz_compare/phi2is0extr
module load abaqus/6.13
abaqus job=1 cpus=2 mem=8000mb mp_mode=threads interactive