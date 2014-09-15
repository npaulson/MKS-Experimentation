### Introduction

* This verification step was used to compare the elastic strain fields between Noah's and Matthew's simulations.
* The simulations should have exactly the same parameters

#### Main script:

	S1 = finite_element_grab_single.py


* This is the main script which reads a single .dat filename and calls from F1

#### Function script:

	F1 = function_load_fe_single.py :

* This script contains the functions necessary to read the .dat file.
* The functions in this script work for C3D8 element type outputs (8 nodes per element)
 