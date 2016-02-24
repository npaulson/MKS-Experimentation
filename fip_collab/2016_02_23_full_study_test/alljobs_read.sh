cd /nv/gpfs-gateway-scratch1/3/nhpnp3/1_31_5deg

for f in {1..40}
do
    echo " Submitting $f file..."
    export number=$f;
    msub -V run_script_read.sh
done
