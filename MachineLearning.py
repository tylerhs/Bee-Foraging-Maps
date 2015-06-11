from sklearn.svm import SVR
import numpy
from PIL import Image
import matplotlib
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from sklearn.gaussian_process import GaussianProcess

def svrAlg(): 
    """Runs a Support Vector Regression Algorithm on X, an array of metrics 
        and densities, the corresponding densities. Note that X and densities should be updated 
        with actual field data collected."""
    X = [[0, 0], [2, 2]] #X is the array of metrics 

    densities = [0.5, 2.5] #densities are the measured densities 

    clf = SVR() #initialize support vector regression thing. 

    clf.fit(X,densities) #trains the model 

    return clf
    
def gaussReg(): 
    metrics = [[0, 0], [2, 2]] #List of lists of metrics calculated 
    densities =  [0.5, 2.5] #The corresponding densities 
    
    gp = GaussianProcess(corr='squared_exponential', theta0=1e-1,
                     thetaL=1e-3, thetaU=1,
                     random_start=100)    #Change these parameters to get better fit...            
    gp.fit(metrics, densities)
    return gp


    ##Number of tiles in one row (width-n)/(overlapSize)+1)
def densMap(fit, metricArray, n, overlap, imageSize ): 
    """Creates and saves a contour plot of densities based on an 
        input fit function, metrics, and image size characteristics."""
    densities = fit.predict(metricArray) #Use the ML fit to predict the density for each tile 
    
    width = imageSize[0] 
    height = imageSize[1] 
    overlapSize = int(overlap*n)
    rowTiles = int((width-n)/(overlapSize)+1)
    #colTiles = int(((height-n)/(overlapSize))+1)
    
    
 #   newArray = numpy.zeros((int((width-n)/(overlapSize)+1),int(((height-n)/(overlapSize))+1)))
 
    #newArray = numpy.zeros(width, height)
    #print newArray
    points = []
    for i in range(len(densities)): 
       # newArray[i%(rowTiles),i/(rowTiles)] = densities[i]
      # newArray[(i%(rowTiles)+1)*(n/2) , (i/(rowTiles)+1)*(n/2)] = densities[i]
       points += [[(i%(rowTiles)+1)*(n/2), (i/(rowTiles)+1)*(n/2)]] #Consider the density to be at the center of each tile 
         
         
         
    grid_x, grid_y = numpy.mgrid[0:width, 0:height]  #create a meshgrid  
    
    #print grid_x #Debugging print statements to check grid size 
    #print grid_y
    
    #points = [] #create a list of where the points are 
    
    #values in the example is densities 
    
    
    data = griddata(points, densities, (grid_x, grid_y), method = 'cubic') #interpolate to get continuous function of points 
    #can change interpolation method
    x = numpy.arange(0, width, 1) #probably won't actually need to use this part...
    y = numpy.arange(0, height, 1)
    X, Y = numpy.meshgrid(x,y)
    
    ##Plotting 
    
   # print newArray
   # plt.figure()
    plt.figure(figsize = (width, height))
    fig = plt.contourf( data)
    
    plt.clabel(fig, inline=1, fontsize=10)
    plt.title('ContourPlot!!!')
    
 #   plt.imshow(plt.contourf(data))
    
    plt.savefig('ContourPlot.jpg')
    
def overlayMap(mapName, contourName): 
    """Overlays the images of a contour map and the original aerial map. Saves the output.
    Note that the contour plot must be cropped to only include the contour image before 
    running this. """
    mapIm = Image.open(mapName) 
    contour = Image.open(contourName)
  #  contour.convert('RGBA')
   # contour.putalpha(30)
    plt.imshow(contour)
    mapIm.convert('RGBA') #Add a transparency layer to the image
    mapIm.putalpha(150) #higher number = darker image. Max = 255
    plt.imshow(mapIm) #Plot the overlaid map
    
    plt.savefig('OverlayMap.jpg')
    
    
def learnSVR(metricArray): 
    """A wrapper function for the machine learning algorithm and post-processing.""" 
    fit = svrAlg() 
    n= 100  #Change your metrics here!!!!!!!!!
    overlap = 0.1 
    imageSize = [100,400]
    
    densMap(fit, metricArray, n, overlap, imageSize )
    overlayMap('SmallTile.jpg', 'ContourPlot.jpg') 
    # Final map is saved as OverlayMap.jpg
    
    
def learnGauss(metricArray): 
    """A wrapper function for the Gaussian machine learning algorithm and post-processing.""" 
    fit = gaussReg() 
    n= 100  #You should probably change this...
    overlap = 0.1 
    imageSize = [100,400]
    densMap(fit, metricArray, n, overlap, imageSize )
    overlayMap('SmallTile.jpg', 'ContourPlot.jpg') 
    # Final map is saved as OverlayMap.jpg
    
