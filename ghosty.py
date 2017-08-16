import numpy as np
import sys
import os
import code
import tifffile

MAX_IMG_RESOLUTION = 500.0


#keep methods near top
def getScaled( value ):
	value = value * scaleRatio
	return int(value)

def makeMinZero(arr):
	minVal = min(arr)
	if minVal < 0:
		arr = [int(i + abs(minVal)) for i in arr]
	else:
		arr = [int(i - minVal) for i in arr]
	return arr


#should read a file, not hardcoded
#utilize sys.argv

#inputs: CSV file to read, name of output file (optional), size of max image resolution, size of the dot [eg 1, 2, 3, 4]
#read frame number and group them by 1000's, make a tiff for each group
def main():

	with open('ROI2.csv') as f:
		line=f.readline()


	header = line.strip().split(',')
	data = np.genfromtxt('ROI2.csv', delimiter=",", skip_header=1)

	xs = makeMinZero(data[:, 15])
	ys = makeMinZero(data[:, 16])
	zs = makeMinZero(data[:, 17])



	#zs has negative numbers in it. if any coordinate has negative numbers, it needs to be reset so the lowest number is 0. also make it all ints


	xdiff = max(xs) - min(xs)
	ydiff = max(ys) - min(ys)
	zdiff = max(zs) - min(zs)



	print "Actual dimensions: " + str(xdiff) + ", " + str(ydiff) + ", " + str(zdiff)

	dim = [xdiff, ydiff, zdiff]

	maxDim = max(dim)

	scaleRatio = MAX_IMG_RESOLUTION / float(maxDim)


	xScaled_Dim = getScaled(xdiff)
	yScaled_Dim = getScaled(ydiff)
	zScaled_Dim = getScaled(zdiff)


	xScaled_Dim = int(xScaled_Dim)
	yScaled_Dim = int(yScaled_Dim)
	zScaled_Dim = int(zScaled_Dim)

	print("Scale ratio: " + str(scaleRatio))
	print "Scaled dimensions: " + str(xScaled_Dim) + ", " + str(yScaled_Dim) + ", " + str(zScaled_Dim)

	#For some reason it gave me an index error here so when I casted the values
	#as ints it worked great. Not sure if its okay to cast as int or not,
	#but it worked :)
	arr = np.uint8(np.zeros((zScaled_Dim + 1,yScaled_Dim + 1, xScaled_Dim + 1)))

	#this scales all the coordinates of the data down to the desired amount
	#to load onto the RAM
	#xs_Scaled = xs * scaleRatio
	#ys_Scaled = ys * scaleRatio
	#zs_Scaled = zs * scaleRatio

	#please use TABS, not spaces
	#GREAT GOOD START
	#this is how I'd do it:
	if len(xs) != len(ys) or len(ys) != len(zs):
		print "length of x y and z not the same, bailing out"
		sys.exit(0)


	for index in range(len(xs)):
		#if index % 1000 == 0:
		#print str(index) + " / " + str(len(xs))
		try:
			arr[getScaled(zs[index]), getScaled(ys[index]), getScaled(xs[index])] = 255
		except:
			print "array error"
			print index
			print getScaled(getScaled(zs[index]), getScaled(ys[index]), getScaled(xs[index]))
			code.interact(local=locals())
	#gave me an error for too many values to unpack
	# for px,py,pz in xs_Scaled,ys_Scaled,zs_Scaled:
	#     # px = int(px)
	#     # py = int(py)
	#     # pz = int(pz)
	#     arr[px,py,pz] = 1
	#

	#IndexError: only integers, slices (`:`), ellipsis (`...`), numpy.newaxis (`None`)
	#and integer or boolean arrays are valid indices
	# for px,py,pz in zip(xs_Scaled,ys_Scaled,zs_Scaled):
	#     # px = int(px)
	#     # py = int(py)
	#     # pz = int(pz)
	#     arr[px,py,pz] = 1
	#

	#IndexError: only integers, slices (`:`), ellipsis (`...`), numpy.newaxis (`None`)
	#and integer or boolean arrays are valid indices
	# for px in xs_Scaled:
	#     for py in ys_Scaled:
	#         for pz in zs_Scaled:
	#             arr[px,py,pz] = 1
	#

	#I was curious if this would work, making a new 3D array with all the
	#scaled down x,y,z coorinates. Then saying wherever the zeros array has
	#these scaled x,y, and z position, make that value 1 but again
	#it gave me a value error:
	#"ValueError: too many values to unpack"

	# scl_arr = np.array((xs_Scaled,ys_Scaled,zs_Scaled))
	#
	# for px,py,pz in scl_arr:
	#     arr[px,py,pz] = 1
	#

	#I feel like I'm missing something so simple and it is bothering the heck out of me

	tifffile.imsave('ghostyOutput.tif', np.uint8(arr))



if __name__ == "__main__":
	main()
