cd /panfs/iw-scratch.pace.gatech.edu/v7/nhpnp3/check_symm_11_20

for f in {1..13}
do
    echo " Submitting $f file..."
    export number=$f;
    msub -V run_script.sh
done
