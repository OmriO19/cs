//Kristoffer Pauly
//Game Project
//The Somewhat Possible Game

class Obstacle{
  //attributes
  int _startX;
  int _spikeX;
  int _spikeY;
  int _squareX;
  int _squareY;
  int _speed;
  boolean _ignore;
  PImage _ball;
  PImage _spike;

  
  Obstacle(int x, PImage ball, PImage spike){ //has only one argument, which startX, squareX and spikeX are all set according to
    _startX = x;
    _squareX = _startX;
    _spikeX = _startX;
    _ignore = false;
    _ball = ball;
    _spike = spike;
  }
  
  void spike(int y){ //spike obstacle (lethal from front and on top)
    _spikeY = y; //the y coordinate of the obstacle, set according to the argument in the constructor
    //strokeWeight(2);
    //stroke(150);
    //fill(0);
    //triangle(_spikeX, _spikeY, _spikeX+30, _spikeY, _spikeX+15, _spikeY-50);
    _spikeX -= _speed;
    image(_spike,_spikeX-50+20, y-50,width/10,height/10);
  }
  
  void spike_long(int y){
        _spikeY = y; //the y coordinate of the obstacle, set according to the argument in the constructor
    //strokeWeight(2);
    //stroke(150);
    //fill(0);
    //triangle(_spikeX, _spikeY, _spikeX+30, _spikeY, _spikeX+15, _spikeY-50);
    _spikeX -= _speed;
    image(_spike,_spikeX-50+20, y-height/4+10,width/10,height/4);
  }
  
  void square(int y){ //square obstacle (lethal from the front, safe on top)
    _squareY = y; //the y coordinate of the obstacle, set according to the argument in the constructor
    //rectMode(CENTER);
    //strokeWeight(2);
    //stroke(150);
    //fill(0);
    //rect(_squareX, _squareY, 50, 50); 
    _squareX -= _speed;
    image(_ball,_squareX-50+25, y-50+17,width/20,height/16);
  }
  
  void spikeDown(int y){
    _spikeY = y; //the y coordinate of the obstacle, set according to the argument in the constructor
    //strokeWeight(2);
    //stroke(150);
    //fill(0);
    //triangle(_spikeX, _spikeY, _spikeX+30, _spikeY, _spikeX+15, _spikeY-50);
    _spikeX -= _speed;
    pushMatrix();
    scale(1,-1);
    image(_spike,_spikeX-50+20, -height/2,width/10,height/2);
    popMatrix();

    //scale(1,1);
  }
  
  void ignore(){ //used to make Player object able to jump on square Obstacle
    _ignore = true;
  }
  
//get methods to use when checking for collision with Player object
  //for the spike obstacle
  int spikeGetX1(){
    return _spikeX+5; //returns front coordinate of the spike 
  }
  int spikeGetX2(){
    return _spikeX+75; //returns back coordinate of the spike 
  }
  int spikeGetY1(){
    return _spikeY-50; //returns top coordinate of the spike
  }
  int spikeGetY2(){
    return _spikeY; //returns bottom coordinate of the spike
  }
  
  //for the square obstacle
  int squareGetX1(){ //returns front coordinate of the square
    return _squareX-25;
  }
  int squareGetX2(){ //returns back coordinate of the square
    return _squareX+75;
  }
  int squareGetY1(){ //returns top coordinate of the square
    return _squareY-25;
  }
  int squareGetY2(){ //returns bottom coordinate of the square
    return _squareY+25;
  }
  
  void move(int speed){ //determines the speed which the obstacles move along the x-axis with
    _speed = speed;
  }
}
