import numpy as np
import sys
import os
import code
import tifffile

MAX_IMG_RESOLUTION = 2000


with open('ROI2.csv') as f:
    line=f.readline()


header = line.strip().split(',')
data = np.genfromtxt('ROI2.csv', delimiter=",", skip_header=1)

xs = data[:, 15]
ys = data[:, 16]
zs = data[:, 17]
xdiff = max(xs) - min(xs)
ydiff = max(ys) - min(ys)
zdiff = max(zs) - min(zs)

print "dimensions: " + str(xdiff) + ", " + str(ydiff) + ", " + str(zdiff)

dim = [xdiff, ydiff, zdiff]

maxDim = max(dim)
print(maxDim)

scaleRatio = MAX_IMG_RESOLUTION / maxDim


xOut = xdiff * scaleRatio
yOut = ydiff * scaleRatio
zOut = zdiff * scaleRatio


xOut = int(xOut)
yOut = int(yOut)
zOut = int(zOut)

print(xOut,yOut,zOut)

#For some reason it gave me an index error here so when I casted the values
#as ints it worked great. Not sure if its okay to cast as int or not,
#but it worked :)
arr = np.zeros((xOut,yOut,zOut))

print(arr)

tifffile.imsave('nameOfFile.tif', arr)

code.interact(local=locals())
