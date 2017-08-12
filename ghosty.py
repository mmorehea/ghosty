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

print "Actual dimensions: " + str(xdiff) + ", " + str(ydiff) + ", " + str(zdiff)

dim = [xdiff, ydiff, zdiff]

maxDim = max(dim)

scaleRatio = MAX_IMG_RESOLUTION / maxDim


xScaled_Dim = xdiff * scaleRatio
yScaled_Dim = ydiff * scaleRatio
zScaled_Dim = zdiff * scaleRatio

def getScaled( value ):
    value = value * scaleRatio
    return value


xScaled_Dim = int(xScaled_Dim)
yScaled_Dim = int(yScaled_Dim)
zScaled_Dim = int(zScaled_Dim)

print("Scale ratio: " + str(scaleRatio))
print "Scaled dimensions: " + str(xScaled_Dim) + ", " + str(yScaled_Dim) + ", " + str(zScaled_Dim)

#For some reason it gave me an index error here so when I casted the values
#as ints it worked great. Not sure if its okay to cast as int or not,
#but it worked :)
arr = np.zeros((xScaled_Dim,yScaled_Dim,zScaled_Dim))

#this scales all the coordinates of the data down to the desired amount
#to load onto the RAM
xs_Scaled = xs * scaleRatio
ys_Scaled = ys * scaleRatio
zs_Scaled = zs * scaleRatio


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

tifffile.imsave('ghostyOutput.tif', arr)

code.interact(local=locals())
