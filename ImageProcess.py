import ImageFilter
import numpy
from PIL import Image
from PIL import ImageStat
from colorsys import * 
import time
from operator import add
from sklearn import preprocessing
from skimage import data

from MachineLearning import * 

#from multiprocessing import Pool   ##Hopefully figure this out - used for multithreading 

#Extract all nxn rectangles from an image (these will be processed then used as inputs for ML algorithm). 
def getSub(n, imageName, overlap): 
    """Takes in n, an integer less than or equal to the minimum dimension of the image 
       and imageName, the string containing the name of the image to be processed.  
       Returns a list of all nxn subrectangles of image.""" 
    # define overlap percentage for sub images        
    image = Image.open(imageName) #load in the image.
    #Find the size of the image. 
    size = image.size
 #  print(size)
    width = size[0] #pull out length and width 
    length = size[1] 
   # subList = []
   #Initialize lists to hold metric results (for analysis later to test) 
    avgList = [] 
  #  avgTimeL = []
    yellowList = [] 
   # yellowTimeL = []
    varList = [] 
    #varTimeL = []
    edgeList = [] 
    #edgeTimeL = []
    textList = []
    #textTimeL = []
    
    smallTileSize = int(overlap*n)
    
    MetricDict = {} #initialize empty dict. 
    # Extract all tiles using a specific overlap (overlap depends on n)
    for i in range(0,width -int( overlap*n), int(overlap*n)): #Go through the entire image 
        for j in range(0, length - int(overlap*n), int(overlap*n)): 
            box = (i,j,i+smallTileSize, j+smallTileSize)  #edge coordinates of the next rectangle. 
            newImage = image.crop(box) #pull out the desired rectangle
        #    subList += [newImage] #More efficient way to store each image? 
            ### METRIC CALCULATIONS - Time counters commented out for now. 

            
           # start = time.time()
            avg = colorAvg(newImage) 
          #  avgTime = time.time() - start 
           # avgTimeL += [avgTime]
           
            yellow = findYellowFast(newImage)
            #yellowTime = time.time() - avgTime - start
            #yellowTimeL += [yellowTime]
         
            var = colorVariance(newImage) 
            #varTime = time.time() - yellowTime - start
            #varTimeL += [varTime]
         
            edges = countEdgePixels(newImage)
            #edgeTime = time.time() - varTime - start
            #edgeTimeL += [edgeTime]
           
            texture = textureAnalysis(newImage) 
            #textTime = time.time() - edgeTime - start
            #textTimeL += [textTime]
      
            avgList += [avg] 
            yellowList += [yellow] 
            varList += [var] 
            edgeList += [edges]
            textList += [texture]
            Metrics = (avg[0], avg[1], avg[2], yellow, var, edges, texture) #store metrics
            
            MetricDict[(i,j)] = Metrics

   # return avgList, yellowList, varList, edgeList, textList, avgTimeL, yellowTimeL, varTimeL, edgeTimeL, textTimeL
    return MetricDict
    
def allMetrics(dictionary,n, im, overlap): 
    """Takes in a dictionary of results from small tiles and calculates average metrics 
    	for a larger tile of size n, in image im, with overlap percentage im."""
    width, height = im.size 
  #  print dictionary
    #FinalMetricDict = {}
    numberMetrics = 7 #Change for diff number of metrics as we add more. 
    overlapSize = int(overlap*n)
    numberTiles = int((width-n)/(overlapSize)+1)*int(((height-n)/(overlapSize))+1)
    metricArray = numpy.zeros((numberMetrics, numberTiles))
    
    for i in range(0,width - n, int(overlap*n)): 
        for j in range(0,height- n, int(overlap*n)): 
            #you're at the start of a box 
            metricTotals = len(dictionary[(0,0)])*[0.0]
            ##Adding up metrics from small tiles 
            for k in range(i,i+n-int(overlap*n)+1, int(overlap*n)): 
                for m in range(j, j+n-int(overlap*n)+1, int(overlap*n)): 
                    #pull out metrics 
                    metrics = dictionary[(k,m)]
                    #print metrics 
                    metricTotals = map(add, metricTotals, metrics)
            ##Averaging metrics 
            num = 1/(overlap**2)
            newMetric = [a/num for a in metricTotals]
            
            ##Put all metrics metrics in an array. One metric per row. 
            for index in range(len(metricTotals)): 
                metricArray[index,int(i/(overlap*n) + j*(width-n)/((overlap*n)**2))] = newMetric[index] 
    #print metricArray 
    #raw_input('Huh?')
    return metricArray 
                
