#

# RandNumGen_NmlDist.py

#

# Written by Matthew Priddy on January 12, 2012

#

# 

# The purpose of this code is to recreate pole figure data

#

# Specifically, this code will use a normal distribution 

# to select, at random, euler angles for a microstructure.

#

# The randomness of the number will be controlled with the mean and

# standard deviation for each normal distribution.

# 



from sys import *

from string import *

from math import *

from pylab import *

from random import *



f = 'Ti64_RandomMicroFZ_21x21x21_EulerAngles'



# 6 faces to the fundamental zone for hexagonal close-packed structures

# 0 <= phi1 <= 360

# 0 <= Phi  <= 90

# 0 <= phi2 <= 60



phi1_spacing = 10.0

phi0_spacing = 10.0

phi2_spacing = 10.0



phi1_number = int(360.0 / phi1_spacing)

phi0_number = int(90.0 / phi0_spacing)

phi2_number = int(60.0 / phi2_spacing)



phi1_FZ = []

phi0_FZ = []

phi2_FZ = []



# negative phi1-face

phi1 = 0.0

for i in range(phi0_number + 1):

	for j in range(phi2_number + 1):

		phi0 = float(i) * phi0_spacing

		phi2 = float(j) * phi2_spacing

		

		phi1_FZ.append(phi1)

		phi0_FZ.append(phi0)

		phi2_FZ.append(phi2)



# positive phi1-face

phi1 = 360.0

for i in range(phi0_number + 1):

	for j in range(phi2_number + 1):

		phi0 = float(i) * phi0_spacing

		phi2 = float(j) * phi2_spacing

		

		phi1_FZ.append(phi1)

		phi0_FZ.append(phi0)

		phi2_FZ.append(phi2)



# negative phi0-face

phi0 = 0.0

for i in range(phi1_number - 1):

	for j in range(phi2_number + 1):

		phi1 = phi1_spacing + float(i) * phi1_spacing

		phi2 = float(j) * phi2_spacing

		

		phi1_FZ.append(phi1)

		phi0_FZ.append(phi0)

		phi2_FZ.append(phi2)



# positive phi0-face

phi0 = 90.0

for i in range(phi1_number - 1):

	for j in range(phi2_number + 1):

		phi1 = phi1_spacing + float(i) * phi1_spacing

		phi2 = float(j) * phi2_spacing

		

		phi1_FZ.append(phi1)

		phi0_FZ.append(phi0)

		phi2_FZ.append(phi2)



# negative phi2-face

phi2 = 0.0

for i in range(phi1_number - 1):

	for j in range(phi0_number - 1):

		phi1 = phi1_spacing + float(i) * phi1_spacing

		phi0 = phi0_spacing + float(j) * phi0_spacing

		

		phi1_FZ.append(phi1)

		phi0_FZ.append(phi0)

		phi2_FZ.append(phi2)



# positive phi2-face

phi2 = 60.0

for i in range(phi1_number - 1):

	for j in range(phi0_number - 1):

		phi1 = phi1_spacing + float(i) * phi1_spacing

		phi0 = phi0_spacing + float(j) * phi0_spacing

		

		phi1_FZ.append(phi1)

		phi0_FZ.append(phi0)

		phi2_FZ.append(phi2)



for files in range(100):

	files = files + 1



# Some things we need to define for the code

# phi1 must be between 0 and 90 degrees (phi1)

# phi0 must be between 0 and 90 degrees (Phi)

# phi2 must be between 0 and 60 degrees (phi2)



	n = 21*21*21				# The number of grains 



	count1 = 0

	count2 = 0

	element = []

	phi1_list = []

	phi0_list = []

	phi2_list = []

	bins_list = []

#	element_bins_list = []

#	bins = [[[0 for k in range(12)] for j in range(18)] for i in range(18)]		

			

	i = 0

	for i in range(n):

		

		num = randint(0,len(phi1_FZ)-1)

		

		element.append(i)

		phi1_list.append(phi1_FZ[num])

		phi0_list.append(phi0_FZ[num])

		phi2_list.append(phi2_FZ[num])

		bins_list.append(num)



	print 'file number: ' + str(files)

					

	dataFileName = f + '_' + str(files).zfill(5) + '.txt'

	dataFile = open(dataFileName,'w')



	dataFile.write(dataFileName + '\n')

	dataFile.write('#element_id phi1 Phi phi2  bin\n')



	for i in range(len(element)):

		dataFile.write('%5d  % 3.6E  % 3.6E  % 3.6E  %5d\n'

		%(element[i]+1, phi1_list[i]*pi/180.0, phi0_list[i]*pi/180.0, phi2_list[i]*pi/180.0, bins_list[i]))



	dataFile.close()

	

"""		

		phi1_bin = int(phi1 // bin_size)

		phi0_bin = int(phi0 // bin_size)

		phi2_bin = int(phi2 // bin_size)

		bins[phi1_bin][phi0_bin][phi2_bin] = bins[phi1_bin][phi0_bin][phi2_bin] + 1

		bins_list.append(((phi0_bin) * 18) + (phi1_bin+1) + (phi2_bin*18*18))

		

	for i in range(18):

		for j in range(18):

			for k in range(12):

				if bins[i][j][k] == 0:

					count1 = count1 + 1

					angle = uniform(0.0, bin_size)

					phi1_insert = (i * bin_size) + angle

					phi0_insert = (j * bin_size) + angle

					phi2_insert = (k * bin_size) + angle

					while bins[i][j][k] == 0:

						ii = randint(0,17)

						jj = randint(0,17)

						kk = randint(0,11)

						if bins[ii][jj][kk] >= 3:

							number = (((jj) * 18) + (ii+1) + (kk*18*18))

							el_number = bins_list.index(number)

							phi1_list[el_number] = phi1_insert

							phi0_list[el_number] = phi0_insert

							phi2_list[el_number] = phi2_insert

							bins_list[el_number] = ((j) * 18) + (i+1) + (k*18*18)

							bins[i][j][k] = bins[i][j][k] + 1

							bins[ii][jj][kk] = bins[ii][jj][kk] - 1



	for i in range(18):

		for j in range(18):

			for k in range(12):

				if bins[i][j][k] == 0:

					count2 = count2 + 1



#	print shape(bins)

#	print count1

#	print count2

"""