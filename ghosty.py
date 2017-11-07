import numpy as np
import sys
import os
import code
import tifffile

def getScaled(value, scaleRatio):
	value = value * scaleRatio
	return int(value)

#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------

def makeMinZero(arr):
	minVal = min(arr)
	if minVal < 0:
		arr = [int(i + abs(minVal)) for i in arr]
	else:
		arr = [int(i - minVal) for i in arr]
	return np.asarray(arr)

#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------

def importData(csv_input, maxResolution):
	with open(csv_input) as f:
		line=f.readline()

	header = line.strip().split(',')
	data = np.genfromtxt(csv_input, delimiter=",", skip_header=1)

	frameID = np.asarray(data[:,0])
	xs = makeMinZero(data[:, 15])
	ys = makeMinZero(data[:, 16])
	zs = makeMinZero(data[:, 17])
	
	if len(xs) != len(ys) or len(ys) != len(zs):
		print("length of x y and z not the same, bailing out")
		sys.exit(0)

	xdiff = max(xs) - min(xs)
	ydiff = max(ys) - min(ys)
	zdiff = max(zs) - min(zs)

	print("Actual dimensions: " + str(xdiff) + ", " + str(ydiff) + ", " + str(zdiff))

	dim = [xdiff, ydiff, zdiff]
	maxDim = max(dim)
	scaleRatio = maxResolution / float(maxDim)

	xScaled_Dim = getScaled(xdiff, scaleRatio)
	yScaled_Dim = getScaled(ydiff, scaleRatio)
	zScaled_Dim = getScaled(zdiff, scaleRatio)

	print("Scale ratio: " + str(scaleRatio))
	print("Scaled dimensions: " + str(xScaled_Dim) + ", " + str(yScaled_Dim) + ", " + str(zScaled_Dim))
	
	tiffDimensions = (zScaled_Dim + 1, yScaled_Dim + 1, xScaled_Dim + 1)
	scaledData = (frameID, xs * scaleRatio, ys * scaleRatio, zs * scaleRatio)

	return tiffDimensions, scaledData

#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------

def writeTIFFs(scaledData, tiffDimensions, numberOfStacks, radius, outDir):
	frameID = scaledData[0]
	scaledX = scaledData[1]
	scaledY = scaledData[2]
	scaledZ = scaledData[3]
	
	numberOfPoints = scaledX.shape[0]
	numberOfFrames = np.max(frameID)
	
	stackBinSize = int(numberOfPoints / numberOfStacks)
	
	index = 0
	
	for frameNumber in range(numberOfStacks):
		
		print("Writing tiff number: " + str(frameNumber))
		arr = np.zeros((tiffDimensions[0], tiffDimensions[1], tiffDimensions[2]))
		
		while True:
			for shiftx in range(-radius,radius):
				for shifty in range(-radius,radius):
					for shiftz in range(-radius,radius):
						try:
							proximityToRadius = float(abs(shiftz) + abs(shifty) + abs(shiftx)) / float(radius*3)
							value = 1.0 - proximityToRadius
							arr[int(scaledZ[index]) + shiftz, int(scaledY[index]) + shifty, int(scaledX[index]) + shiftx] += value
							#arr[int(scaledZ[index]), int(scaledY[index]), int(scaledX[index])] = 255
						except:
							continue
			index += 1
			if (index % 10000 == 0.0):
				print(index)
			if index >= numberOfPoints:
				arr *= 255.0/arr.max()
				outPath = outDir + str(frameNumber).zfill(4) + ".tiff"
				tifffile.imsave(outPath, np.uint8(arr))
				return
			if (index % stackBinSize == 0.0):
				break
		
		#code.interact(local=dict(globals(), **locals())) 
		arr *= 255.0/arr.max()
		outPath = outDir + str(frameNumber).zfill(4) + ".tiff"
		tifffile.imsave(outPath, np.uint8(arr))


#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------

def main():
#code.interact(local=dict(globals(), **locals())) 
	print("------------------------------------------------------------------------------------------------")
	print("------------------------------------------------------------------------------------------------")
	print("Ghosty.py -- a system for converting sparse 3D Molecular localization data to dense TIFF stacks")
	print("Written by Michael Morehead [mmorehea@mix.wvu.edu] and Drew Scatterday [drewscatterday@gmail.com] ")
	print("Usage: python ghosty.py [path/to/csv/] [path/to/out/] [max image resolution] [radius of dot] [number of TIFFs to produce]")
	print("------------------------------------------------------------------------------------------------")
	print("------------------------------------------------------------------------------------------------")
	
	if len(sys.argv) < 4:
		print("Not enough input parameters, please follow usage guide!")
		sys.exit()
	
	csvInput = sys.argv[1]
	outDir = sys.argv[2]
	maxResolution = int(sys.argv[3])
	radius = int(sys.argv[4])
	numberOfStacks = int(sys.argv[5])
	
	print("Importing data...")
	tiffDimensions, scaledData = importData(csvInput, maxResolution)
	print("Writing tiffs...")
	writeTIFFs(scaledData, tiffDimensions, numberOfStacks, radius, outDir)
	print("Done!")

#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------

if __name__ == "__main__":
	main()
