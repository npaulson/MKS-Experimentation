#PBS -N calfem
#PBS -l nodes=1:ppn=1
#PBS -l mem=8000mb
#PBS -q granulous
#PBS -l walltime=05:00:00
#PBS -j oe
#PBS -o out.$PBS_JOBID

cd /nv/gpfs-gateway-scratch1/3/nhpnp3/1_31_5deg
module purge
module load anaconda2
echo " Processing file" $number "\n"
python integrate_parallel.py $number