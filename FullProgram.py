# -*- coding: utf-8 -*-
from ImageProcess import * 
from MachineLearning import *


def main():  #we never use this now. 
    imageName = 'SmallTile.jpg'
    tileSize = 50 
    
    overlap = 0.1 
    imageSize = [472, 398]
    scaledMetrics, scaler= calcMetrics(imageName, tileSize, overlap) 
    
    learnSVR(scaledMetrics, tileSize, overlap, imageSize)
    
def totalSVR(densityList, imageName,tileSize, overlap): 
    """Does a complete run of the SVR learning algorithm. Takes in a training set of density
        data, an imageName in a string, the size of tile desired and an overlap as a percentage."""
    image = Image.open(imageName) #open the image
    imageSize = image.size #get the image size 
    
    imageList = makePicList(7) #Make a list of picture names, numbered by site number '1.jpg' etc. 
    ####Step 1: Calculate Training Metrics 
    if False: #Make True if you want to calculate a new set of training metrics
        metricList, densityList = allTrainMetrics(imageList, densityList) #Compute the metrics on each training image 
        f = open('metricList.txt', 'w')
        print >> f, list(metricList)
        f.close()
    else: 
        f = open('metricList.txt', 'r')
        data = f.read()
        metricList = eval(data)
    
    #print 'metric list ', metricList
    #print 'Training metrics computed' 
    
    ##Step 2: Scale the incoming training data 
    
    scaledTraining, scaler = scaleMetrics(metricList)  #Scale the training metrics to mean 0 and std 1 
    
    ### Train the machine learning algorithm 
    fit = svrAlg(scaledTraining, densityList)  #fit the algorithm 
    print 'Fit is ', fit
    
    print 'Machine Learning done'
    
    ###Calculate metrics on full image 
    
    if True: #Make true if you need to calculate image metrics on a new image. Otherwise make false 
        imageMetrics = calcMetrics(imageName, tileSize, overlap) #calculate the image metrics on the full image
        #Scale the metrics 
        scaledMetrics = scaler.transform(imageMetrics) ##These are the final metrics on the full image - scaled the same as the training metrics 
        f = open('imageMetrics.txt', 'w')
        print >> f, list(scaledMetrics)
        f.close()
    else: 
        f = open('imageMetrics.txt', 'r')
        data = f.read()
        scaledMetrics = eval(data)
    

    
    print 'Image metrics computed'
    
    densities = densMap(fit, scaledMetrics, tileSize, overlap, imageSize, imageName ) 
    numpy.savetxt("densities.csv", densities, delimiter=",",  fmt= '%.4f')   # print 'Completed density map'
    

def totalGauss(densityList, imageName,tileSize, overlap): 
    """Does a complete run of the SVR learning algorithm. Takes in a training set of density
        data, an imageName in a string, the size of tile desired and an overlap as a percentage."""
    image = Image.open(imageName)
    imageSize = image.size
    
    imageList = makePicList(7)
    ####STep 1: Calculate Training Metrics 
    
    metricList, densityList = allTrainMetrics(imageList, densityList)
    
    print 'Training metrics computed'
    
    ##Step 1: Scale the incoming training data 
    
    scaledTraining, scaler = scaleMetrics(metricList) 
    
    ### Train the machine learning algorithm 
    fit = gaussReg(scaledTraining, densityList) 
    
    print 'Machine Learning done'
    
    ###Calculate metrics on full image 
    
    imageMetrics = calcMetrics(imageName, tileSize, overlap)
    #Scale the metrics 
    scaledMetrics = scaler.transform(imageMetrics) ##These are the final metrics on the full image
    #print 'scaled metrics'
    
    print 'Image metrics computed'
    
    #learnSVR(scaledMetrics, tileSize, overlap, imageSize, fit)
    results = densMap(fit, scaledMetrics, tileSize, overlap, imageSize, imageName ) 

   # print 'Completed density map'
    
   # raw_input("Please crop the contour plot. Press return to continue.")
  #  plt.close('all')
  
   # overlayMap(imageName, 'ContourPlot.jpg') 
   
    return results
    
def makePicList(numSites): 
    """makes an image name list for a given number of sites.""" 
    nameList = []
    for i in range(numSites): #for each site 
        currentName = str(i+1)+".jpg" 
        nameList += [currentName]
    return nameList
        
#if __name__ == "__main__":
    
    #totalSVR(['SuperSmallTile.jpg'], [0.5], 'SmallTile.jpg', 75, 0.5)

    
    