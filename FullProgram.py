# -*- coding: utf-8 -*-
from ImageProcess import * 
from MachineLearning import *
from DensityAlignment import *
import math
from sklearn import grid_search
from sklearn import cross_validation
from scipy.stats import randint 
from sklearn.grid_search import *
from Classification import *
from sklearn import feature_selection


Image.MAX_IMAGE_PIXELS = None #So that you can load in large images. Be careful not to crash your computer. 

def totalSVR(densityList, imageName,tileSize, overlap, trainingType): 
    """Does a complete run of the SVR learning algorithm. Takes in a training set of density
        data, an imageName in a string, the size of tile desired and an overlap as a percentage."""
   # densityList = makeDensList()
    #trainingType: 
    #              1 = picList  (transects)
    #              2 = previous data set 
                  
    ##Note that if you have multiple transects you can simply save each transects group of pictures as a picList and then use method 1. 

    ####This section creates an imageList and densityList automatically for you. You can also comment it out and 
    ####Input the lists into the function yourself. This section is for convenience.####

    NUMPICS = 50
    densityList = makeDensList() 
    imageList = makePicList(NUMPICS)
    imageList += ['TreeTrain1.jpeg', 'TreeTrain2.jpeg', 'TreeTrain3.jpeg', 'TreeTrain4.jpeg', 'TreeTrain5.jpeg', 'TreeTrain6.jpeg', 'Grass1.jpg', 'Path1.jpg', 'Buckwheat.jpeg', 'Buckwheat2.jpeg', 'Buckwheat3.jpeg']

            
    if trainingType == 1:  ##pull in pictures titled '1.jpg', etc. 
        metricList, densityList = allTrainMetrics(imageList, densityList)

        ##Save the training set 
        numpy.savetxt('metricListTraining.csv', metricList, delimiter = ",")
        numpy.savetxt('densityListTraining.csv', metricList, delimiter = ",")     
        
    if trainingType == 2:  #Just read in old data that was already saved.
        metricList = numpy.loadtxt('metricListTraining.csv', delimiter = ",")
        densityList = numpy.loadtxt('densityListTraining.csv', delimiter = ",")

    if trainingType == 3:  ### Other types of training sets. Manually enter here so that the other code doesn't need to change. 
        imageList = ['test1.jpg', 'test2.jpg']
        densityList = [1, 0]
        metricList , densityList = allTrainMetrics(imageList, densityList)
        
    ##Step 2: Scale the incoming training data 
    
    scaledTraining, scaler = scaleMetrics(metricList)  #Scale the training metrics to mean 0 and std 1 
    
    ### Train the machine learning algorithm 
    fit = svrAlg(scaledTraining, densityList)  #fit the algorithm 
    
    print 'Machine Learning done'
    
    ###Calculate densities on full image 
    
    if True: #Make true if you need to calculate image metrics on a new image. Otherwise make false
        imageDens = allDensOverlap(tileSize, imageName, overlap, densityList, metricList, fit, scaler)
        fileName = imageName[0:-4] + 'Densities' +  '.txt'
        numpy.savetxt(fileName, imageDens, delimiter = ",")
    else: 
        fileName = imageName[0:-4] + 'Densities' +  '.txt'
        imageDens = numpy.loadtxt(fileName, delimiter = ",")

    print 'Image densities computed'
    densMapShort(imageDens,imageName, overlap, tileSize)
    return fit 
    
