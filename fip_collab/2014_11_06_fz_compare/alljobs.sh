cd /panfs/iw-scratch.pace.gatech.edu/v7/nhpnp3/fz_compare/phi2is0face

for f in phi2is0face_*.inp
do
    echo " Submitting $f file..."
    export number=$f;
    msub -V MKS_calibration.sh
done
