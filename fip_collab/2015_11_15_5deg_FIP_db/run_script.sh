#PBS -N calfem
#PBS -l nodes=1:ppn=1
#PBS -l mem=8000mb
#PBS -q granulous
#PBS -l walltime=03:00:00
#PBS -j oe
#PBS -o out.$PBS_JOBID

cd /panfs/iw-scratch.pace.gatech.edu/v7/nhpnp3/fip_db_11_15
module load anaconda2
echo " Processing file" $number "\n"
python read_input_data5deg.py $number