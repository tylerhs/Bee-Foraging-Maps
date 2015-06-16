from ImageProcess import * 
from MachineLearning import *
import os

def main(): 
    imageName = 'SmallTile.jpg'
    tileSize = 50 
    
    overlap = 0.1 
    imageSize = [472, 398]
    scaledMetrics, scaler= calcMetrics(imageName, tileSize, overlap) 
    
    learnSVR(scaledMetrics, tileSize, overlap, imageSize)
    
    
    
def totalSVR(imageList, densityList, imageName,tileSize, overlap): 
    """Does a complete run of the SVR learning algorithm. Takes in a training set of data."""
    image = Image.open(imageName)
    imageSize = image.size
    ####STep 1: Calculate Training Metrics 
    metricList, densityList = allTrainMetrics(imageList, densityList)
    
    
    ##Step 1: Scale the incoming training data 
    
    scaledTraining, scaler = scaleMetrics(metricList) 
    
    ### Train the machine learning algorithm 
    fit = svrAlg(scaledTraining, densityList) 
    
    ###Calculate metrics on full image 
    
    imageMetrics = calcMetrics(imageName, tileSize, overlap)
    #Scale the metrics 
    scaledMetrics = scaler.transform(imageMetrics) ##These are the final metrics on the full image
    #print 'scaled metrics'
    
    #learnSVR(scaledMetrics, tileSize, overlap, imageSize, fit)
    densMap(fit, scaledMetrics, tileSize, overlap, imageSize ) 

   # print 'Completed density map'
    
    raw_input("Please crop the contour plot. Press return to continue.")
    plt.close('all')
    overlayMap(imageName, 'ContourPlot.jpg') 
    
    
#if __name__ == "__main__":
    
    #totalSVR(['SuperSmallTile.jpg'], [0.5], 'SmallTile.jpg', 75, 0.5)

    
    