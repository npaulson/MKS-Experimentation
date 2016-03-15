#PBS -N calfem
#PBS -l nodes=1:ppn=1
#PBS -l mem=12gb
#PBS -q granulous
#PBS -l walltime=05:00:00
#PBS -j oe
#PBS -o out.$PBS_JOBID

cd /gpfs/scratch1/3/nhpnp3/3_14_cpdb
module purge
module load anaconda2
echo " Processing file" $number "\n"
python Xcalc_GSH_parallel.py $number