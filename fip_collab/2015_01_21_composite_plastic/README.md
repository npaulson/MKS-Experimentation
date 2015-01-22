## MKS Details

* Indicator basis
* 2-phases
* only 1st order terms in MKS expansion

## Simulation Details

* 3d
* 21 elements per side
* isotropic phases
* elastic perfectly plastic material behavior
* rate independent

* total applied strain = 0.001125
* mean plastic strain = 7.12E-5
* max plastic strain ~ 0.0002
* standard deviation of plastic strain = 6.96E-5

In this simulation only the soft phase reaches yield. This is an expected result.

phase1:

* Young's Modulus = 100
* Poisson's Ratio = 0.3
* Yield Strength = .100 

phase2:

* Young's Modulus = 100
* Poisson's Ratio = 0.3
* Yield Strength = .125

### Trial 50 cal, 10 val

* Calibration
	* 50 microstructures
	* 50% VF
* Validation
	* 10 microstructures
	* 50% VF

### Trial 100 cal50pc, 50 val50pc	 

* Calibration
	* 100 microstructures
	* 50% VF
* Validation
	* 50 microstructures
	* 50% VF

### Trial 100 calRpc, 50 val50pc

* Calibration
	* 100 microstructures
	* 1-99% VF
* Validation
	* 50 microstructures
	* 50% VF

### Trial 100 cal50pc, 50 valRpc

* Calibration
	* 100 microstructures
	* 50% VF
* Validation
	* 50 microstructures
	* 1-99% VF

### Trial 100 calRpc, 50 valRpc

* Calibration
	* 100 microstructures
	* 1-99% VF
* Validation
	* 50 microstructures
	* 1-99% VF