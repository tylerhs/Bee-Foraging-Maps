Table densities;
PImage densityMap;

void setup(){
  densityMap = loadImage("densityMap.jpg");
  size(densityMap.width, densityMap.height);
  densities = new Table();
  background(densityMap);
  buildTable();
  saveTable(densities, "densities3.csv");
}

void draw(){
  background(densityMap);
}

void buildTable(){
  float max = 0;
  float temp;
  for(int i=0; i<densityMap.width; i++){
    densities.addColumn();
    for(int j=0; j<densityMap.height; j++){
      temp = hue(get(i,j))/255.0;
      if(temp > max)
        max = temp;
      densities.setFloat(j,i,temp);
    }
  }
  print("Max Hue: ");
  println(max);
}
