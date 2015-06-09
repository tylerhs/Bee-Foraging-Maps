from sklearn.svm import SVR
import numpy
from PIL import Image
 
import matplotlib
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

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
    colTiles = int(((height-n)/(overlapSize))+1)
    
    
    newArray = numpy.zeros((int((width-n)/(overlapSize)+1),int(((height-n)/(overlapSize))+1)))
    #print newArray
    for i in range(len(densities)): 
        newArray[i%(rowTiles),i/(rowTiles)] = densities[i]
        
    x = numpy.arange(0, rowTiles, 1)
    y = numpy.arange(0, colTiles, 1)
    X, Y = numpy.meshgrid(y,x)
    
    ##Plotting 
    
    print newArray
    plt.figure()
    fig = plt.contourf(X,Y, newArray)
    plt.clabel(fig, inline=1, fontsize=10)
    plt.title('New plot!!!')
    
    plt.savefig('ContourPlot.jpg')
    
def overlayMap(mapName, contourName): 
    mapIm = Image.open(mapName) 
    contour = Image.open(contourName)
    contour.convert('RGBA')
    contour.putalpha(70)
    plt.imshow(contour)
    mapIm.convert('RGBA')
    mapIm.putalpha(90)
    plt.imshow(mapIm)
    
    #contour.show()
