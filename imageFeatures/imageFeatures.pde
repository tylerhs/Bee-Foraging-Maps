
PImage bg;
int y;

// list of clicked pixels
color[] pixelList = new color[100];

boolean reset = false;
int count = 0;

// pixel statistics
int maxHue;
int minHue = 255;
int maxSat;
int minSat = 255;
int maxVal;
int minVal = 255;
int totalHue;
int totalSat;
int totalVal;
int avgHue;
int avgSat;
int avgVal;

void setup(){
  // load image
  bg = loadImage("FirstStitchSmall.jpeg");
  size(bg.width, bg.height);
}

void draw(){
  background(bg);
  // if spacebar is pressed, start analyzing pixels
  if(reset){
    if(count == 0){
      println("ADD MORE POINTS!");
      reset = false;
    }
    else{
      // loop across all clicked pixels
      for(int i=0; i<count; i++){
        // update min/max pixel values
        if(hue(pixelList[i]) > maxHue)
          maxHue = int(hue(pixelList[i]));
        if(hue(pixelList[i]) < minHue)
          minHue = int(hue(pixelList[i]));
        if(saturation(pixelList[i]) > maxSat)
          maxSat = int(saturation(pixelList[i]));
        if(saturation(pixelList[i]) < minSat)
          minSat = int(saturation(pixelList[i]));
        if(brightness(pixelList[i]) > maxVal)
          maxVal = int(brightness(pixelList[i]));
        if(brightness(pixelList[i]) < minVal)
          minVal = int(brightness(pixelList[i]));
        
        //count total values for averaging
        totalHue += hue(pixelList[i]);
        totalSat += saturation(pixelList[i]);
        totalVal += brightness(pixelList[i]);
      }
      // compute average values
      avgHue = totalHue/count;
      avgSat = totalSat/count;
      avgVal = totalVal/count;
      
      // print errthang
      print("Number of Points: ");
      println(count);
      println(" ");
      println("\tHue\tSat\tVal");
      print("Min:\t");
      print(minHue);
      print("\t");
      print(minSat);
      print("\t");
      println(minVal);
      print("Avg:\t");
      print(avgHue);
      print("\t");
      print(avgSat);
      print("\t");
      println(avgVal);
      print("Max:\t");
      print(maxHue);
      print("\t");
      print(maxSat);
      print("\t");
      println(maxVal);
      println(" ");
      
      // reset list of pixels and values
      pixelList = new color[100];
      resetValues();
      reset = false;
    }
  }
}

// if mouse is clicked, add pixel color to list
void mouseClicked(){
  loadPixels();
  ellipse(mouseX, mouseY, 5, 5);
  pixelList[count] = pixels[mouseX+bg.width*mouseY];
  count++;
}

// if spacebar is pressed, analyze pixels and reset
void keyPressed(){
  if(key == ' '){
    reset = true;
  }
}

// reset all statistic values
void resetValues(){
  maxHue = 0;
  minHue = 255;
  maxSat = 0;
  minSat = 255;
  maxVal = 0;
  minVal = 255;
  totalHue = 0;
  totalSat = 0;
  totalVal = 0;
  avgHue = 0;
  avgSat = 0;
  avgVal = 0;
  count = 0;
}
