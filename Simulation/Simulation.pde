

// USER DEFINED PARAMETERS
float maxDensity = 0.5;
float threshold = 95;
int resolution = 10;
int numBees = 1;

// GLOBALS
PImage map;
Table densities;
ArrayList<PVector> denseCoords = new ArrayList<PVector>();
PVector[] beePos = new PVector[numBees];
PVector[] beeVel = new PVector[numBees];
int w,h;

void setup(){
  // load density values
  densities = loadTable("densities.csv");
  w = densities.getColumnCount();
  h = densities.getRowCount();
  size(w, h);
  
  // setup simulation
  drawMap();
  findFlowers();
  placeBees();
}

void draw(){
  
  updatePos();
}

// draw density map using values from table
void drawMap(){
  colorMode(HSB, 100);
  for(int i=0; i<w; i++)
    for(int j=0; j<h; j++)
      set(i,j,color(densities.getFloat(j,i)*(100/maxDensity), 100,100));
}

// identify spots with flowers and store them in an ArrayList
void findFlowers(){
  for(int i=0; i<w; i += resolution)
    for(int j=0; j<h; j+= resolution)
      if(hue(get(i,j)) > threshold)
        denseCoords.add(new PVector(i,j));
}

// randomly place all the bees
void placeBees(){
  int x,y;
  colorMode(RGB);
  fill(255,255,0);
  for(int b=0; b<numBees; b++){
    x = int(random(w));
    y = int(random(h));
    beePos[b] = new PVector(
    ellipse(int(random(w)),int(random(h)),14,10);
  }
}

// update the positions of each bee using its given velocity
void updatePos(){
  for(int b=0; b<numBees; b++){
    
}
