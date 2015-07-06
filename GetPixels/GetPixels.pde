PImage bg;

void setup(){
  // load image
  bg = loadImage("TransectStitch1.jpg");
  size(bg.width, bg.height);
}
void draw(){
  background(bg);}
  
 void mouseClicked(){
  loadPixels();
  ellipse(mouseX, mouseY, 5, 5);
  print("X ", mouseX);
  println(" ");
  print("Y ", mouseY);
  println(" ");
}


//1046, 594
//460,1718
