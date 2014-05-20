MKS 1D README

Summary:
*	This project is a demonstration of the use of the Materials Knowledge System (MKS)
	for a 1D mechanics problem
*	This MKS analyses the strain throughout the length of a bar with a macroscopic applied strain.
*	The bar has a constant cross sectional area, but each segment may be assigned a material with a different 
	stiffness.


Files:
	mks1d.py
	fem1d.py
	find_independent.py

Steps:

*	The MKS generates a set of calibration 'microstructures.'
*	Each has a certain number of elements where each element is randomly assigned a material.
*	The finite element method (FEM) response for these 'microstructures' are calculated using fem1d.py
*	The microstructure function for each microstructure is generated
*	The MKS calibration is performed
*	A validation microstructure is generated in the same way as the calibration microstructures
*	The MKS calibration is used to predict the FEM response
*	The FEM response is calculated
*	The strain levels in each element for the MKS prediction and the FEM response are plotted together
