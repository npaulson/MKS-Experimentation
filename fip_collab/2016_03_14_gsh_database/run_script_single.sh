#PBS -N calfem
#PBS -l nodes=1:ppn=1
#PBS -l mem=12000mb
#PBS -q granulous
#PBS -l walltime=05:00:00
#PBS -j oe
#PBS -o out.$PBS_JOBID

cd /gpfs/scratch1/3/nhpnp3/3_14_db
module purge
module load anaconda2
python combine_Xcalc.py