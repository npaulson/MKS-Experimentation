#PBS -N calfem
#PBS -l nodes=1:ppn=1
#PBS -l mem=8000mb
#PBS -q granulous
#PBS -l walltime=01:00:00
#PBS -j oe
#PBS -o out.$PBS_JOBID

cd /panfs/iw-scratch.pace.gatech.edu/v7/nhpnp3/gsh_test_12_7
module purge
module load anaconda2
echo " Processing file p=" $num_p "\n"
python fourier_regress_setup.py $num_p