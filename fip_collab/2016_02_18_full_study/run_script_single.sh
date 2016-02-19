#PBS -N calfem
#PBS -l nodes=1:ppn=1
#PBS -l mem=8000mb
#PBS -q granulous
#PBS -l walltime=03:00:00
#PBS -j oe
#PBS -o out.$PBS_JOBID

cd /nv/gpfs-gateway-scratch1/3/nhpnp3/2_18_full
module purge
module load anaconda2
python main_cal.py
python main_val.py