import ImageFilter
import numpy
from PIL import Image
from PIL import ImageStat
from colorsys import * 


#Extract all nxn rectangles from an image (these will be processed then used as inputs for ML algorithm). 
def getSub(n, imageName): 
    """Takes in n, an integer less than or equal to the minimum dimension of the image 
       and imageName, the string containing the name of the image to be processed.  
       Returns a list of all nxn subrectangles of image.""" 
    image = Image.open(imageName) #load in the image.
    #Find the size of the image. 
    size = image.size
 #   print(size)
    width = size[0] #pull out length and width 
    length = size[1] 
    subList = []
    #Faster way to do this? Might take awhile when our image is really large (i.e. entire map 
    #especially with small n values... 
    for i in range(0,width - n+1, int(0.1*n)): #Go through the entire image 
        for j in range(0, length - n+1, int(0.1*n)): 
            box = (i,j,i+n, j+n)  #edge coordinates of the next rectangle. 
            newImage = image.crop(box) #pull out the desired rectangle
            subList += [newImage] #More efficient way to store each image? 
            ##Add in metric calculations here - don't need to store 
    return subList #return a list of images (use image.show() to display). 
    

#Start of helper functions for computing metrics. 
    
def colorAvg(imageName): 
    """Takes in a string containing an image file name, returns the average red, blue, and green 
        values for all the pixels in that image.""" 
    im = Image.open(imageName) 
    imStats = ImageStat.Stat(im) 
    (redAv, greenAv, blueAv) = imStats.mean
    return redAv, greenAv, blueAv
    
    

  #rgb_to_hsv(r,g,b)  converts pixel coords to HSV coords 
  
   
def findYellow(imageName): 
    """counts the number of yellow pixels in the given image.""" 
    im = Image.open(imageName)
    pix = im.load() #load in pixel array  
    #define HSV value ranges for yellow  
    #for now just base of Hue - refine for actual yellows seen in field? 
    minHue = 50/360.
    maxHue = 61/360.
    width, height = im.size  #find the size of the image 
    count = 0 #initialize a counter for yellow pixels.  
    for i in range(width): 
        for j in range(height): 
            (r,g,b) = pix[i,j] #pull out the current r,g,b values 
            (h,s,v) = rgb_to_hsv(r/255.,g/255.,b/255.) 
            if minHue<=h and h<maxHue: 
                count += 1 #add one to the count 
    totalPix = width*height 
    portion = float(count)/totalPix
    #print(portion)
    return portion
    
def colorVariance(imageName):
    ''' calculates the diversity in color using a hue histogram'''
    
    # load image pixels
    im = Image.open(imageName)
    pix = im.load()
    width, height = im.size
    
    # create empty histogram to be filled with frequencies
    histogram = [0]*360
    pixelHue = 0
    for i in range(width):
        for j in range(height):
            (r,g,b) = pix[i,j] #pull out the current r,g,b values 
            (h,s,v) = rgb_to_hsv(r/255.,g/255.,b/255.)
            pixelHue = int(360*h)
            #build histogram
            histogram[pixelHue] += 1
    print histogram
    # calculate standard deviation of histogram
    return numpy.std(histogram)
        
    
      
def countEdgePixels(imageName):
    ''' counts the number of pixels that make up the edges of features'''
    # define threshold for edges
    threshold = 150 
    
    # open image and filter
    im = Image.open(imageName)
    im2 = im.filter(ImageFilter.FIND_EDGES)
    im2.save("Filtered.jpg")
    im2 = im2.convert("L")
	
    # load pixels and count edge pixels
    pix = im2.load()
    pixels = 0
    for x in range(0,im.size[0]):
        for y in range(0, im.size[1]):
            if pix[x,y] > threshold:
                pixels += 1

    return float(pixels) / (im.size[0]*im.size[1])
