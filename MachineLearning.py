from sklearn.svm import SVR
import numpy
from PIL import Image
 
import matplotlib
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

def svrAlg(): 
    X = [[0, 0], [2, 2]] #X is the array of metrics 

    densities = [0.5, 2.5] #densities are the measured densities 

    clf = SVR() #initialize support vector regression thing. 

    clf.fit(X,densities) #trains the model 

    return clf
    
    ##Number of tiles in one row (width-n)/(overlapSize)+1)
def densMap(fit, metricArray, n, overlap, imageSize ): 
    densities = fit.predict(metricArray)
    
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
       points += [[(i%(rowTiles)+1)*(n/2), (i/(rowTiles)+1)*(n/2)]]
         
         
         
    grid_x, grid_y = numpy.mgrid[0:width, 0:height]  #create a meshgrid  
    
    print grid_x
    print grid_y
    
    #points = [] #create a list of where the points are 
    
    #values in the example is densities 
    
    
    data = griddata(points, densities, (grid_x, grid_y), method = 'cubic') #interpolate to find all points 
    
    x = numpy.arange(0, width, 1)
    y = numpy.arange(0, height, 1)
    X, Y = numpy.meshgrid(x,y)
    
    ##Plotting 
    
   # print newArray
   # plt.figure()
    plt.figure(figsize = (width, height))
    fig = plt.contourf( data)
    
    plt.clabel(fig, inline=1, fontsize=10)
    plt.title('New plot!!!')
    
 #   plt.imshow(plt.contourf(data))
    
    plt.savefig('ContourPlot.jpg')
    
def overlayMap(mapName, contourName): 
    mapIm = Image.open(mapName) 
    contour = Image.open(contourName)
  #  contour.convert('RGBA')
   # contour.putalpha(30)
    plt.imshow(contour)
    mapIm.convert('RGBA')
    mapIm.putalpha(150)
    plt.imshow(mapIm)
    
    plt.savefig('OverlayMap.jpg')
