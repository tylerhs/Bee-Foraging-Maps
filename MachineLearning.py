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
import math
import OpenGL
from mpl_toolkits.mplot3d import Axes3D
#import seaborn as sns
from sklearn import neighbors

def svrAlg(X, densities): 
    """Runs a Support Vector Regression Algorithm on X, an array of metrics 
        and densities, the corresponding densities."""
   # X = [[0, 0], [2, 2]] #X is the array of metrics 
    #densities = [0.5, 2.5] #densities are the measured densities 
 #   clf = SVR( epsilon= 0.90000000000000002, C= 52, gamma =  0.30000000000000004, degree =  6, kernel ='rbf') #initialize support vector regression thing. 
    clf = SVR(kernel = 'rbf', gamma = 0.05)
    clf.fit(X,densities) #trains the model 

    return clf
    
def gaussReg(metrics, densities): 
    """Runs a Gaussian Regression algorithm on metrics, and array of metrics, 
        and densities, the corresponding densities."""
  #  metrics = [[0, 0], [2, 2]] #List of lists of metrics calculated 
   # densities =  [0.5, 2.5] #The corresponding densities 
    
    gp = GaussianProcess( regr = 'linear', corr = 'absolute_exponential', theta0 = 1, thetaL=1, thetaU=10)    #Change these parameters to get better fit...            
   
    gp.fit(metrics, densities)
    return gp

    ##Number of tiles in one row (width-n)/(overlapSize)+1)

    
def densMapShort(densities,imageName, overlap, n): 
    """Takes in densities, a list of densities ordered by tile arrangement, 
    imageName, a string containing the file name of the image, 
    overlap, the percent tilesize to shift, and n, the tileSize. Creates 
    and displays a density map overlaid with the original image and returns a list 
    containing [rowTiles, colTiles] where row tiles is the number of tiles in a row 
    and colTiles is the number of tiles in a column."""
    image = Image.open(imageName) #open the image
    imageSize = image.size
    overlapSize = int(overlap*n)
    width = imageSize[0] 
    height = imageSize[1] 
    rowTiles = int((width-n)/(overlapSize))+1 
    colTiles = int((height-n)/(overlapSize))+1
        
    points = [] #Compute the points where densities are being plotted
    for i in range(len(densities)):
        x = (i%rowTiles)*overlapSize + n/2
        y = (i/rowTiles)*overlapSize + n/2
        points += [[x,y]]
    #interpolation
    grid_x, grid_y = numpy.mgrid[0:width, 0:height]
    data = griddata(points, densities, (grid_x, grid_y), method = 'cubic')
    
    

    numpy.savetxt("densitiesTest.csv", data, delimiter = ",")
    #with open('densities.csv', 'wb'), as f: 
    #    writer = csv.writer('densities.csv')
    #    writer.writerows(data)
   # spec = sns.cubehelix_palette(20, start = 0.5, rot = -0.8)

  #  spec = sns.color_palette(n_colors = 20)
    #Plotting stuff
    v = numpy.linspace(min(densities), max(densities), 20, endpoint=True)
    fig = plt.contourf(grid_x, grid_y, data, levels = v, alpha = 0.4, antialiased = True)

    mapIm = Image.open(imageName)
    plt.imshow(mapIm)
    
    
    x = plt.colorbar(fig)

    plt.savefig('TransectContour.pdf', format = 'pdf', dpi = 1200)
    return [rowTiles, colTiles]
    

    
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
    
    
