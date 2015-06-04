import ImageFilter
import numpy
from PIL import Image
from PIL import ImageStat
from colorsys import * 
import time


#Extract all nxn rectangles from an image (these will be processed then used as inputs for ML algorithm). 
def getSub(n, imageName): 
    """Takes in n, an integer less than or equal to the minimum dimension of the image 
       and imageName, the string containing the name of the image to be processed.  
       Returns a list of all nxn subrectangles of image.""" 
    # define overlap percentage for sub images
    overlap = 0.1
       
    image = Image.open(imageName) #load in the image.
    #Find the size of the image. 
    size = image.size
 #  print(size)
    width = size[0] #pull out length and width 
    length = size[1] 
   # subList = []
   #Initialize lists to hold metric results (for analysis later to test) 
    avgList = [] 
    avgTimeL = []
    yellowList = [] 
    yellowTimeL = []
    varList = [] 
    varTimeL = []
    edgeList = [] 
    edgeTimeL = []
    textList = []
    textTimeL = []
    
    # Extract all tiles using a specific overlap (overlap depends on n)
    for i in range(0,width - n+1, int(overlap*n)): #Go through the entire image 
        for j in range(0, length - n+1, int(overlap*n)): 
            box = (i,j,i+n, j+n)  #edge coordinates of the next rectangle. 
            newImage = image.crop(box) #pull out the desired rectangle
            #subList += [newImage] #More efficient way to store each image? 
            ##Add in metric calculations here - don't need to store 
            ###TEMPORARY METRIC CALCULATIONS 
            start = time.time()
            avg = colorAvg(newImage) 
            avgTime = time.time() - start 
            avgTimeL += [avgTime]
           
            yellow = findYellowFast(newImage)
            yellowTime = time.time() - avgTime - start
            yellowTimeL += [yellowTime]
         
            var = colorVariance(newImage) 
            varTime = time.time() - yellowTime - start
            varTimeL += [varTime]
         
            edges = countEdgePixels(newImage)
            edgeTime = time.time() - varTime - start
            edgeTimeL += [edgeTime]
           
            texture = textureAnalysis(newImage) 
            textTime = time.time() - edgeTime - start
            textTimeL += [textTime]
      
            
            avgList += [avg] 
            yellowList += [yellow] 
            varList += [var] 
            edgeList += [edges]
            textList += [texture]
            
    return avgList, yellowList, varList, edgeList, textList, avgTimeL, yellowTimeL, varTimeL, edgeTimeL, textTimeL
   ## return subList #return a list of images (use image.show() to display). 
    

#Start of helper functions for computing metrics. 
    
def colorAvg(imageName): 
    """Takes in a string containing an image file name, returns the average red, blue, and green 
        values for all the pixels in that image.""" 
    im = Image.open(imageName) 
    imStats = ImageStat.Stat(im) 
    (redAv, greenAv, blueAv) = imStats.mean
    return redAv, greenAv, blueAv
    
    

  #rgb_to_hsv(r/255.,g/255.,b/255.)  converts pixel coords to HSV coords 
  
   
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

def textureAnalysis(imageName):
    ''' determines the proportion of small grids that have distinct texture'''
    # define texture threshold and grid size
    threshold = 100
    n = 5
    
    # open image
    im = Image.open(imageName)
    width, height = im.size
    
    # loop across image
    count = 0
    for i in range(0,width-n,n):
        for j in range(0,height-n,n):
            
            # divide into small grids
            box = (i,j,i+n,j+n)
            imTemp = im.crop(box)
            
            # calculate intensity from RGB data
            rImage, gImage, bImage = imTemp.split()
            rData = list(rImage.getdata())
            gData = list(rImage.getdata())
            bData = list(rImage.getdata())
            intensity =  [rData[i]+gData[i]+bData[i] for i in range(len(rData))]
            
            # count as high texture if difference in intensity is 
            # greater than threshold
            if ((max(intensity) - min(intensity)) > threshold):
                count += 1
                
    # calculate the percentage of high texture grids
    return float(count)/((width/n)*(height/n))
    
def findYellowFast(im): 
    """counts the number of yellow pixels in the given image.""" 
 #   im = Image.open(imageName)
    #define HSV value ranges for yellow  
    #for now just base of Hue - refine for actual yellows seen in field? 
    minHue = 55/360.
    maxHue = 70/360.
    
    minSat = 0.15 
   # maxSat = 0.4
   
    minV = 0.5
    
    
    width, height = im.size  #find the size of the image 
    count = 0 #initialize a counter for yellow pixels.  
    rgbList = list(im.getdata())
    hsvList = map(getHSV, rgbList)
    for (h,s,v) in hsvList: 
        if minHue <h and h<maxHue and minSat<s and minV<v: 
            count += 1
    totalPix = width*height 
    portion = float(count)/totalPix
    #print(portion)
    return portion
def getHSV((r,g,b)): 
    return rgb_to_hsv(r/255., g/255., b/255.)
    
def analysis(avg, yellow, var, edges, texture): 
    """analyze things to check if they work""" 
    r = [a[0] for a in avg]
    ravg = numpy.mean(r)
    rmin = min(r) 
    rmax = max(r)
    g = [a[1] for a in avg]
    gavg = numpy.mean(g)
    gmin = min(g) 
    gmax = max(g)
    b = [a[2] for a in avg]
    bavg = numpy.mean(b)
    bmin = min(b) 
    bmax = max(b)
    
    
    print('Red Statistics') 
    print('Average is ', ravg) 
    print('Min is ', rmin)
    print('Max is ', rmax)
    
    print('Green Statistics') 
    print('Average is ', gavg) 
    print('Min is ', gmin)
    print('Max is ', gmax)
    
    print('Blue Statistics') 
    print('Average is ', bavg) 
    print('Min is ', bmin)
    print('Max is ', bmax)
    
    
    yavg = numpy.mean(yellow)
    ymin = min(yellow)
    ymax = max(yellow)
    
    print 'Yellow Statistics' 
    print 'Average is ', yavg 
    print 'Min is ', ymin 
    print 'Max is ', ymax
    
    vavg = numpy.mean(var)
    vmin= min(var)
    vmax = max(var) 
    
    print 'Color Variance Statistics' 
    print 'Average is ', vavg 
    print 'Min is ', vmin 
    print 'Max is ', vmax
    
    eavg = numpy.mean(edges)
    emin= min(edges)
    emax = max(edges) 
    
    print 'Edge Count Statistics' 
    print 'Average is ', eavg 
    print 'Min is ', emin 
    print 'Max is ', emax
    
    tavg = numpy.mean(texture) 
    tmin= min(texture)
    tmax = max(texture) 
    print 'Texture Statistics' 
    print 'Average is ', tavg 
    print 'Min is ', tmin 
    print 'Max is ', tmax

            