def totalGauss(densityList, imageName,tileSize, overlap, trainingType): 
    """Does a complete run of the SVR learning algorithm. Takes in a training set of density
        data, an imageName in a string, the size of tile desired and an overlap as a percentage."""
    densityList = makeDensList()
    #trainingType:  
    #              1 = picList/transect 
    #              2 = previous data set 
                  
    ##Note that if you have multiple transects you can simply save each transects group of pictures as a picList and then use method 1. 
   
    ####Rewrite image and density lists.... 
    NUMPICS = 50  ##Change the number of training pictures here. 
    imageList = makePicList(NUMPICS)
    imageList = makeImList(imageList)        
        
    if trainingType == 1:  ##pull in pictures titled '1.jpg', etc. 
        print('Using saved pictures for training data')
        NUMPICS = 50  ##Change the number of training pictures here. 
        imageList = makePicList(NUMPICS)
        imageList = makeImList(imageList)
        
        metricList, dL = allTrainMetrics(imageList, densityList)

        ### Save the training set  - metrics

        
        numpy.savetxt('metricListTraining.csv', metricList, delimiter = ",")
        
        #### Save the training set - densities 
        #f = open('densityListTraining.txt', 'w')
        #print >> f, densityList 
        #f.close()        
        #
        numpy.savetxt('densityListTraining.csv', densityList, delimiter = ",")
        
    if trainingType == 2: 
        metricList = numpy.loadtxt('metricListTraining.csv', delimiter = ",")
        densityList = numpy.loadtxt('densityListTraining.csv', delimiter = ",")
    if trainingType == 3: 
        print('Using other type of training data')
        imageList = ['test1.jpg', 'test2.jpg']
        densityList = [100, 0]
        metricList , densityList = allTrainMetrics(imageList, densityList)
        
    ##Step 2: Scale the incoming training data 
    
    scaledTraining, scaler = scaleMetrics(metricList) 
    

    fit = gaussReg(scaledTraining, densityList)  ## Fit using Gaussian Regression
    classifier = getClassifier()
    
    print 'Machine Learning done'
    
    ###Calculate densities on full image 
    
    if True: #Make true if you need to calculate image metrics on a new image. Otherwise make false
        imageDens = allDensOverlapClass(tileSize, imageName, overlap, densityList, metricList, fit, scaler, classifier)
        fileName = imageName[0:-4] + 'Densities' +  '.txt'
        numpy.savetxt(fileName, imageDens, delimiter = ",")
    else: 
        fileName = imageName[0:-4] + 'Densities' +  '.txt'
        imageDens = numpy.loadtxt(fileName, delimiter = ",")

    print 'Image densities computed'
    [rowTiles, colTiles] = densMapShort(imageDens,imageName, overlap, tileSize)
    
    
    ####Output a file in the correct format for the bee simulation. 
    fileName = imageName[0:-4] + 'Densities' + 'withRows' + '.txt'
    f = open(fileName, 'w')
    print >> f, list([rowTiles, colTiles] + imageDens)
    f.close()
    
    
    
    return fit
    
def makePicList(numSites): 
    """makes an image name list for a given number of sites.""" 
    nameList = []
    for i in range(numSites): #for each site 
        currentName = str(i+1)+".jpg" 
        nameList += [currentName]
    return nameList
        
#if __name__ == "__main__":
    
    #totalSVR(['SuperSmallTile.jpg'], [0.5], 'SmallTile.jpg', 75, 0.5)

    
def makeDensList(): 
    """Creates a density list. Change the length of the list inside the code, as well as 
    entering the desired trainingData manually. Returns a numpy array of densities."""
    trainingData = numpy.zeros(83)

    
     #Uncomment below groupings for full data set from both transects, plus additional data.  
    #trainingData[2] = 14 
    #trainingData[3] = 3
    #trainingData[4] = 7
    #trainingData[6] = 8
    #trainingData[19] = 5
    #
    #trainingData[54] = 25830 
    #trainingData[58] = 7840 
    #trainingData[59] = 13600
    #trainingData[68] = 1 
    #trainingData[58] = 20000 
    #trainingData[64] = 20000 
    #trainingData[66] = 40000 
    
    ######Start of handmade density list. Do not use for final as this is not 
    ######based on field data. Just guessing. 
    #
    #trainingData[58] = 7800 
    #trainingData[64] = 10000
    #trainingData[66] = 5000
    #trainingData[108] = 20000
    #trainingData[109] = 10000
    #trainingData[110] = 20000
    
    #Uncomment group below if NNG data comes firt. 
 #   trainingData[4] = 25830 
    trainingData[4] = 1000
    trainingData[8] = 7840 
    trainingData[7] = 2000
  #  trainingData[9] = 13600 
    #trainingData[18] = 1
    #
    trainingData[58] = 20000
    trainingData[59] = 10000
    trainingData[60] = 20000
    trainingData[67] = 20000
    trainingData[68] = 10000
    trainingData[69] = 5000
    trainingData[70] = 10000
    trainingData[71] = 7000
    trainingData[72] = 2000
    #trainingData += [0,0,0,0,0,0,0,0,20000, 10000, 20000, 0,0,0,0,0,0, 20000, 10000, 5000,
    #10000, 7000, 2000] 
    

    return trainingData    
def makeImList(imList): 
    """Takes in a list of images and appends the list of extra training images to it. 
    Returns the appended list."""
    imList += ['TreeTrain1.jpeg', 'TreeTrain2.jpeg', 'TreeTrain3.jpeg', 
    'TreeTrain4.jpeg', 'TreeTrain5.jpeg', 'TreeTrain6.jpeg', 'Grass1.jpg',
    'Path1.jpg', 'Buckwheat.jpeg', 'Buckwheat2.jpeg', 'Buckwheat3.jpeg', 
    'Zero1.jpeg', 'Zero2.jpeg', 'Zero3.jpeg', 'Zero4.jpeg', 'Zero5.jpeg', 
    'Zero6.jpeg', 'BW1.jpeg', 'BW2.jpeg', 'BW3.jpeg', 'BW4.jpeg', 'BW5.jpeg', 'BW6.jpeg', 
    'Grass2.jpeg', 'Grass3.jpeg', 'Grass4.jpeg', 'Grass5.jpeg', 'Grass6.jpeg', 'Grass7.jpeg',
    'Grass8.jpeg', 'Grass9.jpeg', 'Grass10.jpeg', 'Grass11.jpeg']
    return imList