def calcMetrics(imageName, tileSize, overlap): 
    """wrapper function to calculate metrics for each tile of the image.
        returns an array containing metric vectors in order by coordinates 
        of the upper left hand of the tile desired. Also returns a scalar object 
        for scaling future input data. """ 
        
    NUMBERMETRICS = 7
    im = Image.open(imageName)
    subDict = getSub(tileSize, imageName, overlap)  #Get a dictionary of metrics for small tiles
    finalMetrics = allMetrics(subDict, tileSize, im, overlap) #calculate metrics on larger tiles  
    #scaled, scaler = scaleMetrics(finalMetrics) ##Scale metrics 
    totalSize = finalMetrics.size #Find the size of this scaled metric array
    numCols = totalSize/NUMBERMETRICS  #Find the number of tiles =number of cols
    scaledMetrics = []
    for i in range(numCols): ##Change output into a list of lists 
        currentMetric = [] 
        for metric in range(NUMBERMETRICS): 
            currentMetric += [finalMetrics[metric, i]] 
        scaledMetrics += [currentMetric]
    return scaledMetrics #return the scaledmetrics and the scaler for later use...
    
def scaleMetrics(metricArray): 
    """Takes in a array of metrics, scales them to have 
        mean 0 and stdev 1. returns both the metrics and the scaler object 
        which can be used to transform later data. """ 
        
    #First put all metrics into arrays with one metric 
    scaler = preprocessing.StandardScaler().fit(metricArray)
    scaledArray = scaler.transform(metricArray) 
    return scaledArray, scaler 


#######################Debugging Functions############################# 


def oneDensity((i,j), w, h, imageName): 
    densityList = [0.0,1.0, 0.99, 0.02, 0.64, 0.0, 0.1]

    image = Image.open(imageName) 
    
    box = (i,j,i+w, j+h)
    newImage = image.crop(box)
    
    
    f = open('metricList.txt', 'r')
    data = f.read()
    metricList = eval(data)
    scaledTraining, scaler = scaleMetrics(metricList)
    
    #Calculate metrics 
    avg = colorAvg(newImage) 
    yellow = findYellowFast(newImage) 
    edges = countEdgePixels(newImage) 
    var = colorVariance(newImage) 
    texture = textureAnalysis(newImage)
    Metrics = (avg[0], avg[1], avg[2], yellow, var, edges, texture)
   # print 'Original Metrics ', Metrics
    Metrics = scaler.transform(Metrics)
    
    #Find fit 
    fit = svrAlg(scaledTraining, densityList)
        
    density = fit.predict(Metrics)
    return list(density)
 
def oneDensOverlap((i,j), n, imageName, overlap, subTileDict, fit, scaler): 
    """Computes the density of one tile with overlap""" 
    #Note that this algorithm assumes 1/overlap is an integer 
    shiftSize = int(n*overlap)
    #How many subtiles are in the width of the image? 
    numTiles =int( 1/overlap )
    metricTotal = len(subTileDict[(0,0)])*[0.0]
    for k in range(numTiles): 
        for m in range(numTiles): 
           # print (k,m)
            newMetrics = subTileDict[(i + m*shiftSize, j + k*shiftSize)]
            metricTotal = map(add, metricTotal, newMetrics)
  #  print metricTotal
    num = 1/(overlap**2)
    avgMetric = [a/num for a in metricTotal] #Compute the average 
   # print avgMetric
    scaledMetric = scaler.transform(avgMetric) #Scale the metric 
    density = fit.predict(scaledMetric) 
    return list(density)
    
def allDensOverlap(n, imageName, overlap): 
    """Computes all densities on a map with tilesize n, the given image as the map, and an overlap 1-overlap."""
    image = Image.open(imageName) 
    imageSize = image.size 
    width = imageSize[0]
    height = imageSize[1] 
    densityList = []
    
    subTileDict = getSub(n, imageName, overlap) #Compute the metrics on subtiles 
    
    #Read in the training data
    f = open('metricList.txt', 'r')
    data = f.read()
    metricList = eval(data)
    scaledTraining, scaler = scaleMetrics(metricList)
    
    densityList = [0.0,1.0, 0.99, 0.02, 0.64, 0.0, 0.1] ##Change density list in code because training only happens once. 
    fit = svrAlg(scaledTraining, densityList)
    
    allDensities = []
    shiftSize = int(n*overlap)
    for k in range(0, height -n, shiftSize): 
        for m in range(0, width - n, shiftSize): 
          #  print (m,k)
            currentDensity = oneDensOverlap((m,k), n, imageName, overlap, subTileDict, fit, scaler)
            allDensities += currentDensity
    return allDensities 
    
    
