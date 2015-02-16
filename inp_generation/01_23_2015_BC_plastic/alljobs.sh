cd /panfs/iw-scratch.pace.gatech.edu/v7/nhpnp3/composite_plastic_1_7

for f in sq21*.inp
do
    echo " Submitting $f file..."
    export number=$f;
    msub -V MKS_calibration.sh
done
