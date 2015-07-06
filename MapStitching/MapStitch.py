from cv2 import *
from cv import *

import numpy as np
##Import the two overlapping images. 
firstTile = 'DJI00289.jpg'
firstTile = imread(firstTile)

secondTile = 'DJI00290.jpg'
secondTile = imread(secondTile)

H,W, c = firstTile.shape


#template = firstTile.crop((0,0,tempSize[0], 800))
template = firstTile[0:800, 0:H]

#window = cv.NamedWindow('template')
#imshow(window, template) ##Debugging template 
#
#raw_input('Good?')
#destroyAllWindows()

h,w,c = secondTile.shape


result = (W-w+1)*(H-h+1)

#
#dest = cv.CreateMat(H,W, cv.CV_32FC1)
#src = cv.fromarray(secondTile)
#cv.Convert(src, dest)

secondTile = imread('DJI00290.jpg')

matches = matchTemplate(secondTile, template, 1)

bestMatch = np.unravel_index(matches.argmin(), matches.shape)

