cd /gpfs/scratch1/3/nhpnp3/

for f in {1302100..1302200}
do
    echo "cancel job $f"
    canceljob $f || true
done
