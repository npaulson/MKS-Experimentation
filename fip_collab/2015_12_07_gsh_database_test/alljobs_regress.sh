cd /panfs/iw-scratch.pace.gatech.edu/v7/nhpnp3/gsh_test_12_7

for p in {0..7}
do
    echo " Submitting $p $q file..."
    export num_p=$p;
    msub -V run_script_regress.sh
done