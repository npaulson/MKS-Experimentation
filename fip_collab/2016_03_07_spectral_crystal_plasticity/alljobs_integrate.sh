cd /gpfs/scratch1/3/nhpnp3/3_14_cpdb

for f in {0..400}
do
    echo " Submitting $f file..."
    export number=$f;
    msub -V run_script_integrate.sh
done
