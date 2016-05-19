#PBS -N calfem
#PBS -l nodes=1:ppn=1
#PBS -l mem=25gb
#PBS -q granulous
#PBS -l walltime=1:00:00
#PBS -j oe
#PBS -o out.$PBS_JOBID

cd /gpfs/scratch1/3/nhpnp3/5_11_composite
module purge
module load anaconda2
python main.py