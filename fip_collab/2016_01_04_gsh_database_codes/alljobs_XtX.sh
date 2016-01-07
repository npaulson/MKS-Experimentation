cd /panfs/iw-scratch.pace.gatech.edu/v7/nhpnp3/gsh_6deg_12_2

for f in {0..199}
do
    echo " Submitting $f file..."
    export number=$f;
    msub -V run_script_XtX.sh
done
