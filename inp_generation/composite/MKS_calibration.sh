#PBS -N calfem
#PBS -l nodes=1:ppn=2
#PBS -l mem=8000mb
#PBS -q granulous
#PBS -l walltime=00:15:00
#PBS -j oe
#PBS -o out.$PBS_JOBID

cd /gpfs/scratch1/3/nhpnp3/5_11_composite
module load abaqus/6.13
echo " Processing inp file" $number "\n"
abaqus job=$number cpus=2 mem=8000mb mp_mode=threads interactive