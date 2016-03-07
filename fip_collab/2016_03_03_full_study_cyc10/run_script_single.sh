#PBS -N calfem
#PBS -l nodes=1:ppn=1
#PBS -l mem=8000mb
#PBS -q granulous
#PBS -l walltime=10:00:00
#PBS -j oe
#PBS -o out.$PBS_JOBID

cd /nv/gpfs/scratch1/3/nhpnp3/1_31_5deg
module purge
module load anaconda2
python Xcalc.py