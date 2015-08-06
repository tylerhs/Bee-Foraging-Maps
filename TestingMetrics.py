from PIL import ImageFilter
import numpy
from PIL import Image
from PIL import ImageStat
from colorsys import * 
import time
from operator import add
from sklearn import preprocessing
import matplotlib.pyplot as plt 



def getHSV((r,g,b)): 
    """A Helper function that takes in a tuple of r,g,b values for a single pixel and converts to HSV values. 
    Returns a tuple of hsv values for that pixel."""
    return rgb_to_hsv(r/255., g/255., b/255.)
def getHSVList(im): 
    im = Image.open(im)
    pix = im.load()
    width, height = im.size 
    
    HueList = []
    SatList = []
    ValList = []
    
    for i in range(width): 
        for j in range(height): 
            (r,g,b) = pix[i,j]
            (h,s,v) = rgb_to_hsv(r/255., g/255., b/255.)
            HueList += [int(h*360)]
            SatList += [int(s*100)]
            ValList += [int(v*100)] 
            
    return HueList, SatList, ValList 
    
def colorVariance(im):
    ''' calculates the diversity in color using a hue histogram'''
    
    # load image pixels
    im = Image.open(im)
    pix = im.load()
    width, height = im.size
    
    # create empty histogram to be filled with frequencies
    histogram = [0]*361
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
    plt.hist(histogram)
    return histogram, numpy.mean(histogram)

    
def satVariance(im):
    ''' calculates the diversity in color using a hue histogram'''
    
    # load image pixels
    im = Image.open(im)
    pix = im.load()
    width, height = im.size
    
    # create empty histogram to be filled with frequencies
    histogram = [0]*361
    for i in range(width):
        for j in range(height):
            (r,g,b) = pix[i,j] #pull out the current r,g,b values 
            (h,s,v) = rgb_to_hsv(r/255.,g/255.,b/255.)
            pixelSat = int(360*s)
            #build histogram
            histogram[pixelSat] += 1
    #print histogram
    # calculate standard deviation of histogram
    plt.hist(histogram)
    return histogram, numpy.mean(histogram)
    
def valVariance(im):
    ''' calculates the diversity in color using a hue histogram'''
    
    # load image pixels
    im = Image.open(im)
    pix = im.load()
    width, height = im.size
    
    # create empty histogram to be filled with frequencies
    histogram = [0]*361
    for i in range(width):
        for j in range(height):
            (r,g,b) = pix[i,j] #pull out the current r,g,b values 
            (h,s,v) = rgb_to_hsv(r/255.,g/255.,b/255.)
            pixelVal = int(360*v)
           # print pixelVal
            #build histogram
            histogram[pixelVal] += 1
    #print histogram
    # calculate standard deviation of histogram
    plt.hist(histogram)
    return histogram, numpy.mean(histogram)
    
def addHist(H1, H2): 
    #print H1
    #print H2
    newHist = [0]*len(H1)
    for i in range(len(H1)): 
        newHist[i] = H1[i] + H2[i]

    return newHist
    
def totalHueHist(imList): 
    total = [0]*361
    stdev = 0
    for im in imList: 
        a,b = colorVariance(im)
        total = addHist(total, a)
        stdev += b
    plt.figure(2)
    plt.hist(total)
    return stdev/len(imList)
    
def totalSatHist(imList): 
    total = [0]*361
    stdev = 0 
    for im in imList: 
        a,b = satVariance(im)
        total = addHist(total, a)
        stdev += b
    plt.figure(2)
    plt.hist(total)
    return stdev/len(imList)
    
def totalValHist(imList): 
    total = [0]*361
    stdev = 0 
    for im in imList: 
        a,b = valVariance(im)
        total = addHist(total, a)
        stdev += b
    plt.figure(2)
    plt.hist(total)
    return stdev/len(imList)

def makeHists(imList): 
    HueListTotal = [] 
    SatListTotal = [] 
    ValListTotal = [] 
    
    for im in imList: 
        Hue, Sat, Val = getHSVList(im) 
        HueListTotal += Hue
        SatListTotal += Sat 
        ValListTotal += Val 

    HueHist, hbins = numpy.histogram(HueListTotal)
    SatHist, sbins = numpy.histogram(SatListTotal)
    ValHist, vbins = numpy.histogram(ValListTotal)
    
    
    
    #####Plotting histograms#####################################
    #hwidth = 0.7*(hbins[1] - hbins[0])
    #hcenter = (hbins[:-1] + hbins[1:])/2 
    #plt.bar(hcenter, HueHist, align = 'center', width = hwidth)
    #plt.title('Hue Histogram')
    #plt.show()
    #
    #plt.figure(2)
    #plt.title('Saturation Histogram')
    #swidth = 0.7*(sbins[1] - sbins[0])
    #scenter = (sbins[:-1] + sbins[1:])/2 
    #plt.bar(scenter, SatHist, align = 'center', width = swidth)
    #plt.show()
    #
    #plt.figure(3)
    #plt.title('Value Histogram')
    #vwidth = 0.7*(vbins[1] - vbins[0])
    #vcenter = (vbins[:-1] + vbins[1:])/2 
    #plt.bar(vcenter, ValHist, align = 'center', width = vwidth)
    #plt.show()
    
    ##################Metric Calculations ################################
    
    valVar = numpy.var(ValListTotal)
    hueVar = numpy.var(HueListTotal)
    satVar = numpy.var(SatListTotal)
    
    valhistVar = numpy.var(ValHist)
    huehistVar = numpy.var(HueHist)
    sathistVar = numpy.var(SatHist) 
    
    print 'Hue, Sat, Val Variances are: \n', hueVar, '\n', satVar, '\n', valVar 
    
    print 'Hue, Sat, Val Histogram Variances are \n', huehistVar, '\n', sathistVar,'\n', valhistVar
    
    return ValHist
        
            
                    
def printResults(bwList, grassList, treeList): 
    
    print 'Calculating means' 
    
    bVal = totalValHist(bwList)
    gVal = totalValHist(grassList)
    tVal = totalValHist(treeList) 
    
    print 'Values are ', bVal, gVal, tVal
    
    bSat = totalSatHist(bwList)
    gSat = totalSatHist(grassList)
    tSat = totalSatHist(treeList) 
    
    print 'Saturations are ', bSat, gSat, tSat 
    
    bHue = totalHueHist(bwList)
    gHue = totalHueHist(grassList)
    tHue = totalHueHist(treeList)   
    print 'Hues are ', bHue, gHue, tHue  
    