cd /panfs/iw-scratch.pace.gatech.edu/v7/nhpnp3/rand_cal_12_18

for f in cal_*.inp
do
    echo " Submitting $f file..."
    export number=$f;
    msub -V MKS_calibration.sh
done
