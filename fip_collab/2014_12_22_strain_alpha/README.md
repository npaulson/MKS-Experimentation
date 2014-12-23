Author: Noah Paulson

## Test Descriptions

All simulations in this study are CPFEM, performed on Alpha-Ti polycrystals using Abaqus/6.13 to a strain amplitude of 0.5% by Matthew Priddy


results_50cal_5val.txt

* calibration with 50 datasets, from phi2=0 face. Each voxel is randomly assigned an orientation.
* validation with 5 datasets, from phi2=0 face. Each voxel is randomly assigned an orientation.

This gives better results than the method used in 2014_12_17_strain_alpha

results_199cal_Priddy_100val_Priddy.txt

* calibration with 199 datasets. Each grain in the equiaxed microstructure is randomly assigned an orientation from a uniformish ODF.
* validation with 100 datasets. Each grain in the equiaxed microstructure is randomly assigned an orientation from a basal texture ODF.