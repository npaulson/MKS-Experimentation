#PBS -N calfem
#PBS -l nodes=1:ppn=1
#PBS -l mem=12000mb
#PBS -q granulous
#PBS -l walltime=24:00:00
#PBS -j oe
#PBS -o out.$PBS_JOBID

cd /gpfs/scratch1/3/nhpnp3/1_31_5deg
module purge
module load anaconda2
python main.py