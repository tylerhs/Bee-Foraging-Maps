from PIL import Image
import math

def divideTransect(Start, End, imageName): 
    """Takes in the pixel coordinates of a start and end for a transect. Divides into images that
        match the collected density data.""" 
        
    image = Image.open(imageName)
    ##First, calculate the length of the transect. 
        
    dim1 = Start[0] - End[0] #width
    dim2 = Start[1] - End[1] #height
    
    if dim1>dim2: 
        print 'Vertical'
        return transectVert(Start, End, image)
    else: 
        print 'Horizontal'
        imList = transectHoriz(Start, End, image)
    return imList
    
def transectHoriz(Start, End, image): 
    """Transect runs up and down in the image."""
    length = int(math.sqrt(abs(Start[0] - End[0])**2 + abs(Start[1] - End[1])**2))
    slope = abs(Start[1] - End[1])/length 
    meterSize = length/50 ##pixels/meter 
    
    imageList = []
    
 
    for i in range(Start[0], End[0], meterSize): #Go along the entire transect every meter - in pixels
        ##Starting center pixel is Start[1]. 
        ##Ending center pixel is End[1] 
        ##Slope is calculated already as slope - interpolate assuming linear
        
        centerPix = Start[1] + slope*i #Intercept + slope*number of pixels you have moved. 
        
        leftBound = centerPix - meterSize 
        rightBound = centerPix + meterSize  
        box = (leftBound,i, rightBound, i+meterSize)
        
        subIm = image.crop(box)
        imageList += [subIm] 
    
    return imageList
        
def transectVert(Start, End, image): 
    """Transect runs left and right in the image."The left end is start.""" 
    length = int(math.sqrt(abs(Start[0] - End[0])**2 + abs(Start[1] - End[1])**2)) 
    slope = (End[0] - Start[0])/float(length)
    print 'slope ', slope
    meterSize = length/50 ##pixels/meter     
    meterInc = int(math.sqrt(meterSize**2 - slope**2))
    imageList = []
    vertMeterSize = math.ceil((End[1] - Start[1])/50.)
    vertMeterSize = int(vertMeterSize)
    print 'Meter size is ', meterSize
    print 'Meter incremenents (vertically) are ', meterInc 
    print 'Vertical Distance is ', Start[1] - End[1] 
    
    for i in range(Start[1], End[1], vertMeterSize): #Go along the entire transect every meter - in pixels
        ##Starting center pixel is Start[1]. 
        ##Ending center pixel is End[1] 
        ##Slope is calculated already as slope - interpolate assuming linear
        centerPix = Start[0] + int(slope*(i-Start[1])) #Intercept + slope*number of pixels you have moved. 
     #   print 'Center Pixel is ', centerPix
        leftBound = centerPix - meterSize 
        rightBound = centerPix + meterSize 
        box = (leftBound, i, rightBound, i+meterSize)
        subIm = image.crop(box)
        imageList += [subIm] 
    print 'Final i is ', i 
    print 'final center pix is ', centerPix
    print 'Length is ', len(imageList)
    return imageList

def main(): 
    ####//1046, 594
######//460,1718*/
    imageName = 'TransectStitch1.jpg'
    #End = (594, 1046)
    #Start = (1718, 460)

    Start = (1035,588)
    End = (456,1720)

  #  Start = tuple(raw_input('Please Input Start Coordinates'))
   # End  = tuple(raw_input('Please Input End Coordinates'))
   
    stuff= divideTransect(Start, End, imageName)
  #  stuff[-1].show()
    if len(stuff) != 50: 
        print "Error! Transect length is not 50 meters." 
    return stuff