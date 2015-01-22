---
layout: post
title: MKS for Plastic Deformation of a 2 Phase Composite
author: Noah Paulson

latex: true

composite_plastic_error_chart:
  type: img
  src: https://farm8.staticflickr.com/7534/16271592215_29ea06464f_o.png
  
slice_50cal_10val:
  type: img
  src: https://farm8.staticflickr.com/7536/16084026440_943e1b4839_b.jpg

---

## Introduction

The purpose of this study was to investigate the prediction of total strain using the MKS framework. Two - phase composite microstructures with isotropic phases were chosen to simplify the problem. The goal was to calibrate with plastic FEM simulations and predict the total strain at each voxel location (elastic strain + plastic strain). 

## Parameters
* 2 phase microstructures with isotropic phases
* Both phases exhibit elastic, perfectly plastic behavior
* 0.15% applied strain amplitude

#### Phase 1 Parameters:
* Young's Modulus: 100 GPa
* Poisson's Ratio: 0.3
* Yield Strength: 100 MPa

#### Phase 2 Parameters:
* Young's Modulus: 100 GPa
* Poisson's Ratio: 0.3
* Yield Strength: 125 MPa

#### Calibration Set:
* 50% volume fraction
* 50 random microstructures

#### Validation Sets:
* 3 sets: 30% VF, 50% VF, 70% VF
* 10 random microstructures in each set 

## Results

_The following chart shows the errors seen in the 10 validation microstructures_

{% include ContentManager.html content=page.composite_plastic_error_chart %}

* Mean % Error: mean error per voxel in all microstructures  
* Average Maximum % Error: max error per microstructure 
* Absolute Maximum % Error: max error in any microstructure 

_The following image compares a slice of a strain field for a 50% VF validation microstructure between the MKS and FEM_

{% include ContentManager.html content=page.slice_50cal_10val %}

* S.R. Kalidindi, S.R. Niezgoda, G. Landi, S. Vachhani, T. Fast _A Novel Framework for Building Materials Knowledge Systems_ CMC 17 (2010) 103-125
