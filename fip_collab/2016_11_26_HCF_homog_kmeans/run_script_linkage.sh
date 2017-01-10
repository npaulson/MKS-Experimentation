#PBS -N calfem
#PBS -l nodes=1:ppn=1
#PBS -l mem=10gb
#PBS -q granulous
#PBS -l walltime=3:00:00
#PBS -j oe
#PBS -o out.$PBS_JOBID

cd $PBS_O_WORKDIR
module purge
module load anaconda2/2.1.0
python main_linkage.py