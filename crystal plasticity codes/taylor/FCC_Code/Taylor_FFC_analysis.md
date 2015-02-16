## Main Code

### L878: Program Main

The following files are opened and the contents will be replaced:

* open **s##** files (what are these?)
* open **crystalstresses.txt** file
* open **texture.out** file
* open **wstar.txt**
* open **Hamad_test.txt**

the following files are opened

* open **errorfile**
* open **ept.res**
* open **ept.res0**


define **IC**, **ALPHA**, **PI**  (what are **IC**, **ALPHA**?)

define **FTHETA** (what is **FTHETA**)

define **Theta_Flag** 

if **Theta_Flag** = 1 then **FTHETA** is in degree units

L937: Call **INPUT** subroutine

L939: Call **INITIALIZE(IC)**

if **Theta_Flag** isn't 1 then notify user the values of **LFLAG** and **QFAC**

assign **TEX** to **TEXFLAG**, and **TAUTO** to **OUTFLAG**

start the time loop

if **TIME** is equal to **TTIME** (the total simulation time) go to **300** ???

set **TAU** to **TIME** (current time) + **DTIME** (timestep)

if **TAU** is greater than **TTIME** set **TAU** equal to **TTIME** and set **DTIME** to **TAU** minus **TIME**

Next we want to get the deformation gradient at **TAU** in global coordinates

L969: start loop over all the crystals (1 to **NCRYS**), for each crystal do the following:

L971: call **DEFGRAD(ICRYS)** to provide the deformation gradient tensor, **FTAU** at the end of the current timestep

L975: call **TRSTRESS(ICRYS)** to compute the trial stress **TBTR**

## Subroutines

### L267: DEFGRAD(ICRYS)

The formulations of each deformation gradient tensor are defined in this subroutine

include  **commonsn.tex**

define **FSB**, **FSB1**, **TMP1** and **ROT** as [3,3] arrays

set **FTTAU** to **ONET** (the [3,3] identity tensor)

based on **LFLAG** and **EDOT** in the input file **temptay.inp**, assign **FTTAU** the associated deformation gradients.

### L521: FORMSP(ICRYS)

Define SMATG and PMATG from the original slip systems and crystal orientations from the **fcc12** and **euler.inp** files

include 'commonsn.tex'

first we initialize a loop I = 1 to 12 for FCC (change this to take in **NSLIP** for consistency)

calculate tensor **TMP** = dot(**SMAT(:, :, I)**, **QT(:, :, I)**)

calculate tensor **SMATG** = dot(**QMAT**, **TMP**)

therefore **SMATG** is **SMAT** taken from crystal to sample frame

define **PMAT** as the vector form of **SMATG**. The off-diagonal terms of **SMATG** are doubled so that **PMAT** can be dotted with the vector form of stress


### L841: INPUT

includes **commonsn.tex**

This subroutine reads **temptay.inp** to pull out the values for the variables defined by the user: **C11**, **C12**, **C44**, **LFLAG**, **EDOT**, **QFAC**, **TTIME**, **DTIME**, **TAUTO**, **DTMAX**, **GDO**, **XM**, **OUT**, **TEX**, **HO**, **SO**, **SS**, **AEXP**, **QL**, **SEXP**

### L608: INITIALIZE

includes **commonsn.tex**

open files **euler.inp** and **fcc12** (to read)

initialize constants **ZERO**, **TINY**, **ONE**, **TWO**, **THREE**, **FOUR**, **HALF**, **THIRD**, **PI**

initialize variable **TIME**

initialize  **ONET** and **ONES**

initialize **DELTA**

initialize **FT** as **ONES** (3x3 identity) if new run. If continuing from previous run assign it from "16" (what is 16?)

read first line of **fcc12** to find number of slip systems (**NSLIP**)

read in the slip planes (**AM**) and slip directions (**AN**) from **fcc12**

generate the **SMAT** array: loop from 1 to **NSLIP**. Make **AM** and **AN** into unit vectors. For each slip system take the outer product of the normalized **AM** and **AN**  

define **RADDEG**

