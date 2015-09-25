#PBS -N calfem
#PBS -l nodes=1:ppn=1
#PBS -l mem=8000mb
#PBS -q granulous
#PBS -l walltime=05:00:00
#PBS -j oe
#PBS -o out.$PBS_JOBID

cd /panfs/iw-scratch.pace.gatech.edu/v7/nhpnp3/dir_9_22
module purge
module load oldrepo
module load python/2.7.2
echo " Processing file" $number "\n"
python check_db_single.py $number