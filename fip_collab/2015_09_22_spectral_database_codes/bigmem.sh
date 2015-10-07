#PBS -N calfem
#PBS -l nodes=1:ppn=1
#PBS -l mem=100gb
#PBS -q granulous
#PBS -l walltime=00:15:00
#PBS -j oe
#PBS -o out.$PBS_JOBID

cd /panfs/iw-scratch.pace.gatech.edu/v7/nhpnp3/dir_10_2
module purge
module load oldrepo
module load python/2.7.2
echo " Processing file" $number "\n"
python bigmem.py $number