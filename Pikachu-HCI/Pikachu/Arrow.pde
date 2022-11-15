class Arrow{
  //attributes (affected by arguments)
  int _ArrowX; //x position of the top left corner of object
  int _ArrowY; //y position of the top left corner of object
  int _ArrowSize; //size of the player object
  PImage _Arrow;

  Arrow(int x, int y, int size, PImage arrow){ //the Arrow object has 4 arguments x & y position, size and rendable image
    //settings attributes to be equal to arguments that are passed in'
      // create instance and load all valid images from the data/PT_Teddy folder
    _ArrowX = x;
    _ArrowY = y;
    _ArrowSize = size;    
    _Arrow = arrow;
    //image(_Arrow, _ArrowX, _ArrowY, size, size);
  }
  
  void changeCoords(int x, int y){
    _ArrowX = x;
    _ArrowY = y; 
    image(_Arrow, _ArrowX, _ArrowY, _ArrowSize, _ArrowSize);
  }
 
}
