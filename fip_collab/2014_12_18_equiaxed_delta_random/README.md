Author: Noah Paulson

## Test Descriptions

All simulations in this study are Linear Elastic, performed on Alpha-Ti polycrystals using Abaqus/6.13

results_100cal_25val_rand.txt :

* calibration with 100 datasets, from phi2=0 face, 101 orientations, only one orientation for phi=0 edge at [0,0,0] (phi1,Phi,phi2). Each voxel is randomly assigned an orientation.
* validation with 25 datasets, same orientations as for calibration. Each voxel is randomly assigned an orientation.

results_100cal_25val_rand_large.txt

* calibration with 100 datasets, from phi2=0 face, 101 orientations, only one orientation for phi=0 edge at [0,0,0] (phi1,Phi,phi2). Each voxel is randomly assigned an orientation.
* validation with 25 datasets, 10,000 orientations from [0 <= phi1 <= 2*pi, 0 <= Phi <= pi, 0 <= phi2 <= pi/3]. Each voxel is randomly assigned an orientation.

results_100cal_25val_equiaxed.txt

* calibration with 100 datasets, from phi2=0 face, 101 orientations, only one orientation for phi=0 edge at [0,0,0] (phi1,Phi,phi2). Each voxel is randomly assigned an orientation.
* validation with 25 datasets, 4,800 orientations from [0 <= phi1 <= 2*pi, 0 <= Phi <= pi/2, 0 <= phi2 <= pi/3]. Each grain is randomly assigned an orientation.

results_100cal_25val_delta.txt

* calibration with 100 datasets, from phi2=0 face, 101 orientations, only one orientation for phi=0 edge at [0,0,0] (phi1,Phi,phi2). Each voxel is randomly assigned an orientation.
* validation with 25 datasets, 4,800 orientations from [0 <= phi1 <= 2*pi, 0 <= Phi <= pi/2, 0 <= phi2 <= pi/3]. The center cell and surroundings are each randomly assigned an orientation

results_100calV2_25val_equiaxed.txt

* calibration with 100 datasets, from phi2=0 face, only one orientation for phi=0 edge at [0,0,0] (phi1,Phi,phi2). Each voxel is randomly assigned an orientation.
* validation with 25 datasets, 4,800 orientations from [0 <= phi1 <= 2*pi, 0 <= Phi <= pi/2, 0 <= phi2 <= pi/3]. Each grain is randomly assigned an orientation.


results_100caldelta_25val_equiaxed.txt

* calibration with 100 datasets, from phi2=0 face, 101 orientations, only one orientation for phi=0 edge at [0,0,0] (phi1,Phi,phi2). The center cell and surroundings are each randomly assigned an orientation
* validation with 25 datasets, 4,800 orientations from [0 <= phi1 <= 2*pi, 0 <= Phi <= pi/2, 0 <= phi2 <= pi/3]. Each grain is randomly assigned an orientation.


results_200cal_rand_del_25val_equiaxed.txt

* calibration with 200 datasets, from phi2=0 face, 101 orientations, only one orientation for phi=0 edge at [0,0,0] (phi1,Phi,phi2). For 100 each voxel is randomly assigned an orientation. For the other 100 the center cell and surroundings are each randomly assigned an orientation 
* validation with 25 datasets, 4,800 orientations from [0 <= phi1 <= 2*pi, 0 <= Phi <= pi/2, 0 <= phi2 <= pi/3]. Each grain is randomly assigned an orientation

results_100cal_25val_equiaxed_nonorm.txt

* in this iteration the normalization ([1,5,5,5,5,5,9,9,9,9,9,9,9,9,9]) was removed from the GSH coefficients
* calibration with 100 datasets, from phi2=0 face, 101 orientations, only one orientation for phi=0 edge at [0,0,0] (phi1,Phi,phi2). Each voxel is randomly assigned an orientation.
* validation with 25 datasets, 4,800 orientations from [0 <= phi1 <= 2*pi, 0 <= Phi <= pi/2, 0 <= phi2 <= pi/3]. Each grain is randomly assigned an orientation.