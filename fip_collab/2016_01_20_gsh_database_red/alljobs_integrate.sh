cd /nv/gpfs-gateway-pace1/project/pme/pme1/nhpnp3/1_20_3deg

for f in {0..9}
do
    echo " Submitting $f file..."
    export number=$f;
    msub -V run_script_integrate.sh
done
