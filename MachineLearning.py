from sklearn.svm import SVR
import numpy
from PIL import Image
import matplotlib
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from sklearn.gaussian_process import GaussianProcess
import sklearn

def svrAlg(X, densities): 
    """Runs a Support Vector Regression Algorithm on X, an array of metrics 
        and densities, the corresponding densities. Note that X and densities should be updated 
        with actual field data collected."""
   # X = [[0, 0], [2, 2]] #X is the array of metrics 

    #densities = [0.5, 2.5] #densities are the measured densities 

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
    if type(fit)==sklearn.gaussian_process.gaussian_process.GaussianProcess: #If the fit is Gaussian
        densities, MSE = fit.predict(metricArray, eval_MSE =True)
        sigma = numpy.sqrt(MSE)
        print(sigma)
    else:
        densities = fit.predict(metricArray) #Use the ML fit to predict the density for each tile 
    
    width = imageSize[0] 
    height = imageSize[1] 
   # print 'width ', width 
    #print 'height ', height
    overlapSize = int(overlap*n)
    rowTiles = int((width-n)/(overlapSize))+1
    #print 'rowTiles is ', rowTiles
    #colTiles = int(((height-n)/(overlapSize))+1)
    
    
 #   newArray = numpy.zeros((int((width-n)/(overlapSize)+1),int(((height-n)/(overlapSize))+1)))
 
    #newArray = numpy.zeros(width, height)
    #print newArray
    points = []
    for i in range(len(densities)):
        points += [[(i%rowTiles)*overlapSize + n/2, (i/rowTiles)*overlapSize + n/2]]
       # newArray[i%(rowTiles),i/(rowTiles)] = densities[i]
      # newArray[(i%(rowTiles)+1)*(n/2) , (i/(rowTiles)+1)*(n/2)] = densities[i]
      # points += [[(i%(rowTiles)+1)*(n/2), (i/(rowTiles)+1)*(n/2)]] #Consider the density to be at the center of each tile 

    grid_x, grid_y = numpy.mgrid[0:width, 0:height]  #create a meshgrid  


    print 'At line 72 in densMap'
    #print grid_x #Debugging print statements to check grid size 
    #print grid_y
    
    #points = [] #create a list of where the points are 
    
    #values in the example is densities 
    
  #  print('Points is ', points) 
   # print('Densities is ', densities)
    data = griddata(points, densities, (grid_x, grid_y), method = 'cubic') #interpolate to get continuous function of points 
    #can change interpolation method
    x = numpy.arange(0, width, 1) #probably won't actually need to use this part...
    y = numpy.arange(0, height, 1)
    X, Y = numpy.meshgrid(x,y)
    
  #  print 'At line 88 in densMap' 
    ##Plotting 
   #print newArray
    plt.figure(1)
    
    #plt.figure(figsize = (width, height))
  #  print "Hi Cassie"
    fig = plt.contourf(grid_x, grid_y, data, levels=[-2,-1,0,1,2])
    
   # print 'At line 95 in densMap'
    #plt.clabel(fig, inline=1, fontsize=10)
    #plt.title('ContourPlot!!!')
    
    
    #plt.imshow(plt.contourf(data))
    
    plt.savefig('ContourPlot.jpg')
    
    
    plt.close()
    
def overlayMap(mapName, contourName): 
    """Overlays the images of a contour map and the original aerial map. Saves the output.
    Note that the contour plot must be cropped to only include the contour image before 
    running this. """
    mapIm = Image.open(mapName) 
    contour = Image.open(contourName)
  #  contour.convert('RGBA')
   # contour.putalpha(30)
    plt.figure(2)
    plt.imshow(contour)
    mapIm.convert('RGBA') #Add a transparency layer to the image
    mapIm.putalpha(150) #higher number = darker image. Max = 255
    plt.imshow(mapIm) #Plot the overlaid map
    
    plt.savefig('OverlayMap.jpg')
    
    
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
    
