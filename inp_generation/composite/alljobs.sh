cd /gpfs/scratch1/3/nhpnp3/5_11_composite

for f in *.inp
do
    echo " Submitting $f file..."
    export number=$f;
    msub -V MKS_calibration.sh
done