assign the value from the first line of **euler.inp** to **NCRYS** (total # crystals)

read the bunge euler angles from **euler.inp**, convert to Canova angles and save to **TH(ICRYS)**, **PHI(ICRYS)** and **OM(ICRYS)** 

initialize **wstar** and **NSB** with zeros

call **ROTMAT**: obtain transformation matrix and store for use in the final texture calculation (**QMAT** and **QT**)

call **FORMSP**: compute **SMATG** and **PMAT** for crystal in sample frame

initialize PK2 stress (**TBTMAT**) at zero or read from restart file

initialize the inverse of the plastic deformation gradient (**FPTINV**) as identity matrix for all crystals or read from restart file

initialize **ACCGAM** at 0

initialize all slip resistances in **CRSS** at **SO** or read from restart file

for each combination of slip systems initialize **QLAT** to **QL**, then, for co-planar sets of slip systems set this ratio to **ONE**

write headers in the stress output files

### L1472: ROTMAT

include **commonsn.tex**

calculate sine and cosine of **OM**, **PHI**, **TH** vectors 

calculate **QMAT** rotation matrices out of the Canova Euler angles for each crystal

transpose **QMAT** to make **QT**

### L1581: TRSTRESS(ICRYS)

define [3,3,12] arrays **BALPHA**, **CALPHA** and **TMP1**

define [3,3] arrays **TMP2**, **TMP3**, **TC**, and **EC**

compute the tensor quantity **A** (Kalidindi, 1992. pg. 544):

L1593 **TMP3** = dot(transpose(**FTAU**),**FTAU**)

L1623 **TMP2** = dot(**TMP3**,**FPTINV(:,:,ICRYS)**)

L1653 **A(:,:,ICRYS)** = dot(transpose(**FPTINV(:,:,ICRYS)**),**TMP2**)

in summary, **A** = transpose(**FPTINV**) {dot} transpose(**FTAU**) {dot} **FTAU** {dot} **FPTINV**

compute  **TBTR** (Kalidindi, 1992. pg. 544):

redefine **TMP2** = **A** - **ONET**

redefine **TMP3** = dot(**QT(:,:,ICRYS)**,**TMP2**)

**EC** = dot(**TMP3**,**QMAT(:,:,ICRYS)**)

**TC** = 0.5 x (**L** {dot} **EC**) where in the code the matrix form of **L** is used with **C11**, **C12** and **C44**. **TC** is "T-star trial** in the paper.

redefine **TMP2** = **QMAT(:,:,ICRYS)** <dot> **TC**

**TBTR(:,:,ICRYS)** = **TMP2** {dot} **QT(:,:,ICRYS)**


## Glossary:

* **A**: [3,3,**NCRYS**] array of tensors A for crystal (Kalidindi, 1992. pg. 544)
* **ACCGAM**: [**NSLIP**, **NCRYS**] array of ???
* **AEXP**: slip hardening parameter, identical for all systems, defined in **temptay.inp**
* **AM**: [**NSLIP**,3] array of slip planes
* **AN**: [**NSLIP**,3] array of slip directions
* **CRSS**: [**NSLIP**, **NCRYS**] array of slip system resistances for all crystals
* **DELTA**: 6 element vector of unique components of 3x3 identity matrix
* **DTIME**: The length of the timestep. The initial timestep is defined in **temptay.inp**
* **DTMAX**: maximum timestep in numerical integration, defined in **temptay.inp**
* **EDOT**: applied strain rate in **temptay.inp**
* **FOUR**: 4.0
* **FPTINV**: [3,3,**NCRYS**] array of the inverse of plastic deformation gradient and beginning of time step for all crystals
* **FT**: [3,3] Deformation gradient in initial configuration
* **TTTAU**: [3,3] Deformation gradient tensor at time Tau???
* **GDO**: reference strain rate, defined in **temptay.inp**
* **HALF**: **ONE**/**TWO**
* **HO**: slip hardening parameter, identical for all systems, defined in **temptay.inp**
* **L**: elastic stiffness tensor 
* **LFLAG**: ID of deformation type in **temptay.inp**
* **NCRYS**: number of crystals in simulation
* **NSB**: [**NCRYS**] vector of ??
* **NSLIP**: number of slip systems
* **OM**: [ICRYS] vector of third Canova angle in radians
* **ONE**: 1.0
* **ONES**: [6,6] identity matrix
* **ONET**: [3,3] identity matrix
* **OUT**: results output frequency, defined in **temptay.inp**
* **PHI**: [ICRYS] vector of second Canova angle in radians
* **PI**: **FOUR** x atan(**ONE**)
* **PMAT**: vector form of **SMATG** where the off-diagonal components are doubled
* **RADDEG**: **PI**/180.0
* **QFAC**: ??? defined in **temptay.inp**
* **QL**: ??? hardening parameter, defined in **temptay.inp**
* **QLAT**: [**NSLIP**, **NSLIP**] ratio of latent hardening rate to self-hardening rate
* **QMAT**: [3,3,**NCRYS**] array of rotation matrices for each crystal
* **QT**: [3,3,**NCRYS**] array, transpose of **QMAT**
* **SEXP**: ??? hardening parameter, defined in **temptay.inp**
* **SMAT**: [3,3,**NSLIP**] array storing S_o^alpha for the crystal (outer product of **AM** and **AN** for each slip system)
* **SMATG**: [3,3,**NSLIP**,**NCRYS**] array containing S_o^alpha in sample frame
* **SO**: initial slip resistance value
* **SS**: saturation value for slip hardening, defined in **temptay.inp**
* **TAUTO (OUTFLAG)**: duration before automatic time steps, defined in **temptay.inp**
* **TBTMAT**: [3,3,**ICRYS**] array containing second PK stress (in relaxed configuration) at beginning timestep for all crystals
* **TEX (TEXFLAG)**: texture output frequency, defined in **temptay.inp**
* **TH**: [ICRYS] vector of first Canova angle in radians
* **THIRD**: **ONE**/**THREE**
* **THREE**: 3.0
* **TINY**: 1.0E-10
* **TTIME**: total simulation time, defined in **temptay.inp**
* **TWO**: 2.0
* **wstar**: [3,**NCRYS**] array ???
* **XM**: rate sensitivity, defined in **temptay.inp**
* **ZERO**: 0.0