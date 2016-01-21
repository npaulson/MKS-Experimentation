cd /nv/gpfs-gateway-pace1/project/pme/pme1/nhpnp3/1_20_3deg

for f in {1..20}
do
    echo " Submitting $f file..."
    export number=$f;
    msub -V run_script_read.sh
done
