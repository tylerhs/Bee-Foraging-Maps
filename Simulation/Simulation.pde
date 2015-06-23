
// USER DEFINED PARAMETERS
float maxDensity = 0.5;
float densThreshold = 95;
int distThreshold = 150;
int resolution = 5;
int numBees = 30;
float weightCoeff = 0.001;

// GLOBALS
PImage map;
Table densities;
ArrayList<PVector> denseCoords = new ArrayList<PVector>();
ArrayList<PVector> weightedCoords = new ArrayList<PVector>();
PVector[] beePos = new PVector[numBees];
PVector[] beeVel = new PVector[numBees];
int w,h;

void setup(){
  // load density values
  densities = loadTable("densities.csv");
  w = densities.getColumnCount();
  h = densities.getRowCount();
  
  size(w, h);
  frameRate(30);
  
  // setup simulation
  drawMap();
  findFlowers();
  placeBees();
}

void draw(){
  drawMap();
  calcVel();
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
      if(hue(get(i,j)) > densThreshold)
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
    beePos[b] = new PVector(x,y);
    beeVel[b] = new PVector(0,0);
  }
}

// calculate the velocities for each bee using its surrounding flowers
void calcVel(){
  int dist;
  int weight;
  int x, y, r;
  PVector target;
  int xDiff, yDiff;
  for(int b=0; b<numBees; b++){
    for(int f=0; f<denseCoords.size(); f++){
      x = int(denseCoords.get(f).x);
      y = int(denseCoords.get(f).y);
      dist = int(sqrt(pow(x - beePos[b].x,2) + pow(y - beePos[b].y,2)));
      if(dist < distThreshold){
        weight = int(weightCoeff*(150-dist)*hue(get(x,y)));
        //print(weight);
        //print("\t");
        for(int w=0; w<weight; w++)
          weightedCoords.add(new PVector(x,y));
      }
    }
    //println(" ");
    r = int(random(weightedCoords.size()));
    target = weightedCoords.get(r);
    xDiff = int(target.x - beePos[b].x);
    yDiff = int(target.y - beePos[b].y);
    if(xDiff == 0 || yDiff == 0)
      beeVel[b].set(0,0);
    else
      beeVel[b].set(xDiff/abs(xDiff),yDiff/abs(yDiff));
    weightedCoords.clear();
  }
}

// update the positions of each bee using its given velocity
void updatePos(){
  for(int b=0; b<numBees; b++){
    beePos[b].add(beeVel[b]);
    ellipse(beePos[b].x, beePos[b].y,14,10);
  }
}


