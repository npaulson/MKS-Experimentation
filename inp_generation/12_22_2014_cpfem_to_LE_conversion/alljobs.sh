cd /panfs/iw-scratch.pace.gatech.edu/v7/nhpnp3/val_priddy_12_22

for f in val_Priddy_*.inp
do
    echo " Submitting $f file..."
    export number=$f;
    msub -V MKS_calibration.sh
done
