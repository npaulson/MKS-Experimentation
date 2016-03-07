cd /nv/gpfs/scratch1/3/nhpnp3/1_31_5deg

for f in {0..49}
do
    echo " Submitting $f file..."
    export number=$f;
    msub -V run_script_integrate.sh
done
