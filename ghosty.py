import numpy as np
import sys
import os
import code
import tifffile

#getting a weird error:
#File "ghosty.py", line 65, in main
#xScaled_Dim = getScaled(xdiff)
#File "ghosty.py", line 11, in getScaled
#value = value * scaleRatio
#NameError: global name 'scaleRatio' is not defined

#Scales data down so it can be loaded onto RAM
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



#inputs: CSV file to read, name of output file (optional), size of max image resolution, size of the dot [eg 1, 2, 3, 4]
#read frame number and group them by 1000's, make a tiff for each group


#not sure if there is a better way to do this maybe utilizng loops
#because this requires a set order for input
csv_input, out_file, MAX_IMG_RESOLUTION, dot_size, frame_num = sys.argv[1:6]

def main():

	with open(csv_input) as f:
		line=f.readline()


	header = line.strip().split(',')
	data = np.genfromtxt(csv_input, delimiter=",", skip_header=1)

	xs = makeMinZero(data[:, 15])
	ys = makeMinZero(data[:, 16])
	zs = makeMinZero(data[:, 17])



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


	arr = np.uint8(np.zeros((zScaled_Dim + 1, yScaled_Dim + 1, xScaled_Dim + 1)))

	if len(xs) != len(ys) or len(ys) != len(zs):
		print "length of x y and z not the same, bailing out"
		sys.exit(0)


	for index in range(len(xs)):
		if frame_num % 1000 == 0:
			break
		try:
			arr[getScaled(zs[index]), getScaled(ys[index]), getScaled(xs[index])] = 255
		except:
			print "array error"
			print index
			print getScaled(getScaled(zs[index]), getScaled(ys[index]), getScaled(xs[index]))
			code.interact(local=locals())

	out_file = out_file + str(frame_num)
	tifffile.imsave(out_file.tif, np.uint8(arr))



if __name__ == "__main__":
	main()
