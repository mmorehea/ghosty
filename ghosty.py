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



arr = np.zeros((xOut,yOut,zOut))

tifffile.imsave('nameOfFile.tif', arr)

code.interact(local=locals())

