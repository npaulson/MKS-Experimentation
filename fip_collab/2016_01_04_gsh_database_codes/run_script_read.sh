#PBS -N calfem
#PBS -l nodes=1:ppn=1
#PBS -l mem=8000mb
#PBS -q granulous
#PBS -l walltime=01:00:00
#PBS -j oe
#PBS -o out.$PBS_JOBID

cd /nv/gpfs-gateway-pace1/project/pme/pme1/nhpnp3/1_21_3deg
module purge
module load anaconda2
echo " Processing file" $number "\n"
python read_input_data.py $number