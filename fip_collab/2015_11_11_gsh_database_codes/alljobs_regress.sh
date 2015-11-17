cd /panfs/iw-scratch.pace.gatech.edu/v7/nhpnp3/dir_11_12

for p in {0..7}
do
    for q in {0..7}
    do
        echo " Submitting $p $q file..."
        export num_p=$p;
        export num_q=$q;
        msub -V run_script_regress.sh
    done
done