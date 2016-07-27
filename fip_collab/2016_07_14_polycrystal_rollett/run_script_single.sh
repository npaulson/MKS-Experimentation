#PBS -N calfem
#PBS -l nodes=1:ppn=1
#PBS -l mem=30gb
#PBS -q granulous
#PBS -l walltime=10:00:00
#PBS -j oe
#PBS -o out.$PBS_JOBID

cd /gpfs/pace1/project/me-kalidindi/shared/Ti64_spatial_stats
module purge
module load anaconda2
python main_rep.py