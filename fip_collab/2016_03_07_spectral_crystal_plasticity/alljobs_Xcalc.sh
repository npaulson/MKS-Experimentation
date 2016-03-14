cd /gpfs/pace1/project/me-kalidindi/shared/dir_nhp

for f in {0..39}
do
    echo " Submitting $f file..."
    export number=$f;
    msub -V run_script_Xcalc.sh
done
