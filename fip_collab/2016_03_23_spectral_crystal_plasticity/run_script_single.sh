#PBS -N calfem
#PBS -l nodes=1:ppn=1
#PBS -l mem=14000mb
#PBS -q granulous
#PBS -l walltime=5:00:00
#PBS -j oe
#PBS -o out.$PBS_JOBID

cd /gpfs/pace1/project/me-kalidindi/shared/dir_nhp
module purge
module load anaconda2
python main.py