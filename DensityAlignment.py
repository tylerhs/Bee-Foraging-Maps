from PIL import Image

def divideTransect(Start, End, imageName): 
    """Takes in the pixel coordinates of a start and end for a transect. Divides into images that
        match the collected density data.""" 
        
    image = Image.open(imageName)
    ##First, calculate the length of the transect. 
        
    dim1 = abs(Start[0] - End[0]) #width
    dim2 = abs(Start[1] - End[1]) #height
    
    if dim1>dim2: 
        print 'Vertical'
        return transectVert(Start, End, image)
    else: 
        print 'Horizontal'
        imList = transectHoriz(Start, End, image)
    return imList
    
def transectHoriz(Start, End, image): 
    """Transect runs up and down in the image."""
    length = abs(Start[0] - End[0]) 
    slope = abs(Start[1] - End[1])/length 
    meterSize = length/50 ##pixels/meter 
    
    imageList = []
    
    print 'I tried.'
    
 
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
    length = abs(End[1] - Start[1]) 
    slope = abs(Start[0] - End[0])/length 
    meterSize = length/50 ##pixels/meter 
    
    imageList = []
    print Start[1], End[1], meterSize
    for i in range(Start[1], End[1], meterSize): #Go along the entire transect every meter - in pixels
        ##Starting center pixel is Start[1]. 
        ##Ending center pixel is End[1] 
        ##Slope is calculated already as slope - interpolate assuming linear
        
        centerPix = Start[0] + slope*i #Intercept + slope*number of pixels you have moved. 
        
        leftBound = centerPix - meterSize 
        rightBound = centerPix + meterSize 
      #  print 'found bound'
        box = (leftBound, i, rightBound, i+meterSize)
        
        subIm = image.crop(box)
        imageList += [subIm] 
     #   print subIm
    return imageList
    

def main(): 
    ####//1046, 594
######//460,1718*/
    imageName = 'TransectStitch1.jpg'
    End = (594, 1046)
    Start = (1718, 460)

  #  Start = tuple(raw_input('Please Input Start Coordinates'))
   # End  = tuple(raw_input('Please Input End Coordinates'))
   
    return divideTransect(Start, End, imageName)
    