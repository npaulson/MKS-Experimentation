cd /gpfs/scratch1/3/nhpnp3/3_14_db

for f in {48..96}
do
    echo " Submitting $f file..."
    export number=$f;
    msub -V run_script_integrate.sh
done
