#PBS -N calfem
#PBS -l nodes=1:ppn=1
#PBS -l mem=20gb
#PBS -q granulous
#PBS -l walltime=01:00:00
#PBS -j oe
#PBS -o out.$PBS_JOBID

cd /gpfs/pace1/project/me-kalidindi/shared/dir_nhp
module purge
module load anaconda2
echo " Processing file" $number "\n"
python Xcalc_GSH_parallel.py $number