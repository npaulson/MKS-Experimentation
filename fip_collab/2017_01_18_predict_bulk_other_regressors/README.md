NOTES:

* Neural Network regression: Poor CV error, poor predictive capability
* Ridge Regression: Ridge regression is just linear regression with regularization related to the L2 norm of the coefficients (regularization parameter alpha). Simplifies to linear regression for alpha=0
* Nearest neighbor regression: gives good values for cross-validation set but is not predictive for datapoints that are far from calibration points (as is the case for our validation set of MVEs)
* Support Vector Regression: gives good CV error and has good predictive capability. This is for a linear kernel with C=10 (penalty parameter for error term)
* Random Forest Regression: gives good CV error but poor predictive capability. This is for an ensemble of 100 estimators