#PBS -N calfem
#PBS -l nodes=1:ppn=1
#PBS -l mem=5gb
#PBS -q granulous
#PBS -l walltime=1:00:00
#PBS -j oe
#PBS -o out.$PBS_JOBID

cd $PBS_O_WORKDIR
module purge
module load anaconda2
python test.py