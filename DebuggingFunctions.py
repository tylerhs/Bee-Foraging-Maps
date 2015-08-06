from MachineLearning import * 
from FullProgram import * 
from ImageProcess import * 
from DensityAlignment import *
from Classification import * 


############Functions here were written for debugging purposes and are not used in 
############running the full program. 


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
    print Metrics
    
    #Find fit 
    fit = svrAlg(scaledTraining, densityList)
        
    density = fit.predict(Metrics)
    return list(density)
 
 
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
    
def fullTest():  #we never use this now. 
    imageName = 'SmallTile.jpg'
    tileSize = 50 
    
    overlap = 0.1 
    imageSize = [472, 398]
    scaledMetrics, scaler= calcMetrics(imageName, tileSize, overlap) 
    
    learnSVR(scaledMetrics, tileSize, overlap, imageSize)
    
def densMap(fit, metricArray, n, overlap, imageSize, imageName): 
    """Creates and saves a contour plot of densities based on an 
        input fit function, metrics, and image size characteristics."""
        
    if True: #Make true if you want to calculate densities (i.e. if you have a new fit/new density list)  
        print 'calculating densities'
        if type(fit)==sklearn.gaussian_process.gaussian_process.GaussianProcess: #If the fit is Gaussian
            densities, MSE = fit.predict(metricArray, eval_MSE =True)
            sigma = numpy.sqrt(MSE)
            print(sigma)
        else:
            densities = fit.predict(metricArray) #Use the ML fit to predict the density for each tile 
            #print len(densities)
        f = open('densities.txt', 'w')
        print >> f, list(densities)
        f.close()
    else: 
        f = open('densities.txt', 'r')
        data = f.read()
        densities = eval(data)
       # print densities
        densities = numpy.array(densities)
        f.close()
        imageName = 'FirstStitchLong.jpg'
        overlap = 0.2 
        n = 50
        image = Image.open(imageName) #open the image
        imageSize = image.size #get the image size 
 #   print 'Image Size is ', imageSize
 

    width = imageSize[0] 
    height = imageSize[1] 
   # print 'width ', width 
    #print 'height ', height
    overlapSize = int(overlap*n)
    rowTiles = int((width-n)/(overlapSize))+1
    print 'Row Tiles is ', rowTiles
    #colTiles = int(((height-n)/(overlapSize))+1)
    
    
 #   newArray = numpy.zeros((int((width-n)/(overlapSize)+1),int(((height-n)/(overlapSize))+1)))
 
    #newArray = numpy.zeros(width, height)
    #print newArray
    points = []
    for i in range(len(densities)):
        x = (i%rowTiles)*overlapSize + n/2
        y = (i/rowTiles)*overlapSize + n/2
        points += [[x,y]]
       # newArray[i%(rowTiles),i/(rowTiles)] = densities[i]
      # newArray[(i%(rowTiles)+1)*(n/2) , (i/(rowTiles)+1)*(n/2)] = densities[i]
      # points += [[(i%(rowTiles)+1)*(n/2), (i/(rowTiles)+1)*(n/2)]] #Consider the density to be at the center of each tile 
  #  print points
    grid_x, grid_y = numpy.mgrid[0:width, 0:height]  #create a meshgrid 
     
   # print densities
   # print('Points is ', points) 
   # print('Densities is ', densities)
    data = griddata(points, densities, (grid_x, grid_y), method = 'linear') #interpolate to get continuous function of points 
    #can change interpolation method
    print data.size

  #  print 'Max is ', numpy.amax(data)
   # min_max_scaler = sklearn.preprocessing.MinMaxScaler()
    #data_minmax = min_max_scaler.fit_transform(data) 
    
  
    
    ##Plotting 
    plt.figure(1)
    
    #plt.figure(figsize = (width, height))
  #  print "Hi Cassie"
    v = numpy.linspace(min(densities), max(densities), 20, endpoint=True)
    fig = plt.contourf(grid_x, grid_y, data, levels = v, alpha = 0.4, antialiased = True)
    
    mapIm = Image.open(imageName)
    plt.imshow(mapIm)
    maxDens = max(densities)
    print maxDens  
    x = plt.colorbar(fig)   
    plt.savefig('ContourPlot.jpg')
    return data
def testDensMap(n, overlap, imageName): 
    densities = [] 
    image = Image.open(imageName) 
    imageSize = image.size 
    width = imageSize[0]
    overlapSize = int(n*overlap)
   # rowTiles = math.ceil((width-n)/(overlapSize))
    print imageSize
    for i in range(n/2, imageSize[1], int(overlap*n)): #For the entire height of the picture 
       # print 'row number ', i
        #for j in range(0,imageSize[0]/2,int(overlap*n)): #For the first third of the image 
        #    densities += [0.8] 
        # #   print 'j ', j
        #for k in range(imageSize[0]/2, imageSize[0]-n, int(overlap*n)): #For the rest of the image 
        #    densities += [0.2] 
        for m in range(0, imageSize[0]-n, int(overlap*n)): 
            if m < imageSize[0]/2: 
                densities += [0.8] 
            else: 
                densities += [0.2]

         #   print 'k ', k
   # print 'Densities are ', densities 
    print 'Densities computed! Plotting now...'
    densMapShort(densities, imageName,overlap,n) 
    
def learnSVR(metricArray, n, overlap, imageSize, fit): 
    """A wrapper function for the machine learning algorithm and post-processing.""" 
   # fit = svrAlg() 
   # metricArray = [[1,1],[2,3],[4,5], [3,7],[70,20],[5,20],[9,18], [87,34],[43,127], [1,10],[5,3],[4,8], [3,90],[76,20],[500,20],[29,34], [38,34],[43,17]]
  #  n= 50  #Change your metrics here!!!!!!!!!
   # overlap = 0.3 
    #imageSize = [100,400]
    
    densMap(fit, metricArray, n, overlap, imageSize )
    overlayMap('SmallTile.jpg', 'ContourPlot.jpg') 
    # Final map is saved as OverlayMap.jpg
    
    
def learnGauss(metricArray): 
    """A wrapper function for the Gaussian machine learning algorithm and post-processing.""" 
    fit = gaussReg() 
    n= 100  #You should probably change this...
    overlap = 0.3 
    imageSize = [100,400]
    densMap(fit, metricArray, n, overlap, imageSize )
    overlayMap('SmallTile.jpg', 'ContourPlot.jpg') 
    # Final map is saved as OverlayMap.jpg
    
def mainTransect():  
    """Helper function to test the transect stitches and make sure they 
        are reasonable. Takes no arguments. Parameters are changed inside the function."""


   # Start = (3260, 2672 ) new transect data start/end points
   #
   # End = (2731, 12280)
   #
    imageName = 'TransectStitch2.jpg'
    End = (594, 1046)
    Start = (1718, 460)
    
    Start = (3581, 1582)
    End = (3227, 7596)
#
#    Start = (1035,588)
#    End = (456,1720)

  #  Start = tuple(raw_input('Please Input Start Coordinates'))
   # End  = tuple(raw_input('Please Input End Coordinates'))
   
    stuff= divideTransect(Start, End, imageName)
    if len(stuff) != 50: 
        print "Error! Transect length is not 50 meters." 
    return stuff  