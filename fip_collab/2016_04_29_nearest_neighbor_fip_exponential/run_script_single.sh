#PBS -N calfem
#PBS -l nodes=1:ppn=1
#PBS -l mem=12000mb
#PBS -q iw-shared-6
#PBS -l walltime=10:00:00
#PBS -j oe
#PBS -o out.$PBS_JOBID

cd /gpfs/scratch1/3/nhpnp3/5_3_Xdir
module purge
module load anaconda2
python main_cal.py