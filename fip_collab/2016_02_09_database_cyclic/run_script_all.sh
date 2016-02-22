cd /nv/gpfs-gateway-scratch1/3/nhpnp3/2_9_cyc

for f in {1..559}
do
    echo " Submitting $f file..."
    export number=$f;
    msub -V run_script_read.sh
done

export file="combine_input_data.py";
msub -V run_script_single.sh

export file="Xcalc.py";
msub -V run_script_single.sh 

for f in {0..399}
do
    echo " Submitting $f file..."
    export number=$f;
    msub -V run_script_integrate.sh
done
 
export file="combine_coeff.py";
msub -V run_script_single.sh 