def scoreFit(): 
    
    """Scores the fit of the function defined inside the function with the training data 
    read in from the relevant files. Returns a number representing a score. Bigger is better."""
    ##Calculate the training data. 
    metricList = numpy.loadtxt(open("metricListTraining.csv", "rb"), delimiter = ',')
    
    
    densityList = numpy.loadtxt(open("densityListTraining.csv", "rb"), delimiter = ',')
    scaledTraining, scaler = scaleMetrics(metricList) 
    
    
    X_train, X_test, y_train, y_test=cross_validation.train_test_split(scaledTraining, densityList, test_size = 0.4, random_state=0) 
    
    #clf = SVR( kernel = 'rbf', gamma = 0.05, epsilon = 0.4)
  #  clf = SVR(C=1.0, cache_size=200, coef0=0.0, degree=3, epsilon=0.1, gamma=0.05,
  #kernel='rbf', max_iter=-1, shrinking=True, tol=0.001, verbose=False)

  #  gp = GaussianProcess( corr='absolute_exponential',theta0 = 0.4, thetaL = 0.001, thetaU = 1, random_start = 10)    #Change these parameters to get better fit...            
    gp = GaussianProcess( corr='absolute_exponential', theta0 = .4, thetaL=.001, thetaU=1.0)    #Change these parameters to get better fit...            
        
    gp.fit(X_train, y_train)
    
    #clf.fit(X_train, y_train) 
    #
    #return clf.score(X_test, y_test)
    
    return gp.score(X_test, y_test)

def findGaussParams(): 
    """Finds and scores randomized sets of Gaussian parameters. Higher score means 
        a better mapping. Returns a list of scores, parameters, and other data."""
    metricList = numpy.loadtxt(open("metricListTraining.csv", "rb"), delimiter = ',')
    densityList = numpy.loadtxt(open("densityListTraining.csv", "rb"), delimiter = ',')
    densityList, scaler = scaleMetrics(metricList)     
    
    fit = GaussianProcess()
    
    params = {}
    
    params['regr'] = ['constant', 'linear', 'quadratic']
    #params['corr'] = ['absolute_exponential', 'squared_exponential', 'cubic', 'linear']
    params['corr'] = ['absolute_exponential']
    params['theta0'] = range(1,11)
    params['thetaU'] = range(6,11)
    params['thetaL'] = range(1,6) 
    
    rand_search = RandomizedSearchCV(fit, param_distributions = params)
    
    X,y = metricList, densityList
    
    
    rand_search.fit(X,y)
    print(rand_search.grid_scores_)
    
    return rand_search.grid_scores_
    
def findSVRParams(): 
    """Finds and scores randomized sets of SVR parameters. Higher score means 
        a better mapping. Returns a list of scores, parameters, and other data."""
    #Load in metrics 
    metricList = numpy.loadtxt(open("metricListTraining.csv", "rb"), delimiter = ',')
    densityList = numpy.loadtxt(open("densityListTraining.csv", "rb"), delimiter = ',')
    metricList, scaler = scaleMetrics(metricList)
        
    fit = SVR()
    
    params = {}
    
    params['C'] = list(numpy.arange(0,100))
    params['epsilon'] =list( numpy.arange(0,5, 0.1))
    params['kernel'] = ['linear', 'poly', 'rbf', 'sigmoid']
    params['degree'] = list(numpy.arange(0,10))
    params['gamma'] = list(numpy.arange(0,0.5, 0.1))
    
    
    print('params computed')
    
    rand_search = RandomizedSearchCV(fit, param_distributions = params)
    
    X,y = metricList, densityList
    
    
    rand_search.fit(X,y)
    print(rand_search.grid_scores_)
    
    return rand_search.grid_scores_ 
def f_regression(X,Y): 
    """Helper function for getFeatures to generate regression function with desired parameters."""
    import sklearn 
    return sklearn.feature_selection.f_regression(X,Y, center=False) 
    
    
def getFeatures(features):
    """finds the k best features of the model"""
    metricList = numpy.loadtxt(open("metricListTraining.csv", "rb"), delimiter = ',')
    densityList = numpy.loadtxt(open("densityListTraining.csv", "rb"), delimiter = ',')
    metricList, scaler = scaleMetrics(metricList)  
    
      
    X,Y = metricList, densityList 
    
    featureSelector = feature_selection.SelectKBest(score_func = f_regression, k=features) 
    
    featureSelector.fit(X,Y)
    
    print [1+a for a in list(featureSelector.get_support(indices = True))]
    