def allDensities(w,h, imageName): 
    image = Image.open(imageName) 
    imageSize = image.size 
    width = imageSize[0]
    height = imageSize[1] 
    
    densityList = []
    for k in range(0, height -h, h): 
        for m in range(0, width - w, w): 
            currentDensity = oneDensity((m,k), h, w, imageName)
            densityList += currentDensity
    return densityList 
    
    
######TRAINING SET CALCULATIONS#########################

def trainMetrics(imageName, density): 
    image = Image.open(imageName) 
    avg = colorAvg(image) 
    yellow = findYellowFast(image) 
    edges = countEdgePixels(image) 
    var = colorVariance(image) 
    texture = textureAnalysis(image) 
    
    metrics = [avg[0], avg[1], avg[2], yellow, var, edges, texture] 
    return [metrics, density] 
    
def allTrainMetrics(imageList, densityList): 
    metricsList = []
    for i in range(len(imageList)): 
        imageName = imageList[i]
        #currentIm = Image.open(imageName) 
        [metrics, density] = trainMetrics(imageName, densityList[i]) 
        metricsList += [metrics] 
    return metricsList, densityList
    
      
          
#Start of helper functions for computing metrics. 
    
def colorAvg(im): 
    """Takes in a string containing an image file name, returns the average red, blue, and green 
        values for all the pixels in that image.""" 
    #im = Image.open(imageName) 
    imStats = ImageStat.Stat(im) 
    (redAv, greenAv, blueAv) = imStats.mean
    return redAv, greenAv, blueAv
    
    

  #rgb_to_hsv(r/255.,g/255.,b/255.)  converts pixel coords to HSV coords 
  
   
def findYellow(im):  #Use the fast version! (findYellowFast(im))
    """counts the number of yellow pixels in the given image.""" 
    #im = Image.open(imageName)
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
    
def colorVariance(im):
    ''' calculates the diversity in color using a hue histogram'''
    
    # load image pixels
    #im = Image.open(imageName)
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
    #print histogram
    # calculate standard deviation of histogram
    return numpy.std(histogram)
        
    
      
def countEdgePixels(im):
    ''' counts the number of pixels that make up the edges of features'''
    # define threshold for edges
    threshold = 150 
    
    # open image and filter
    #im = Image.open(imageName)
    im2 = im.filter(ImageFilter.FIND_EDGES)
    #im2.save("Filtered.jpg")
    im2 = im2.convert("L")
	
    # load pixels and count edge pixels
    pix = im2.load()
    pixels = 0
    for x in range(0,im.size[0]):
        for y in range(0, im.size[1]):
            if pix[x,y] > threshold:
                pixels += 1

    return float(pixels) / (im.size[0]*im.size[1])
    
def textureAnalysis(im):
    ''' determines the proportion of the image that has texture'''
    # define texture threshold and grid size
    threshold = 100
    n = 7
    
    # open image
    #im = Image.open(imageName)
    width, height = im.size
    
    # loop across image
    count = 0
    for i in range(0,width-n,n):
        for j in range(0,height-n,n):
            
            # divide into small grids
            box = (i,j,i+n,j+n)
            imTemp = im.crop(box)
            
            # calculate intensity from RGB data
            pixels = list(imTemp.getdata())
            intensity =  [pixels[i][0]+pixels[i][1]+pixels[i][2] for i in range(len(pixels))]
                      
            # count as high texture if difference in intensity is 
            # greater than threshold
            if ((max(intensity) - min(intensity)) > threshold):
                count += 1
                
    # calculate the percentage of high texture grids
    
    if width/n == 0: 
        print width
        raw_input('Oops')
    return float(count)/((width/n)*(height/n))
    
def findYellowFast(im): 
    """counts the number of yellow pixels in the given image.""" 
 #   im = Image.open(imageName)
    #define HSV value ranges for yellow  
    #for now just base of Hue - refine for actual yellows seen in field? 
    minHue = 43/360.
    maxHue = 49/360.
    
    minSat = 80/360. 
   # maxSat = 0.4
   
    minV = 70/360.
    
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

            
