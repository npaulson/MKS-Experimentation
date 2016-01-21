cd /nv/gpfs-gateway-pace1/project/pme/pme1/nhpnp3/1_19_6deg

for f in {0..49}
do
    echo " Submitting $f file..."
    export number=$f;
    msub -V run_script_integrate.sh
done
