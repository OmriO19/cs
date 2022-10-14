//Kristoffer Pauly
//Game Project
//The Somewhat Possible Game

// create a reference to an image sequence

class Player{
  //attributes (affected by arguments)
  int _PlayerX; //x position of the player object
  int _PlayerY; //y position of the player object
  int _PlayerSize; //size of the player object
  int _startY; //starting y position of the player object, used to determine where the "floor" is

  //attributes (not affected by arguments)
  int gravity = 6; //gravity that the player object is affected by
  float jumpCounter = 0; //counter used to determine how long the jump lasts
  float jumpCounterLimit = 15; //the limit for the jumpCounter
  
  float player_current =0;
  boolean isJumping = false; //boolean used to trigger jump
  //float jumpAngle = 0; //the angle at which player object is rotated
  //float incrementAngle = PI/20; //the increment at which the jumpAngle will be changed when jumping
  
  //boolean notInAir = true; //used to determine when player object is allowed to jump
  
  ISPlayer hero;

  Player(int x, int y, int size,ISPlayer player){ //the Player object has three arguments x & y position and size
    //settings attributes to be equal to arguments that are passed in'
      // create instance and load all valid images from the data/PT_Teddy folder
 
    _PlayerX = x;
    _PlayerY = y;
    
    _PlayerSize = size;
    _startY = y; //used to determine when gravity is active
    hero = player;
    
  }
  
  void changeISPlayer(ISPlayer player){
     hero = player; 
  }
  
  
 
  /*void jump(float current){ //makes the Player jump, this will be controlled by the person playing the game
    if(notInAir){ //if the player is on the ground == true
      isJumping = true; //sets boolean to true, which triggers the jump in "physics()" 
    }
    player_current = current;
  }*/
  
  //void jump(){ //makes the Player jump, this will be controlled by the person playing the game
  //  if(notInAir){ //if the player is on the ground == true
  //    isJumping = true; //sets boolean to true, which triggers the jump in "physics()" 
  //  }
  //}
  
  //void physics(boolean keyPressed){ //is put into the "draw()" to constantly update
  //  //gravity
  //  if(_PlayerY < _startY){ //if player object's y position is less than the starting y position
  //    _PlayerY += gravity; //increment player object's y position by gravity
  //    notInAir = false; //player object is not in the air, stopping "jump()" from working
  //  }else{
  //    notInAir = true; //if player is on the "floor" = true, allowing "jump()" to work
  //  }
    
  //  //jump triggered by "jump()" method
  //  if(isJumping){
  //    _PlayerY -= 12; //increments the y position of the player simulating a jump
  //  }
  //  //breath 
  //  /*if(player_current < 0){ //when the counter reaches the limit the jump stops
  //    isJumping = false;
  //  }*/
  //  if(!keyPressed){ //when the counter reaches the limit the jump stops
  //    isJumping = false;
  //  }
  //}
  
  ////////////////////////////////////////////////////////////////// new version ############
    void jump(){ //makes the Player jump, this will be controlled by the person playing the game
      isJumping = true; //sets boolean to true, which triggers the jump in "physics()" 
    }
    
    void physics(){ //is put into the "draw()" to constantly update
    //gravity
    if(_PlayerY < _startY){ //if player object's y position is less than the starting y position
      _PlayerY += gravity; //increment player object's y position by gravity
    }
    //jump triggered by "jump()" method
    if(isJumping){
      if(_PlayerY > 100)
      {
        _PlayerY -= 12; //increments the y position of the player simulating a jump
      }

      jumpCounter += 0.5; //increments the jumpCounter, wzhich determines when to stop jumping 
    }
    if(jumpCounter >= jumpCounterLimit){ //when the counter reaches the limit the jump stops
      isJumping = false;
      jumpCounter = 0; //the counter is reset
    }
  }
  //////////////////////////////////////////////////////////////////////////////// ##########
  //get methods to use when checking for collision with obstacles
  int getX(){ 
    return _PlayerX + _PlayerSize/2; //returns the location of the player's front coordinate
  }
  int getY(){
    return _PlayerY + _PlayerSize/2; //returns the location of the players's bottom coordinate
  }
  int getSize(){
    return _PlayerSize;
  }

  void setJumpLimit(int x)
  {
    jumpCounterLimit += x;
  }
  
}
