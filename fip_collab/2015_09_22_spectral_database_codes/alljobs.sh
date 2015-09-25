cd /panfs/iw-scratch.pace.gatech.edu/v7/nhpnp3/dir_9_22

for f in 1 2 3 4 5 6 7 8 9 10 11
do
    echo " Submitting $f file..."
    export number=$f;
    msub -V run_script.sh
done
