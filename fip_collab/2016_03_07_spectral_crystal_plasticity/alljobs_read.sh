cd /gpfs/scratch1/3/nhpnp3/3_14_cpdb

for f in {0..59}
do
    echo " Submitting $f file..."
    export number=$f;
    msub -V run_script_read.sh
done
