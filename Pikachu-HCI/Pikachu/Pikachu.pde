
import ddf.minim.*;
import ddf.minim.analysis.*;
import ddf.minim.effects.*;
import ddf.minim.signals.*;
import ddf.minim.spi.*;
import ddf.minim.ugens.*;



import com.hirschandmann.image.*;
// create a reference to an image sequence
ISPlayer pikachu_render, character_0_render, character_1_render, character_2_render, character_3_render;


import processing.serial.*;    // Importing the serial library to communicate with the Arduino 

Serial myPort;      // Initializing a vairable named 'myPort' for serial communication
PImage img, ball, spike, ball2, arrow;


//delaring obstacles
Obstacle[] obstacles = new Obstacle[300]; //As you may guess, yes, there are A LOT of obstacles.
//Note that not all 300 obstacle objects are actually used, however, it's nice to have more than
//necessary, just in case you want to add more obstacles.

//declaring global variables
int timer = 0; //used for score and timing obstacles
int deathCounter = 0; //used to track deaths (manually resetting counts as well)
int highScore = 0; //creating counter used to show the player's highscore
int fade = 0; //used to fade to dark when player wins
int score = 0;
int max_score = 0;
int total_score = 0;
int hard_completed = 0;
int diff_menu = 0; //flag if the game in difficulty menu
int character_menu = 0;
int character = 0;
int menu = 1; //flag if the game in menu
int menuBox = 0;
int difficulty = 0; // default on easy, 0 is easy, 1 is medium, 2 is hard
int exit_game = 0;
int death = 0;
int win = 0;
Player hero;
boolean flag = false;


AudioPlayer backgroundMusic;
AudioPlayer deathNoise;
Minim minim;


void setup(){
  size(1000, 600);
  img = loadImage("bg.png");
  ball = loadImage("pokeball3.png");
  ball2 = loadImage("pokeball3.png");;
  ball2.filter(GRAY);
  spike = loadImage("spike.png");
  arrow = loadImage("arrow.png");
  
  pikachu_render = new ISPlayer(this,dataPath("character/pika"));
  pikachu_render.setDelay(1000/12);
  character_0_render = new ISPlayer(this,dataPath("character/pika"));
  character_0_render.setDelay(1000/12);
  character_1_render = new ISPlayer(this,dataPath("character/pika_1"));
  character_1_render.setDelay(1000/12);
  character_2_render = new ISPlayer(this,dataPath("character/pika_2"));
  character_2_render.setDelay(1000/12);
  character_3_render = new ISPlayer(this,dataPath("character/pika_3"));
  character_3_render.setDelay(1000/12);
  
  hero = new Player(150, 524, 50,pikachu_render);
  minim = new Minim(this);
  backgroundMusic = minim.loadFile("Dance of the Pixies.mp3", 5048);
  deathNoise = minim.loadFile("Death Noise.wav", 5048);

  // Activate if using the arduino model 
  // ###
  //myPort  =  new Serial (this, "/dev/cu.usbserial-1420",  9600); // Set the com port and the baud rate according to the Arduino IDE
  //myPort.bufferUntil ( '\n' );   // Receiving the data from the Arduino IDE
  // ###
  //initialising obstacles
  for(int i = 0; i < 300; i++){
    obstacles[i] = new Obstacle(1000, ball, spike); //set to 1000, which is the right-most edge of the screen
  }
}

void draw(){

  //background
  scenery();
  //song on
  backgroundMusic.play();
  
  //obstacles
  for(int i = 0; i < 300; i++){
    obstacles[i].move(4); //initialises the move speed for all obstacles
  }
  Arrow arr = new Arrow(420, 175 ,30, arrow);
  if (exit_game == 1){
     exit();
  }
  else if(menu == 1){
      int menuC = menuColor();
      displayMenu(menuC);
      displayArrow(arr);
  }
  else if(character_menu == 1){
      displayCharacterMenu();
  }
  else if(diff_menu == 1){
    int diffC = difficultyColor();
    displayDiffMenu(diffC);
    displayArrow(arr);
  }
  else{
    if(win == 1){
       displayWin(); 
    }
    else if(death == 1){
        displayDeath();
    }
    else{
      switch(difficulty){
        case 0: //easy
            obstacleSpawnEasy(); //spawns the obstacles (based on timer)
            break;
        case 1: //medium
            obstacleSpawnMedium();
            break;
        case 2: //hard
            obstacleSpawnHard();
            break; 
      }
      /*
      switch(character){
         case 0:
             pikachu_render = new ISPlayer(this,dataPath("character/pika"));
             break;
         case 1:
             pikachu_render = new ISPlayer(this,dataPath("character/pika_1"));
             break;
         case 2:
             pikachu_render = new ISPlayer(this,dataPath("character/pika_2"));
             break;
         case 3:
             pikachu_render = new ISPlayer(this,dataPath("character/pika_3"));
             break;
         
      }
      pikachu_render.setDelay(1000/12);
      */
      image(pikachu_render,hero.getX()-hero.getSize()-10,hero.getY()-hero.getSize()-10,width/10,height/10);
      collision(); //checks collisions between obstacles and hero
      
      //hero
      hero.physics();
      
      //timer, scoreboard and control display
      timer();
      scoreboard(); 
      displayControls();
    }
  }
}


// image sequence events
// first frame loaded (e.g. can pause and render first frame while the rest load)
void firstFrameLoaded(ISPlayer player){
  //println(player+" first frame loaded");
}

// all frames loaded
void onSequenceLoaded(ISPlayer player){
  //println(player+" sequence fully loaded");
  player.loop();
}

// triggered when an sequence finished playing
void onSequencePlayed(ISPlayer player){
  //println(player+" sequence played");
}

void serialEvent  (Serial myPort) {
  float val =  float (myPort.readStringUntil ( '\n' ) );
  //println(val);
  if(val> 0){
    hero.jump();
  }
  
} 



void mouseClicked(){
  if(menu == 1){
      if(mouseButton == LEFT){
        if(mouseX > 425 && mouseX < 575 && mouseY > 180 && mouseY < 220){
          menu = 0;
          diff_menu = 1;
        }
        if(mouseX > 430 && mouseX < 570 && mouseY > 225 && mouseY < 270){
          menu = 0;
          character_menu = 1;
        }
        if(mouseX > 475 && mouseX < 525 && mouseY > 275 && mouseY < 325){
          menu = 0;
          exit_game = 1;
        }
    }
  }
  else if(character_menu == 1){
      if(mouseButton == LEFT){
        if(mouseX > 150 && mouseX < 150+width/10 && mouseY > 250 && mouseY < 250 + height/10){
          pikachu_render = new ISPlayer(this,dataPath("character/pika"));
          pikachu_render.setDelay(1000/12);
          character_menu = 0;
          menu = 1;
        }
        if(mouseX > 150+2*width/10 && mouseX < 150+2*width/10+width/10 && mouseY < 250 + height/10 && max_score >= 20){
          pikachu_render = new ISPlayer(this,dataPath("character/pika_1"));
          pikachu_render.setDelay(1000/12);
          character_menu = 0;
          menu = 1;
        }
        if(mouseX > 150+4*width/10 && mouseX < 150+4*width/10+width/10 && mouseY < 250 + height/10 && total_score >= 100){
          pikachu_render = new ISPlayer(this,dataPath("character/pika_2"));
          pikachu_render.setDelay(1000/12);
          character_menu = 0;
          menu = 1;
        }
        if(mouseX > 150+6*width/10 && mouseX < 150+6*width/10+width/10 && mouseY < 250 + height/10 && hard_completed == 1){
          pikachu_render = new ISPlayer(this,dataPath("character/pika_3"));
          pikachu_render.setDelay(1000/12);
          character_menu = 0;
          menu = 1;
        }
      }
  }
  else if(diff_menu == 1){
    if(mouseButton == LEFT){
      if(mouseX > 480 && mouseX < 520 && mouseY > 180 && mouseY < 220){
        difficulty = 0;
        diff_menu = 0;
      }
      if(mouseX > 450 && mouseX < 550 && mouseY > 225 && mouseY < 270){
        difficulty = 1;
        diff_menu = 0;
      }
      if(mouseX > 480 && mouseX < 520 && mouseY > 275 && mouseY < 325){
        difficulty = 2;
        diff_menu = 0;
      }
    }
  }
}



void keyPressed(){
  if(win == 1){
     switch(key){
       case ENTER:
         menu = 1;
         win = 0;
         difficulty = 0;
         break;
       case ' ':
         win = 0;
         break;
     }
  }
  else if(death == 1){
     switch(key){
       case ENTER:
         menu = 1;
         death = 0;
         difficulty = 0;
         break;
       case ' ':
         death = 0;
         break;
     }
  }
  else if(menu == 1){
    if(key == CODED){
       switch(keyCode){
         case UP:
           menuBox = (menuBox - 1);
           if (menuBox < 0)
             menuBox += 3;
           break;
         case DOWN:
           menuBox = (menuBox + 1) % 3;
           break;
       }
    }
    else{
      switch(key){
         case ENTER:
           switch(menuBox){
             case 0:
               diff_menu = 1;
               menu = 0;
               break;
             case 1:
               character_menu = 1;
               menu = 0;
               break;
             case 2:
               exit_game = 1;
               menu = 0;
               break;
           }
         break;
         case ' ':
           switch(menuBox){
             case 0:
               diff_menu = 1;
               menu = 0;
               break;
             case 1:
               character_menu = 1;
               menu = 0;
               break;
             case 2:
               exit_game = 1;
               menu = 0;
               break;
           }
      }
    }
  }
  else if(diff_menu == 1){
    if(key == CODED){
       switch(keyCode){
         case UP:
           difficulty = (difficulty - 1);
           if (difficulty < 0)
             difficulty += 3;
           break;
         case DOWN:
           difficulty = (difficulty + 1) % 3;
           break;
       }
    }
    else{
      switch(key){
         case ENTER:
           diff_menu = 0;
           break;
         case ' ':
           diff_menu = 0;
           break; 
      }
    }
  }
  if(diff_menu != 1 && menu != 1)
  {
    switch(key){
      //jump (using W)
    case 'w': //when 'w' is pressed
      hero.jump();
      break;
      
      //jump (using Spacebar)
    case ' ': //when spacebar is pressed
      hero.setJumpLimit(2);
      hero.jump();
      break;
    }
    switch(keyCode){
      //jump (using Up Arrow key)
    case UP: //when 'Up arrow' is pressed
      hero.jump();
      break;
    }
  }
}

void collision(){
  //collision with spike
  for(int i = 0; i < 300; i++){
    if(hero.getX() > obstacles[i].spikeGetX1() && hero.getX() < obstacles[i].spikeGetX2()){
      if(hero._PlayerY > obstacles[i].spikeGetY1() && hero._PlayerY < obstacles[i].spikeGetY2()){
        //println("Death by Spike");
        backgroundMusic.pause();
        deathNoise.play();
    
        delay(1000);
        deathNoise.rewind();
        reset();
        reset();
      }
    }
    //collision with square
    if(hero.getX() > obstacles[i].squareGetX1() && hero.getX() < obstacles[i].squareGetX2()){
      ////if player hits the front of the square
      if(hero._PlayerY > obstacles[i].squareGetY1() && hero._PlayerY < obstacles[i].squareGetY2()){

      //if(hero.getY() < obstacles[i].squareGetY1()){ //if player hits top of the square
        hero._startY = obstacles[i].squareGetY1()-26;
        if(!obstacles[i]._ignore)
        {
          score += 1;
          //println(score);
          obstacles[i]._ball = ball2;
          // Activate if using the arduino model
          //myPort.write("255\n");
        }
        obstacles[i].ignore();
    }
    }
    if(hero.getX() > obstacles[i].squareGetX2()){ //resets the "floor" value
      hero._startY = 524;
      obstacles[i].ignore(); //sets _ignore to true
    }
  }
}

void timer(){ //timer used to determine score and obstacle spawning
//Note to self: song length is 12000 on the timer
  timer += 1;
  //println(timer); //print of the timer, useful for when you are adding obstacles in the spawner
}

void reset(){ //resets the game back to the beginning

  //replays music from start
  backgroundMusic.rewind();
  //resets timer
  total_score += score;
  if(max_score < score){
    max_score = score;
  }
  timer = 0;
  score = 0;
  //resets obstacles
  for(int i = 0; i < 300; i++){
    obstacles[i] = new Obstacle(1000, ball, spike);
  }
  //resets "floor"
  hero._startY = 524;
  //increments death counter (used to track deaths)
  deathCounter += 1;
  //reset win fade
  death = 1;
  menuBox = 0;
  fade = 0;
}

void winReset(){ //resets the game back to the beginning
  //replays music from start
  //backgroundMusic.stop();
  //backgroundMusic.play();
  //resets timer
  total_score += score;
  if(max_score < score){
    max_score = score;
  }
  if(difficulty == 2){
     hard_completed = 1; 
  }
  timer = 0;
  score = 0;
  //resets obstacles
  for(int i = 0; i < 300; i++){
    obstacles[i] = new Obstacle(1000, ball, spike);
  }
  //resets "floor"
  hero._startY = 524;
  //increments death counter (used to track deaths)
  //reset win fade
  win = 1;
  menuBox = 0;
  fade = 0;
}

void scoreboard(){ //scoreboard that tracks longest travelled distance
  if(score > highScore){
    highScore = score;
  }
  textAlign(CENTER);
  //highscore display
  textSize(35);
  fill(0);
  
  text("Highscore: "+highScore, 800, 50); //highscore is divided by 60 so each second = 1 point
  //death counter display
  //fill(255);
  //textSize(45);
  //text(deathCounter, 500, 60);
}

int menuColor(){
   if(mouseX > 425 && mouseX < 575 && mouseY > 180 && mouseY < 220){
      return 1;
   }
   if(mouseX > 430 && mouseX < 570 && mouseY > 225 && mouseY < 270){
      return 2;
   }
   if(mouseX > 475 && mouseX < 525 && mouseY > 275 && mouseY < 325){
     return 3;
   }
   return 0;
} 


int difficultyColor(){
   if(mouseX > 480 && mouseX < 520 && mouseY > 180 && mouseY < 220){
      return 1;
   }
   if(mouseX > 450 && mouseX < 550 && mouseY > 225 && mouseY < 270){
      return 2;
   }
   if(mouseX > 480 && mouseX < 520 && mouseY > 275 && mouseY < 325){
     return 3;
   }
   return 0;
}

int characterBoxColor(){
    if(mouseX > 150 && mouseX < 150+width/10 && mouseY > 250 && mouseY < 250 + height/10){
      return 0;
    }
    if(mouseX > 150+2*width/10 && mouseX < 150+2*width/10+width/10 && mouseY < 250 + height/10){
      return 1;
    }
    if(mouseX > 150+4*width/10 && mouseX < 150+4*width/10+width/10 && mouseY < 250 + height/10){
      return 2;
    }
    if(mouseX > 150+6*width/10 && mouseX < 150+6*width/10+width/10 && mouseY < 250 + height/10){
      return 3;
    }
    return -1;
}

void displayCharacterMenu(){
  textAlign(CENTER);
  textSize(35);
  fill(0);
  text("Characters", 500, 50);
  int box_color = characterBoxColor();
  noFill();
  textSize(20);
  
  // display character_0
  if(box_color == 0){
    stroke(255,0,0);
    strokeWeight(6);
  }
  rect(150,250, width/10 ,height/10, 3, 3, 3, 3);
  stroke(0,0,0);
  strokeWeight(4);
  image(character_0_render,150, 250,width/10,height/10);

  
 
  //display character_1
  if(max_score >= 20){
     if(box_color == 1){
      stroke(255,0,0);
      strokeWeight(6);
     }
     noFill();
     rect(150+2*width/10,250, width/10 ,height/10, 3, 3, 3, 3);
     stroke(0,0,0);
     strokeWeight(4);
    image(character_1_render,150+2*width/10,250,width/10,height/10);
  } else {
      fill(0);
      rect(150+2*width/10,250, width/10 ,height/10, 3, 3, 3, 3);
      text("Score 20", 200+2*width/10,250+1.5*height/10);
      text("in one game", 200+2*width/10,280+1.5*height/10);
      text("to unlock", 200+2*width/10,310+1.5*height/10);
      
  }
  
  //display character_2
  if(total_score >= 100){
    if(box_color == 2){
      stroke(255,0,0);
      strokeWeight(6);
    }
     noFill();
     rect(150+4*width/10,250, width/10 ,height/10, 3, 3, 3, 3);
     stroke(0,0,0);
     strokeWeight(4);
     image(character_2_render,150+4*width/10,250,width/10,height/10);
  } else {
      fill(0);
      rect(150+4*width/10,250, width/10 ,height/10, 3, 3, 3, 3);
      text("Collect", 200+4*width/10,250+1.5*height/10);
      text("100 pokeballs", 200+4*width/10,280+1.5*height/10);
      text("to unlock", 200+4*width/10,310+1.5*height/10);
      //text("Collect 100 pokeballs to unlock", 150+2*width/10,250);
  }
  
  //display character_3
  if(hard_completed == 1){
     if(box_color == 3){
      stroke(255,0,0);
      strokeWeight(6);
    }
    noFill();
    rect(150+6*width/10,250, width/10 ,height/10, 3, 3, 3, 3);
    stroke(0,0,0);
    strokeWeight(4);
    image(character_3_render,150+6*width/10, 250,width/10,height/10);
  } else {
    fill(0);
    rect(150+6*width/10,250, width/10 ,height/10, 3, 3, 3, 3);
    text("Complete", 200+6*width/10,250+1.5*height/10);
    text("hard mode", 200+6*width/10,280+1.5*height/10);
    text("to unlock", 200+6*width/10,310+1.5*height/10);
    //text("Complete hard mode to unlock", 150+2*width/10,250);
  }
  
}

void displayMenu(int chosen_box){
  textAlign(CENTER);
  textSize(35);
  fill(0);
  text("Press Enter to continue", 500, 50);

  textSize(35);
  if(chosen_box == 1)
    fill(255,0,0);
  else
    fill(0);
  text("New game", 500, 200);
  

  textSize(35);
  if(chosen_box == 2)
    fill(255,0,0);
  else
    fill(0);
  text("Character", 500, 250);
  
  
  textSize(35);
  if(chosen_box == 3)
    fill(255,0,0);
  else
    fill(0);
  text("Exit", 500, 300);
    
}

void displayDiffMenu(int diff){
  
  textAlign(CENTER);
  textSize(35);
  fill(0);
  text("Choose difficulty", 500, 50);

  textSize(35);
  if(diff == 1)
    fill(255,0,0);
  else
    fill(0);
  text("Easy", 500, 200);
  

  textSize(35);
  if(diff == 2)
    fill(255,0,0);
  else
    fill(0);
  text("Medium", 500, 250);
  
  
  textSize(35);
  if(diff == 3)
    fill(255,0,0);
  else
    fill(0);
  text("Hard", 500, 300);
    
}

void displayArrow(Arrow arr){
  if (menu == 1){
      switch (menuBox){
        case 0: //easy
          arr.changeCoords(380, 175);
          break;
        case 1:
          arr.changeCoords(385, 225);
          break;
        case 2:
          arr.changeCoords(430, 275);
          break; 
    }
  }
  else if(diff_menu == 1)
  {
    switch (difficulty){
      case 0: //easy
        arr.changeCoords(425, 175);
        break;
      case 1:
        arr.changeCoords(400, 225);
        break;
      case 2:
        arr.changeCoords(422, 275);
        break; 
    }
  }
    
}

void displayDeath(){
  textAlign(CENTER);
  textSize(50);
  fill(0);
  text("YOU DIED!", 500,150);
  
  textSize (35);
  text("Press Enter to return to main menu", 500, 250);
  text("Press Space to play again", 500, 300);
}

void displayWin(){
  textAlign(CENTER);
  textSize(50);
  fill(random(255), random(255), random(255));
  text("You Win!", 500, 150);
  
  fill(0);
  textSize (35);
  text("Press Enter to return to main menu", 500, 250);
  text("Press Space to play again", 500, 300); 
}

void displayControls(){
  //displays controls until the timer reaches 250, i.e. until encountering the first obstacle
  if(timer < 250){
    textAlign(CENTER);
    textSize(35);
    fill(0);
    
    text("JUMP with SPACE", 220, 50);
    // hebrew
    //text("נשוף כדי לקפוץ", 220, 50);

  }else{ //displays current score
    textAlign(CENTER);
    textSize(35);
    fill(0);
    
    text("Current score: "+ score, 200, 50);
    // hebrew
    // text("ניקוד: "+ score, 200, 50);
  }
}

void scenery(){ //this covers up the entire window, making an actual "background()" unnessecary
  //background (has several colour changes and ellipses to imitate a setting sun)
  
  image(img,0,-40); // Using instead of background();
}

void gameComplete(){
  //fades to black by acting as an increasing alpha for the rect that covers the screen
  /*noStroke();
  fill(0, 0, 0, fade);
  rectMode(CENTER);
  rect(500, 300, 1000, 600);
  fade += 1;*/
  //you win text
  winReset();
  
  // hebrew
  //text("תפסת את כולם!!!", 500, 300);
}

void obstacleSpawnEasy(){ //spawns the obstacles based on the timer (this part of the code is incredibly long)
/*
Notes to self: 
- floor is 525 (square) and 550 (spike)
- good timer distance for linked objects 12 (square) and 8 (spike)
- nearly 1200 lines of code for this part D:
*/
  if(timer > 150){
    obstacles[1].spike(550);
  }

  if(timer > 350){
    obstacles[3].spike(550);
  }
  if(timer > 525){
    obstacles[5].spike(550);
  }
  if(timer > 600){
    obstacles[6].spike(550);
  }
  //===============(600 = 10s)===============
  if(timer > 675){
    obstacles[7].spike(550);
  }

  if(timer > 750){
    obstacles[1].square(525);
  }
  if(timer > 780){
    obstacles[2].square(475);
  }
  if(timer > 810){
    obstacles[3].spike(550);
  }
  if(timer > 845){
    obstacles[4].square(375);
  }

  if(timer > 858){
    obstacles[10].spike(550);
  }


  if(timer > 882){
    obstacles[13].spike(550);
  }
  if(timer > 930){ 
    obstacles[6].square(375);
  }

  if(timer > 1005){
    obstacles[15].spike(550);
  }
  if(timer > 1080){ 
    obstacles[7].square(525);
  }
  if(timer > 1120){ 
    obstacles[8].square(475);
  }

  if(timer > 1200){ 
    obstacles[10].square(475);
  }
  //===============(1200 = 20s)===============
  if(timer > 1240){ 
    obstacles[11].square(525);
  }
  if(timer > 1276){ 
    obstacles[16].spike(450);
  }
  if(timer > 1280){ 
    obstacles[12].square(475);
  }

  if(timer > 1338){
    obstacles[17].spike(550);
  }
  if(timer > 1346){
    obstacles[18].spike(550);
  }

  if(timer > 1450){ 
    obstacles[14].square(525);
  }
  if(timer > 1500){ 
    obstacles[15].square(475);
  }
  if(timer > 1524){ 
    obstacles[16].spike(550);
  }

  if(timer > 1650){
    obstacles[22].spike(550);
  }

  if(timer > 1690){
    obstacles[24].spike(550);
  }
  if(timer > 1698){
    obstacles[25].spike(550);
  }

  if(timer > 1775){
    obstacles[28].spike(550);
  }
  //===============(1800 = 30s)===============
  if(timer > 1830){
    obstacles[29].spike(550);
  }
  if(timer > 1838){
    obstacles[30].spike(550);
  }
  if(timer > 1870){
    obstacles[31].spike(550);
  }
  if(timer > 1878){
    obstacles[32].spike(550);
  }
  if(timer > 1940){
    obstacles[33].spike(550);
  }
  if(timer > 2000){
    obstacles[34].spike(550);
  }
  if(timer > 2008){
    obstacles[35].spike(550);
  }
  if(timer > 2040){
    obstacles[36].spike(550);
  }
  if(timer > 2048){
    obstacles[37].spike(550);
  }
  if(timer > 2080){
    obstacles[38].spike(550);
  }
  if(timer > 2088){
    obstacles[39].spike(550);
  }
  if(timer > 2160){ 
    obstacles[17].square(525);
  }
  if(timer > 2200){ 
    obstacles[18].square(475);
  }
  if(timer > 2220){
    obstacles[40].spike(500);
    obstacles[41].spike(550);
  }
  if(timer > 2240){ 
    obstacles[19].square(475);
  }
  if(timer > 2275){ 
    obstacles[20].square(425);
  }
  if(timer > 2310){ 
    obstacles[21].square(375);
  }
  if(timer > 2345){ 
    obstacles[22].square(325);
  }
  if(timer > 2365){ 
    obstacles[23].square(375);
  }
  if(timer > 2400){ 
    obstacles[24].square(325);
  }
  //===============(2400 = 40s)===============
  if(timer > 2414){ 
    obstacles[42].spike(550);
  }
  if(timer > 2422){ 
    obstacles[43].spike(550);
  }
  if(timer > 2430){ 
    obstacles[44].spike(550);
  }
  if(timer > 2438){ 
    obstacles[45].spike(550);
  }
  if(timer > 2550){ 
    obstacles[25].square(525);
  }
  if(timer > 2590){ 
    obstacles[26].square(475);
  }
  if(timer > 2630){ 
    obstacles[27].square(525);
  }
  if(timer > 2670){ 
    obstacles[28].square(475);
  }
  if(timer > 2706){ 
    obstacles[46].spike(550);
  }
  if(timer > 2714){ 
    obstacles[47].spike(550);
  }
  if(timer > 2760){ 
    obstacles[29].square(525);
  }
  if(timer > 2800){ 
    obstacles[30].square(475);
  }
  if(timer > 2840){ 
    obstacles[31].square(525);
  }
  if(timer > 2880){ 
    obstacles[32].square(475);
  }
  if(timer > 2916){ 
    obstacles[48].spike(550);
  }
  if(timer > 2924){ 
    obstacles[49].spike(550);
  }
  if(timer > 2970){ 
    obstacles[33].square(525);
  }
  //===============(3000 = 50s)===============
  if(timer > 3010){ 
    obstacles[34].square(475);
  }
  if(timer > 3050){ 
    obstacles[35].square(525);
  }
  if(timer > 3090){ 
    obstacles[36].square(475);
  }
  if(timer > 3125){ 
    obstacles[37].square(425);
  }
  if(timer > 3130){ 
    obstacles[50].spike(550);
  }
  if(timer > 3138){ 
    obstacles[51].spike(550);
  }
  if(timer > 3146){ 
    obstacles[52].spike(550);
  }
  if(timer > 3154){ 
    obstacles[53].spike(550);
  }
  if(timer > 3160){ 
    obstacles[38].square(375);
  }
  if(timer > 3210){ 
    obstacles[54].spike(550);
  }
  if(timer > 3250){ 
    obstacles[55].spike(550);
  }
  if(timer > 3258){ 
    obstacles[56].spike(550);
  }
  if(timer > 3274){ 
    obstacles[39].square(525);
  }
  if(timer > 3282){ 
    obstacles[57].spike(550);
  }
  if(timer > 3290){ 
    obstacles[58].spike(550);
  }
  if(timer > 3350){ 
    obstacles[59].spike(550);
  }
  if(timer > 3358){ 
    obstacles[60].spike(550);
  }
  if(timer > 3374){ 
    obstacles[40].square(525);
  }
  if(timer > 3382){ 
    obstacles[61].spike(550);
  }
  if(timer > 3390){ 
    obstacles[62].spike(550);
  }
  if(timer > 3450){ 
    obstacles[63].spike(550);
  }
  if(timer > 3458){ 
    obstacles[64].spike(550);
  }
  if(timer > 3474){ 
    obstacles[41].square(525);
  }
  if(timer > 3482){ 
    obstacles[65].spike(550);
  }
  if(timer > 3490){ 
    obstacles[66].spike(550);
  }
  if(timer > 3540){ 
    obstacles[67].spike(550);
  }
  if(timer > 3548){ 
    obstacles[68].spike(550);
  }
  if(timer > 3564){ 
    obstacles[42].square(525);
  }
  if(timer > 3572){ 
    obstacles[69].spike(550);
  }
  if(timer > 3580){ 
    obstacles[70].spike(550);
  }
  //===============(3600 = 60s)===============
  if(timer > 3650){ 
    obstacles[43].square(525);
  }
  if(timer > 3690){ 
    obstacles[44].square(475);
  }
  if(timer > 3725){ 
    obstacles[45].square(425);
  }
  if(timer > 3760){ 
    obstacles[46].square(375);
  }
  if(timer > 3795){ 
    obstacles[47].square(325);
  }  
  if(timer > 3830){ 
    obstacles[48].square(275);
  }
  if(timer > 3838){ 
    obstacles[71].spike(550);
  }
  if(timer > 3846){ 
    obstacles[72].spike(550);
  }
  if(timer > 3854){ 
    obstacles[73].spike(550);
  }
  if(timer > 3862){ 
    obstacles[74].spike(550);
  }
  if(timer > 4000){ 
    obstacles[49].square(525);
  }
  if(timer > 4040){ 
    obstacles[50].square(475);
  }
  if(timer > 4075){ 
    obstacles[51].square(425);
  }
  if(timer > 4110){ 
    obstacles[52].square(375);
  }
  if(timer > 4145){ 
    obstacles[53].square(325);
  }  
  if(timer > 4180){ 
    obstacles[54].square(275);
  }
  if(timer > 4188){ 
    obstacles[75].spike(550);
  }
  if(timer > 4196){ 
    obstacles[76].spike(550);
  }
  //===============(4200 = 70s)===============
  if(timer > 4204){ 
    obstacles[77].spike(550);
  }
  if(timer > 4212){ 
    obstacles[78].spike(550);
  }
  if(timer > 4300){ 
    obstacles[55].square(525);
  }
  if(timer > 4340){ 
    obstacles[56].square(475);
  }
  if(timer > 4375){ 
    obstacles[57].square(425);
  }
  if(timer > 4410){ 
    obstacles[58].square(375);
  }
  if(timer > 4445){ 
    obstacles[59].square(325);
  }  
  if(timer > 4480){ 
    obstacles[60].square(275);
  }
  if(timer > 4488){ 
    obstacles[79].spike(550);
  }
  if(timer > 4496){ 
    obstacles[80].spike(550);
  }
  if(timer > 4504){ 
    obstacles[81].spike(550);
  }
  if(timer > 4512){ 
    obstacles[82].spike(550);
  }
  if(timer > 4600){ 
    obstacles[83].spike(550);
  }
  if(timer > 4650){ 
    obstacles[84].spike(500);
  }
  if(timer > 4700){ 
    obstacles[85].spike(550);
  }
  if(timer > 4750){ 
    obstacles[86].spike(515);
    obstacles[87].spike(550);
  }
  if(timer > 4800){ 
    obstacles[88].spike(550);
  }
  //===============(4800 = 80s)===============
  if(timer > 4850){ 
    obstacles[89].spike(500);
  }
  if(timer > 4900){ 
    obstacles[90].spike(550);
  }
  if(timer > 4950){ 
    obstacles[91].spike(515);
    obstacles[92].spike(550);
  }
  if(timer > 5000){ 
    obstacles[93].spike(550);
  }
  if(timer > 5008){ 
    obstacles[94].spike(550);
  }
  if(timer > 5046){ 
    obstacles[95].spike(550);
  }
  if(timer > 5100){ 
    obstacles[96].spike(515);
    obstacles[97].spike(550);
  }
  if(timer > 5170){ 
    obstacles[98].spike(515);
    obstacles[99].spike(550);
  }
  if(timer > 5230){ 
    obstacles[100].spike(515);
    obstacles[101].spike(550);
  }
  if(timer > 5280){ 
    obstacles[102].spike(515);
    obstacles[103].spike(550);
  }
  if(timer > 5330){ 
    obstacles[104].spike(515);
    obstacles[105].spike(550);
  }
  if(timer > 5380){ 
    obstacles[106].spike(515);
    obstacles[107].spike(550);
  }
  //===============(5400 = 90s)===============
  if(timer > 5500){
    obstacles[61].square(525);
  }
  if(timer > 5540){
    obstacles[62].square(475);
  }
  if(timer > 5575){
    obstacles[63].square(425);
  }
  if(timer > 5605){
    obstacles[64].square(375);
  }
  if(timer > 5625){
    obstacles[65].square(425);
  }
  if(timer > 5640){ 
    obstacles[108].spike(550);
  }
  if(timer > 5648){ 
    obstacles[109].spike(400);
    obstacles[110].spike(550);
  }
  if(timer > 5656){ 
    obstacles[111].spike(400);
    obstacles[112].spike(550);
  }
  if(timer > 5750){
    obstacles[66].square(525);
  }
  if(timer > 5790){
    obstacles[67].square(475);
  }
  if(timer > 5825){
    obstacles[68].square(425);
  }
  if(timer > 5860){
    obstacles[69].square(375);
  }
  if(timer > 5860){ 
    obstacles[113].spike(515);
    obstacles[114].spike(550);
  }
  if(timer > 5876){ 
    obstacles[115].spike(515);
    obstacles[116].spike(550);
  }
  if(timer > 5950){
    obstacles[70].square(525);
  }
  if(timer > 5990){
    obstacles[71].square(475);
  }
  //===============(6000 = 100s)===============
 
  //===============(END)===============
  if(timer > 6000){ //completed the game
    gameComplete();
  }
    //===============(6000 = 100s)===============
}

void obstacleSpawnMedium(){ //spawns the obstacles based on the timer (this part of the code is incredibly long)
/*
Notes to self: 
- floor is 525 (square) and 550 (spike)
- good timer distance for linked objects 12 (square) and 8 (spike)
- nearly 1200 lines of code for this part D:
*/
  if(timer > 150){
    obstacles[1].spike(550);
  }
  if(timer > 250){
    obstacles[2].spike(550);
  }
  if(timer > 350){
    obstacles[3].spike(550);
  }
  if(timer > 450){
    obstacles[4].spike(550);
  }
  if(timer > 525){
    obstacles[5].spike(550);
  }
  if(timer > 600){
    obstacles[6].spike(550);
  }
  //===============(600 = 10s)===============
  if(timer > 675){
    obstacles[7].spike(550);
  }
  if(timer > 682){
    obstacles[8].spike(550);
  }
  if(timer > 750){
    obstacles[1].square(525);
  }
  if(timer > 780){
    obstacles[2].square(475);
  }
  if(timer > 810){
    obstacles[3].square(425);
  }
  if(timer > 845){
    obstacles[4].square(375);
  }
  if(timer > 850){
    obstacles[9].spike(550);
  }
  if(timer > 858){
    obstacles[10].spike(550);
  }
  if(timer > 866){
    obstacles[11].spike(550);
  }
  if(timer > 874){
    obstacles[12].spike(550);
  }
  if(timer > 880){
    obstacles[5].square(375);
  }
  if(timer > 882){
    obstacles[13].spike(550);
  }
  if(timer > 930){ 
    obstacles[6].square(375);
  }
  if(timer > 965){
    obstacles[14].spike(550);
  }
  if(timer > 1005){
    obstacles[15].spike(550);
  }
  if(timer > 1080){ 
    obstacles[7].square(525);
  }
  if(timer > 1120){ 
    obstacles[8].square(475);
  }
  if(timer > 1160){ 
    obstacles[9].square(525);
  }
  if(timer > 1200){ 
    obstacles[10].square(475);
  }
  //===============(1200 = 20s)===============
  if(timer > 1240){ 
    obstacles[11].square(525);
  }
  if(timer > 1276){ 
    obstacles[16].spike(450);
  }
  if(timer > 1280){ 
    obstacles[12].square(475);
  }
  if(timer > 1330){ 
    obstacles[13].square(525);
  }
  if(timer > 1338){
    obstacles[17].spike(550);
  }
  if(timer > 1346){
    obstacles[18].spike(550);
  }
  if(timer > 1354){
    obstacles[19].spike(550);
  }
  if(timer > 1362){
    obstacles[20].spike(550);
  }
  if(timer > 1450){ 
    obstacles[14].square(525);
  }
  if(timer > 1500){ 
    obstacles[15].square(475);
  }
  if(timer > 1524){ 
    obstacles[16].square(525);
  }
  if(timer > 1572){
    obstacles[21].spike(550);
  }
  if(timer > 1650){
    obstacles[22].spike(550);
  }
  if(timer > 1658){
    obstacles[23].spike(550);
  }
  if(timer > 1690){
    obstacles[24].spike(550);
  }
  if(timer > 1698){
    obstacles[25].spike(550);
  }
  if(timer > 1730){
    obstacles[26].spike(550);
  }
  if(timer > 1738){
    obstacles[27].spike(550);
  }
  if(timer > 1775){
    obstacles[28].spike(550);
  }
  //===============(1800 = 30s)===============
  if(timer > 1830){
    obstacles[29].spike(550);
  }
  if(timer > 1838){
    obstacles[30].spike(550);
  }
  if(timer > 1870){
    obstacles[31].spike(550);
  }
  if(timer > 1878){
    obstacles[32].spike(550);
  }
  if(timer > 1940){
    obstacles[33].spike(550);
  }
  if(timer > 2000){
    obstacles[34].spike(550);
  }
  if(timer > 2008){
    obstacles[35].spike(550);
  }
  if(timer > 2040){
    obstacles[36].spike(550);
  }
  if(timer > 2048){
    obstacles[37].spike(550);
  }
  if(timer > 2080){
    obstacles[38].spike(550);
  }
  if(timer > 2088){
    obstacles[39].spike(550);
  }
  if(timer > 2160){ 
    obstacles[17].square(525);
  }
  if(timer > 2200){ 
    obstacles[18].square(475);
  }
  if(timer > 2220){
    obstacles[40].spike(500);
    obstacles[41].spike(550);
  }
  if(timer > 2240){ 
    obstacles[19].square(475);
  }
  if(timer > 2275){ 
    obstacles[20].square(425);
  }
  if(timer > 2310){ 
    obstacles[21].square(375);
  }
  if(timer > 2345){ 
    obstacles[22].square(325);
  }
  if(timer > 2365){ 
    obstacles[23].square(375);
  }
  if(timer > 2400){ 
    obstacles[24].square(325);
  }
  //===============(2400 = 40s)===============
  if(timer > 2414){ 
    obstacles[42].spike(550);
  }
  if(timer > 2422){ 
    obstacles[43].spike(550);
  }
  if(timer > 2430){ 
    obstacles[44].spike(550);
  }
  if(timer > 2438){ 
    obstacles[45].spike(550);
  }
  if(timer > 2550){ 
    obstacles[25].square(525);
  }
  if(timer > 2590){ 
    obstacles[26].square(475);
  }
  if(timer > 2630){ 
    obstacles[27].square(525);
  }
  if(timer > 2670){ 
    obstacles[28].square(475);
  }
  if(timer > 2706){ 
    obstacles[46].spike(550);
  }
  if(timer > 2714){ 
    obstacles[47].spike(550);
  }
  if(timer > 2760){ 
    obstacles[29].square(525);
  }
  if(timer > 2800){ 
    obstacles[30].square(475);
  }
  if(timer > 2840){ 
    obstacles[31].square(525);
  }
  if(timer > 2880){ 
    obstacles[32].square(475);
  }
  if(timer > 2916){ 
    obstacles[48].spike(550);
  }
  if(timer > 2924){ 
    obstacles[49].spike(550);
  }
  if(timer > 2970){ 
    obstacles[33].square(525);
  }
  //===============(3000 = 50s)===============
  if(timer > 3010){ 
    obstacles[34].square(475);
  }
  if(timer > 3050){ 
    obstacles[35].square(525);
  }
  if(timer > 3090){ 
    obstacles[36].square(475);
  }
  if(timer > 3125){ 
    obstacles[37].square(425);
  }
  if(timer > 3130){ 
    obstacles[50].spike(550);
  }
  if(timer > 3138){ 
    obstacles[51].spike(550);
  }
  if(timer > 3146){ 
    obstacles[52].spike(550);
  }
  if(timer > 3154){ 
    obstacles[53].spike(550);
  }
  if(timer > 3160){ 
    obstacles[38].square(375);
  }
  if(timer > 3210){ 
    obstacles[54].spike(550);
  }
  if(timer > 3250){ 
    obstacles[55].spike(550);
  }
  if(timer > 3258){ 
    obstacles[56].spike(550);
  }
  if(timer > 3274){ 
    obstacles[39].square(525);
  }
  if(timer > 3282){ 
    obstacles[57].spike(550);
  }
  if(timer > 3290){ 
    obstacles[58].spike(550);
  }
  if(timer > 3350){ 
    obstacles[59].spike(550);
  }
  if(timer > 3358){ 
    obstacles[60].spike(550);
  }
  if(timer > 3374){ 
    obstacles[40].square(525);
  }
  if(timer > 3382){ 
    obstacles[61].spike(550);
  }
  if(timer > 3390){ 
    obstacles[62].spike(550);
  }
  if(timer > 3450){ 
    obstacles[63].spike(550);
  }
  if(timer > 3458){ 
    obstacles[64].spike(550);
  }
  if(timer > 3474){ 
    obstacles[41].square(525);
  }
  if(timer > 3482){ 
    obstacles[65].spike(550);
  }
  if(timer > 3490){ 
    obstacles[66].spike(550);
  }
  if(timer > 3540){ 
    obstacles[67].spike(550);
  }
  if(timer > 3548){ 
    obstacles[68].spike(550);
  }
  if(timer > 3564){ 
    obstacles[42].square(525);
  }
  if(timer > 3572){ 
    obstacles[69].spike(550);
  }
  if(timer > 3580){ 
    obstacles[70].spike(550);
  }
  //===============(3600 = 60s)===============
  if(timer > 3650){ 
    obstacles[43].square(525);
  }
  if(timer > 3690){ 
    obstacles[44].square(475);
  }
  if(timer > 3725){ 
    obstacles[45].square(425);
  }
  if(timer > 3760){ 
    obstacles[46].square(375);
  }
  if(timer > 3795){ 
    obstacles[47].square(325);
  }  
  if(timer > 3830){ 
    obstacles[48].square(275);
  }
  if(timer > 3838){ 
    obstacles[71].spike(550);
  }
  if(timer > 3846){ 
    obstacles[72].spike(550);
  }
  if(timer > 3854){ 
    obstacles[73].spike(550);
  }
  if(timer > 3862){ 
    obstacles[74].spike(550);
  }
  if(timer > 4000){ 
    obstacles[49].square(525);
  }
  if(timer > 4040){ 
    obstacles[50].square(475);
  }
  if(timer > 4075){ 
    obstacles[51].square(425);
  }
  if(timer > 4110){ 
    obstacles[52].square(375);
  }
  if(timer > 4145){ 
    obstacles[53].square(325);
  }  
  if(timer > 4180){ 
    obstacles[54].square(275);
  }
  if(timer > 4188){ 
    obstacles[75].spike(550);
  }
  if(timer > 4196){ 
    obstacles[76].spike(550);
  }
  //===============(4200 = 70s)===============
  if(timer > 4204){ 
    obstacles[77].spike(550);
  }
  if(timer > 4212){ 
    obstacles[78].spike(550);
  }
  if(timer > 4300){ 
    obstacles[55].square(525);
  }
  if(timer > 4340){ 
    obstacles[56].square(475);
  }
  if(timer > 4375){ 
    obstacles[57].square(425);
  }
  if(timer > 4410){ 
    obstacles[58].square(375);
  }
  if(timer > 4445){ 
    obstacles[59].square(325);
  }  
  if(timer > 4480){ 
    obstacles[60].square(275);
  }
  if(timer > 4488){ 
    obstacles[79].spike(550);
  }
  if(timer > 4496){ 
    obstacles[80].spike(550);
  }
  if(timer > 4504){ 
    obstacles[81].spike(550);
  }
  if(timer > 4512){ 
    obstacles[82].spike(550);
  }
  if(timer > 4600){ 
    obstacles[83].spike(550);
  }
  if(timer > 4650){ 
    obstacles[84].spike(500);
  }
  if(timer > 4700){ 
    obstacles[85].spike(550);
  }
  if(timer > 4750){ 
    obstacles[86].spike(515);
    obstacles[87].spike(550);
  }
  if(timer > 4800){ 
    obstacles[88].spike(550);
  }
  //===============(4800 = 80s)===============
  if(timer > 4850){ 
    obstacles[89].spike(500);
  }
  if(timer > 4900){ 
    obstacles[90].spike(550);
  }
  if(timer > 4950){ 
    obstacles[91].spike(515);
    obstacles[92].spike(550);
  }
  if(timer > 5000){ 
    obstacles[93].spike(550);
  }
  if(timer > 5008){ 
    obstacles[94].spike(550);
  }
  if(timer > 5046){ 
    obstacles[95].spike(550);
  }
  if(timer > 5100){ 
    obstacles[96].spike(515);
    obstacles[97].spike(550);
  }
  if(timer > 5170){ 
    obstacles[98].spike(515);
    obstacles[99].spike(550);
  }
  if(timer > 5230){ 
    obstacles[100].spike(515);
    obstacles[101].spike(550);
  }
  if(timer > 5280){ 
    obstacles[102].spike(515);
    obstacles[103].spike(550);
  }
  if(timer > 5330){ 
    obstacles[104].spike(515);
    obstacles[105].spike(550);
  }
  if(timer > 5380){ 
    obstacles[106].spike(515);
    obstacles[107].spike(550);
  }
  //===============(5400 = 90s)===============
  if(timer > 5500){
    obstacles[61].square(525);
  }
  if(timer > 5540){
    obstacles[62].square(475);
  }
  if(timer > 5575){
    obstacles[63].square(425);
  }
  if(timer > 5605){
    obstacles[64].square(375);
  }
  if(timer > 5625){
    obstacles[65].square(425);
  }
  if(timer > 5640){ 
    obstacles[108].spike(550);
  }
  if(timer > 5648){ 
    obstacles[109].spike(400);
    obstacles[110].spike(550);
  }
  if(timer > 5656){ 
    obstacles[111].spike(400);
    obstacles[112].spike(550);
  }
  if(timer > 5750){
    obstacles[66].square(525);
  }
  if(timer > 5790){
    obstacles[67].square(475);
  }
  if(timer > 5825){
    obstacles[68].square(425);
  }
  if(timer > 5860){
    obstacles[69].square(375);
  }
  if(timer > 5860){ 
    obstacles[113].spike(515);
    obstacles[114].spike(550);
  }
  if(timer > 5876){ 
    obstacles[115].spike(515);
    obstacles[116].spike(550);
  }
  if(timer > 5950){
    obstacles[70].square(525);
  }
  if(timer > 5990){
    obstacles[71].square(475);
  }
  //===============(6000 = 100s)===============
  if(timer > 6025){
    obstacles[72].square(425);
    obstacles[117].spike(550);
  }
  if(timer > 6060){
    obstacles[73].square(375);
  }
  if(timer > 6068){ 
    obstacles[118].spike(350);
  }
  if(timer > 6076){ 
    obstacles[119].spike(350);
  }
  if(timer > 6084){ 
    obstacles[120].spike(350);
  }
  if(timer > 6092){ 
    obstacles[121].spike(350);
  }
  if(timer > 6200){
    obstacles[74].square(525);
  }
  if(timer > 6240){
    obstacles[75].square(475);
  }
  if(timer > 6275){
    obstacles[76].square(425);
  }
  if(timer > 6310){
    obstacles[77].square(375);
  }
  if(timer > 6318){ 
    obstacles[122].spike(350);
  }
  if(timer > 6326){ 
    obstacles[123].spike(350);
  }
  if(timer > 6334){ 
    obstacles[124].spike(350);
  }
  if(timer > 6342){ 
    obstacles[125].spike(350);
  }
  if(timer > 6450){
    obstacles[78].square(525);
  }
  if(timer > 6490){
    obstacles[79].square(475);
  }
  if(timer > 6525){
    obstacles[80].square(425);
  }
  if(timer > 6560){
    obstacles[81].square(375);
  }
  if(timer > 6560){ 
    obstacles[126].spike(515);
    obstacles[127].spike(550);
  }
  if(timer > 6576){ 
    obstacles[128].spike(515);
    obstacles[129].spike(550);
  }
  //===============(6600 = 110s)===============
  if(timer > 6700){ 
    obstacles[82].square(525);
  }
  if(timer > 6740){ 
    obstacles[83].square(475);
  }
  if(timer > 6775){ 
    obstacles[84].square(425);
  }
  if(timer > 6791){ 
    obstacles[130].spike(400);
  }
  if(timer > 6799){ 
    obstacles[131].spike(400);
  }
  if(timer > 6820){ 
    obstacles[85].square(425);
  }
  if(timer > 6836){ 
    obstacles[132].spike(400);
  }
  if(timer > 6844){ 
    obstacles[133].spike(400);
  }
  if(timer > 6865){ 
    obstacles[86].square(425);
  }
  if(timer > 6881){ 
    obstacles[134].spike(400);
  }
  if(timer > 6889){ 
    obstacles[135].spike(400);
  }
  if(timer > 6910){ 
    obstacles[87].square(425);
  }
  if(timer > 6945){ 
    obstacles[88].square(375);
  }
  if(timer > 6980){ 
    obstacles[89].square(325);
  }
  if(timer > 6996){ 
    obstacles[136].spike(300);
  }
  if(timer > 7004){ 
    obstacles[137].spike(300);
  }
  if(timer > 7025){ 
    obstacles[90].square(325);
  }
  if(timer > 7041){ 
    obstacles[138].spike(300);
  }
  if(timer > 7049){ 
    obstacles[139].spike(300);
  }
  if(timer > 7070){ 
    obstacles[91].square(325);
  }
  if(timer > 7086){ 
    obstacles[140].spike(300);
  }
  if(timer > 7094){ 
    obstacles[141].spike(300);
  }
  if(timer > 7115){ 
    obstacles[92].square(325);
  }
  if(timer > 7135){ 
    obstacles[93].square(375);
  }
  if(timer > 7155){ 
    obstacles[94].square(425);
  }
  if(timer > 7175){ 
    obstacles[95].square(475);
  }
  if(timer > 7191){ 
    obstacles[142].spike(450);
  }
  if(timer > 7199){ 
    obstacles[143].spike(450);
  }
  //===============(7200 = 120s)===============
  if(timer > 7220){ 
    obstacles[96].square(475);
  }
  if(timer > 7236){ 
    obstacles[144].spike(450);
  }
  if(timer > 7244){ 
    obstacles[145].spike(450);
  }
  if(timer > 7265){ 
    obstacles[97].square(475);
  }
  if(timer > 7281){ 
    obstacles[146].spike(450);
    obstacles[147].spike(550);
  }
  if(timer > 7289){ 
    obstacles[148].spike(450);
    obstacles[149].spike(550);
  }
  if(timer > 7310){ 
    obstacles[98].square(475);
  }
  if(timer > 7335){ 
    obstacles[99].square(525);
  }
  if(timer > 7380){ 
    obstacles[150].spike(550);
  }
  if(timer > 7388){ 
    obstacles[151].spike(550);
  }
  if(timer > 7433){ 
    obstacles[152].spike(550);
  }
  if(timer > 7441){ 
    obstacles[153].spike(550);
  }
  if(timer > 7536){ 
    obstacles[154].spike(550);
  }
  if(timer > 7550){ 
    obstacles[100].square(525);
  }
  if(timer > 7571){ 
    obstacles[155].spike(500);
  }
  if(timer > 7585){ 
    obstacles[101].square(475);
  }
  if(timer > 7606){ 
    obstacles[156].spike(450);
  }
  if(timer > 7620){ 
    obstacles[102].square(425);
  }
  if(timer > 7641){ 
    obstacles[157].spike(400);
  }
  if(timer > 7655){ 
    obstacles[103].square(375);
  }
  if(timer > 7680){ 
    obstacles[104].square(425);
  }
  if(timer > 7715){ 
    obstacles[105].square(375);
  }
  if(timer > 7750){ 
    obstacles[106].square(325);
  }
  if(timer > 7775){ 
    obstacles[107].square(375);
  }
  //===============(7800 = 130s)===============
  if(timer > 7810){ 
    obstacles[108].square(325);
  }
  if(timer > 7835){ 
    obstacles[109].square(375);
  }
  if(timer > 7860){ 
    obstacles[110].square(425);
    obstacles[158].spike(550);
  }
  if(timer > 7868){ 
    obstacles[159].spike(550);
  }
  if(timer > 7885){ 
    obstacles[111].square(475);
  }
  if(timer > 7910){ 
    obstacles[112].square(525);
  }
  if(timer > 7945){ 
    obstacles[113].square(475);
  }
  if(timer > 7970){ 
    obstacles[114].square(525);
  }
  if(timer > 8005){ 
    obstacles[115].square(475);
  }
  if(timer > 8040){ 
    obstacles[116].square(425);
  }
  if(timer > 8065){ 
    obstacles[117].square(475);
  }
  if(timer > 8100){ 
    obstacles[118].square(425);
  }
  if(timer > 8135){ 
    obstacles[119].square(375);
  }
  if(timer > 8160){ 
    obstacles[120].square(425);
  }
  if(timer > 8195){ 
    obstacles[121].square(375);
  }
  if(timer > 8220){ 
    obstacles[122].square(425);
  }
  if(timer > 8255){ 
    obstacles[123].square(375);
  }
  if(timer > 8290){ 
    obstacles[124].square(325);
  }
  if(timer > 8315){ 
    obstacles[125].square(375);
  }
  if(timer > 8350){ 
    obstacles[126].square(325);
  }
  if(timer > 8375){ 
    obstacles[127].square(375);
  }
  if(timer > 8400){ 
    obstacles[128].square(425);
  }
  //===============(8400 = 140s)===============
  if(timer > 8408){ 
    obstacles[160].spike(550);
  }
  if(timer > 8416){ 
    obstacles[161].spike(550);
  }
  if(timer > 8424){ 
    obstacles[162].spike(550);
  }
  if(timer > 8432){ 
    obstacles[163].spike(550);
  }
  if(timer > 8445){ 
    obstacles[129].square(425);
  }
  if(timer > 8470){ 
    obstacles[130].square(475);
  }
  if(timer > 8495){ 
    obstacles[131].square(525);
  }
  if(timer > 8600){ 
    obstacles[132].square(525);
  }
  if(timer > 8640){ 
    obstacles[133].square(475);
  }
  if(timer > 8648){ 
    obstacles[164].spike(450);
  }
  if(timer > 8656){ 
    obstacles[165].spike(450);
  }
  if(timer > 8664){ 
    obstacles[166].spike(450);
  }
  if(timer > 8750){ 
    obstacles[134].square(525);
  }
  if(timer > 8790){ 
    obstacles[135].square(475);
  }
  if(timer > 8798){ 
    obstacles[167].spike(550);
  }
  if(timer > 8806){ 
    obstacles[168].spike(550);
  }
  if(timer > 8814){ 
    obstacles[169].spike(550);
  }
  if(timer > 8900){ 
    obstacles[136].square(525);
  }
  if(timer > 8940){ 
    obstacles[137].square(475);
  }
  if(timer > 8948){ 
    obstacles[170].spike(550);
  }
  if(timer > 8956){ 
    obstacles[171].spike(550);
  }
  if(timer > 8964){ 
    obstacles[172].spike(550);
  }
  //===============(9000 = 150s)===============
  
  //===============(END)===============
  if(timer > 9000){ //completed the game
    gameComplete();
  }
  //===============(12000 = 200s)===============
}

void obstacleSpawnHard(){ //spawns the obstacles based on the timer (this part of the code is incredibly long)
/*
Notes to self: 
- floor is 525 (square) and 550 (spike)
- good timer distance for linked objects 12 (square) and 8 (spike)
- nearly 1200 lines of code for this part D:
*/
  if(timer > 150){
    obstacles[1].spike(550);
  }
  if(timer > 250){
    obstacles[2].spike(550);
  }
  if(timer > 350){
    obstacles[3].spike(550);
  }
  if(timer > 450){
    obstacles[4].spike(550);
  }
  if(timer > 525){
    obstacles[5].spike(550);
  }
  if(timer > 600){
    obstacles[6].spike(550);
  }
  //===============(600 = 10s)===============
  if(timer > 675){
    obstacles[7].spike(550);
  }
  if(timer > 682){
    obstacles[8].spike(550);
  }
  if(timer > 750){
    obstacles[1].square(525);
  }
  if(timer > 780){
    obstacles[2].square(475);
  }
  if(timer > 810){
    obstacles[3].square(425);
  }
  if(timer > 845){
    obstacles[4].square(375);
  }
  if(timer > 850){
    obstacles[9].spike(550);
  }
  if(timer > 858){
    obstacles[10].spike(550);
  }
  if(timer > 866){
    obstacles[11].spike(550);
  }
  if(timer > 874){
    obstacles[12].spike(550);
  }
  if(timer > 880){
    obstacles[5].square(375);
  }
  if(timer > 882){
    obstacles[13].spike(550);
  }
  if(timer > 930){ 
    obstacles[6].square(375);
  }
  if(timer > 965){
    obstacles[14].spike(550);
  }
  if(timer > 1005){
    obstacles[15].spike(550);
  }
  if(timer > 1080){ 
    obstacles[7].square(525);
  }
  if(timer > 1120){ 
    obstacles[8].square(475);
  }
  if(timer > 1160){ 
    obstacles[9].square(525);
  }
  if(timer > 1200){ 
    obstacles[10].square(475);
  }
  //===============(1200 = 20s)===============
  if(timer > 1240){ 
    obstacles[11].square(525);
  }
  if(timer > 1276){ 
    obstacles[16].spike(450);
  }
  if(timer > 1280){ 
    obstacles[12].square(475);
  }
  if(timer > 1330){ 
    obstacles[13].square(525);
  }
  if(timer > 1338){
    obstacles[17].spike(550);
  }
  if(timer > 1346){
    obstacles[18].spike(550);
  }
  if(timer > 1354){
    obstacles[19].spike(550);
  }
  if(timer > 1362){
    obstacles[20].spike(550);
  }
  if(timer > 1450){ 
    obstacles[14].square(525);
  }
  if(timer > 1500){ 
    obstacles[15].square(475);
  }
  if(timer > 1524){ 
    obstacles[16].square(525);
  }
  if(timer > 1572){
    obstacles[21].spike(550);
  }
  if(timer > 1650){
    obstacles[22].spike(550);
  }
  if(timer > 1658){
    obstacles[23].spike(550);
  }
  if(timer > 1690){
    obstacles[24].spike(550);
  }
  if(timer > 1698){
    obstacles[25].spike(550);
  }
  if(timer > 1730){
    obstacles[26].spike(550);
  }
  if(timer > 1738){
    obstacles[27].spike(550);
  }
  if(timer > 1775){
    obstacles[28].spike(550);
  }
  //===============(1800 = 30s)===============
  if(timer > 1830){
    obstacles[29].spike(550);
  }
  if(timer > 1838){
    obstacles[30].spike(550);
  }
  if(timer > 1870){
    obstacles[31].spike(550);
  }
  if(timer > 1878){
    obstacles[32].spike(550);
  }
  if(timer > 1940){
    obstacles[33].spike(550);
  }
  if(timer > 2000){
    obstacles[34].spike(550);
  }
  if(timer > 2008){
    obstacles[35].spike(550);
  }
  if(timer > 2040){
    obstacles[36].spike(550);
  }
  if(timer > 2048){
    obstacles[37].spike(550);
  }
  if(timer > 2080){
    obstacles[38].spike(550);
  }
  if(timer > 2088){
    obstacles[39].spike(550);
  }
  if(timer > 2160){ 
    obstacles[17].square(525);
  }
  if(timer > 2200){ 
    obstacles[18].square(475);
  }
  if(timer > 2220){
    obstacles[40].spike(500);
    obstacles[41].spike(550);
  }
  if(timer > 2240){ 
    obstacles[19].square(475);
  }
  if(timer > 2275){ 
    obstacles[20].square(425);
  }
  if(timer > 2310){ 
    obstacles[21].square(375);
  }
  if(timer > 2345){ 
    obstacles[22].square(325);
  }
  if(timer > 2365){ 
    obstacles[23].square(375);
  }
  if(timer > 2400){ 
    obstacles[24].square(325);
  }
  //===============(2400 = 40s)===============
  if(timer > 2414){ 
    obstacles[42].spike(550);
  }
  if(timer > 2422){ 
    obstacles[43].spike(550);
  }
  if(timer > 2430){ 
    obstacles[44].spike(550);
  }
  if(timer > 2438){ 
    obstacles[45].spike(550);
  }
  if(timer > 2550){ 
    obstacles[25].square(525);
  }
  if(timer > 2590){ 
    obstacles[26].square(475);
  }
  if(timer > 2630){ 
    obstacles[27].square(525);
  }
  if(timer > 2670){ 
    obstacles[28].square(475);
  }
  if(timer > 2706){ 
    obstacles[46].spike(550);
  }
  if(timer > 2714){ 
    obstacles[47].spike(550);
  }
  if(timer > 2760){ 
    obstacles[29].square(525);
  }
  if(timer > 2800){ 
    obstacles[30].square(475);
  }
  if(timer > 2840){ 
    obstacles[31].square(525);
  }
  if(timer > 2880){ 
    obstacles[32].square(475);
  }
  if(timer > 2916){ 
    obstacles[48].spike(550);
  }
  if(timer > 2924){ 
    obstacles[49].spike(550);
  }
  if(timer > 2970){ 
    obstacles[33].square(525);
  }
  //===============(3000 = 50s)===============
  if(timer > 3010){ 
    obstacles[34].square(475);
  }
  if(timer > 3050){ 
    obstacles[35].square(525);
  }
  if(timer > 3090){ 
    obstacles[36].square(475);
  }
  if(timer > 3125){ 
    obstacles[37].square(425);
  }
  if(timer > 3130){ 
    obstacles[50].spike(550);
  }
  if(timer > 3138){ 
    obstacles[51].spike(550);
  }
  if(timer > 3146){ 
    obstacles[52].spike(550);
  }
  if(timer > 3154){ 
    obstacles[53].spike(550);
  }
  if(timer > 3160){ 
    obstacles[38].square(375);
  }
  if(timer > 3210){ 
    obstacles[54].spike(550);
  }
  if(timer > 3250){ 
    obstacles[55].spike(550);
  }
  if(timer > 3258){ 
    obstacles[56].spike(550);
  }
  if(timer > 3274){ 
    obstacles[39].square(525);
  }
  if(timer > 3282){ 
    obstacles[57].spike(550);
  }
  if(timer > 3290){ 
    obstacles[58].spike(550);
  }
  if(timer > 3350){ 
    obstacles[59].spike(550);
  }
  if(timer > 3358){ 
    obstacles[60].spike(550);
  }
  if(timer > 3374){ 
    obstacles[40].square(525);
  }
  if(timer > 3382){ 
    obstacles[61].spike(550);
  }
  if(timer > 3390){ 
    obstacles[62].spike(550);
  }
  if(timer > 3450){ 
    obstacles[63].spike(550);
  }
  if(timer > 3458){ 
    obstacles[64].spike(550);
  }
  if(timer > 3474){ 
    obstacles[41].square(525);
  }
  if(timer > 3482){ 
    obstacles[65].spike(550);
  }
  if(timer > 3490){ 
    obstacles[66].spike(550);
  }
  if(timer > 3540){ 
    obstacles[67].spike(550);
  }
  if(timer > 3548){ 
    obstacles[68].spike(550);
  }
  if(timer > 3564){ 
    obstacles[42].square(525);
  }
  if(timer > 3572){ 
    obstacles[69].spike(550);
  }
  if(timer > 3580){ 
    obstacles[70].spike(550);
  }
  //===============(3600 = 60s)===============
  if(timer > 3650){ 
    obstacles[43].square(525);
  }
  if(timer > 3690){ 
    obstacles[44].square(475);
  }
  if(timer > 3725){ 
    obstacles[45].square(425);
  }
  if(timer > 3760){ 
    obstacles[46].square(375);
  }
  if(timer > 3795){ 
    obstacles[47].square(325);
  }  
  if(timer > 3830){ 
    obstacles[48].square(275);
  }
  if(timer > 3838){ 
    obstacles[71].spike(550);
  }
  if(timer > 3846){ 
    obstacles[72].spike(550);
  }
  if(timer > 3854){ 
    obstacles[73].spike(550);
  }
  if(timer > 3862){ 
    obstacles[74].spike(550);
  }
  if(timer > 4000){ 
    obstacles[49].square(525);
  }
  if(timer > 4040){ 
    obstacles[50].square(475);
  }
  if(timer > 4075){ 
    obstacles[51].square(425);
  }
  if(timer > 4110){ 
    obstacles[52].square(375);
  }
  if(timer > 4145){ 
    obstacles[53].square(325);
  }  
  if(timer > 4180){ 
    obstacles[54].square(275);
  }
  if(timer > 4188){ 
    obstacles[75].spike(550);
  }
  if(timer > 4196){ 
    obstacles[76].spike(550);
  }
  //===============(4200 = 70s)===============
  if(timer > 4204){ 
    obstacles[77].spike(550);
  }
  if(timer > 4212){ 
    obstacles[78].spike(550);
  }
  if(timer > 4300){ 
    obstacles[55].square(525);
  }
  if(timer > 4340){ 
    obstacles[56].square(475);
  }
  if(timer > 4375){ 
    obstacles[57].square(425);
  }
  if(timer > 4410){ 
    obstacles[58].square(375);
  }
  if(timer > 4445){ 
    obstacles[59].square(325);
  }  
  if(timer > 4480){ 
    obstacles[60].square(275);
  }
  if(timer > 4488){ 
    obstacles[79].spike(550);
  }
  if(timer > 4496){ 
    obstacles[80].spike(550);
  }
  if(timer > 4504){ 
    obstacles[81].spike(550);
  }
  if(timer > 4512){ 
    obstacles[82].spike(550);
  }
  if(timer > 4600){ 
    obstacles[83].spike(550);
  }
  if(timer > 4650){ 
    obstacles[84].spike(500);
  }
  if(timer > 4700){ 
    obstacles[85].spike(550);
  }
  if(timer > 4750){ 
    obstacles[86].spike(515);
    obstacles[87].spike(550);
  }
  if(timer > 4800){ 
    obstacles[88].spike(550);
  }
  //===============(4800 = 80s)===============
  if(timer > 4850){ 
    obstacles[89].spike(500);
  }
  if(timer > 4900){ 
    obstacles[90].spike(550);
  }
  if(timer > 4950){ 
    obstacles[91].spike(515);
    obstacles[92].spike(550);
  }
  if(timer > 5000){ 
    obstacles[93].spike(550);
  }
  if(timer > 5008){ 
    obstacles[94].spike(550);
  }
  if(timer > 5046){ 
    obstacles[95].spike(550);
  }
  if(timer > 5100){ 
    obstacles[96].spike(515);
    obstacles[97].spike(550);
  }
  if(timer > 5170){ 
    obstacles[98].spike(515);
    obstacles[99].spike(550);
  }
  if(timer > 5230){ 
    obstacles[100].spike(515);
    obstacles[101].spike(550);
  }
  if(timer > 5280){ 
    obstacles[102].spike(515);
    obstacles[103].spike(550);
  }
  if(timer > 5330){ 
    obstacles[104].spike(515);
    obstacles[105].spike(550);
  }
  if(timer > 5380){ 
    obstacles[106].spike(515);
    obstacles[107].spike(550);
  }
  //===============(5400 = 90s)===============
  if(timer > 5500){
    obstacles[61].square(525);
  }
  if(timer > 5540){
    obstacles[62].square(475);
  }
  if(timer > 5575){
    obstacles[63].square(425);
  }
  if(timer > 5605){
    obstacles[64].square(375);
  }
  if(timer > 5625){
    obstacles[65].square(425);
  }
  if(timer > 5640){ 
    obstacles[108].spike(550);
  }
  if(timer > 5648){ 
    obstacles[109].spike(400);
    obstacles[110].spike(550);
  }
  if(timer > 5656){ 
    obstacles[111].spike(400);
    obstacles[112].spike(550);
  }
  if(timer > 5750){
    obstacles[66].square(525);
  }
  if(timer > 5790){
    obstacles[67].square(475);
  }
  if(timer > 5825){
    obstacles[68].square(425);
  }
  if(timer > 5860){
    obstacles[69].square(375);
  }
  if(timer > 5860){ 
    obstacles[113].spike(515);
    obstacles[114].spike(550);
  }
  if(timer > 5876){ 
    obstacles[115].spike(515);
    obstacles[116].spike(550);
  }
  if(timer > 5950){
    obstacles[70].square(525);
  }
  if(timer > 5990){
    obstacles[71].square(475);
  }
  //===============(6000 = 100s)===============
  if(timer > 6025){
    obstacles[72].square(425);
    obstacles[117].spike(550);
  }
  if(timer > 6060){
    obstacles[73].square(375);
  }
  if(timer > 6068){ 
    obstacles[118].spike(350);
  }
  if(timer > 6076){ 
    obstacles[119].spike(350);
  }
  if(timer > 6084){ 
    obstacles[120].spike(350);
  }
  if(timer > 6092){ 
    obstacles[121].spike(350);
  }
  if(timer > 6200){
    obstacles[74].square(525);
  }
  if(timer > 6240){
    obstacles[75].square(475);
  }
  if(timer > 6275){
    obstacles[76].square(425);
  }
  if(timer > 6310){
    obstacles[77].square(375);
  }
  if(timer > 6318){ 
    obstacles[122].spike(350);
  }
  if(timer > 6326){ 
    obstacles[123].spike(350);
  }
  if(timer > 6334){ 
    obstacles[124].spike(350);
  }
  if(timer > 6342){ 
    obstacles[125].spike(350);
  }
  if(timer > 6450){
    obstacles[78].square(525);
  }
  if(timer > 6490){
    obstacles[79].square(475);
  }
  if(timer > 6525){
    obstacles[80].square(425);
  }
  if(timer > 6560){
    obstacles[81].square(375);
  }
  if(timer > 6560){ 
    obstacles[126].spike(515);
    obstacles[127].spike(550);
  }
  if(timer > 6576){ 
    obstacles[128].spike(515);
    obstacles[129].spike(550);
  }
  //===============(6600 = 110s)===============
  if(timer > 6700){ 
    obstacles[82].square(525);
  }
  if(timer > 6740){ 
    obstacles[83].square(475);
  }
  if(timer > 6775){ 
    obstacles[84].square(425);
  }
  if(timer > 6791){ 
    obstacles[130].spike(400);
  }
  if(timer > 6799){ 
    obstacles[131].spike(400);
  }
  if(timer > 6820){ 
    obstacles[85].square(425);
  }
  if(timer > 6836){ 
    obstacles[132].spike(400);
  }
  if(timer > 6844){ 
    obstacles[133].spike(400);
  }
  if(timer > 6865){ 
    obstacles[86].square(425);
  }
  if(timer > 6881){ 
    obstacles[134].spike(400);
  }
  if(timer > 6889){ 
    obstacles[135].spike(400);
  }
  if(timer > 6910){ 
    obstacles[87].square(425);
  }
  if(timer > 6945){ 
    obstacles[88].square(375);
  }
  if(timer > 6980){ 
    obstacles[89].square(325);
  }
  if(timer > 6996){ 
    obstacles[136].spike(300);
  }
  if(timer > 7004){ 
    obstacles[137].spike(300);
  }
  if(timer > 7025){ 
    obstacles[90].square(325);
  }
  if(timer > 7041){ 
    obstacles[138].spike(300);
  }
  if(timer > 7049){ 
    obstacles[139].spike(300);
  }
  if(timer > 7070){ 
    obstacles[91].square(325);
  }
  if(timer > 7086){ 
    obstacles[140].spike(300);
  }
  if(timer > 7094){ 
    obstacles[141].spike(300);
  }
  if(timer > 7115){ 
    obstacles[92].square(325);
  }
  if(timer > 7135){ 
    obstacles[93].square(375);
  }
  if(timer > 7155){ 
    obstacles[94].square(425);
  }
  if(timer > 7175){ 
    obstacles[95].square(475);
  }
  if(timer > 7191){ 
    obstacles[142].spike(450);
  }
  if(timer > 7199){ 
    obstacles[143].spike(450);
  }
  //===============(7200 = 120s)===============
  if(timer > 7220){ 
    obstacles[96].square(475);
  }
  if(timer > 7236){ 
    obstacles[144].spike(450);
  }
  if(timer > 7244){ 
    obstacles[145].spike(450);
  }
  if(timer > 7265){ 
    obstacles[97].square(475);
  }
  if(timer > 7281){ 
    obstacles[146].spike(450);
    obstacles[147].spike(550);
  }
  if(timer > 7289){ 
    obstacles[148].spike(450);
    obstacles[149].spike(550);
  }
  if(timer > 7310){ 
    obstacles[98].square(475);
  }
  if(timer > 7335){ 
    obstacles[99].square(525);
  }
  if(timer > 7380){ 
    obstacles[150].spike(550);
  }
  if(timer > 7388){ 
    obstacles[151].spike(550);
  }
  if(timer > 7433){ 
    obstacles[152].spike(550);
  }
  if(timer > 7441){ 
    obstacles[153].spike(550);
  }
  if(timer > 7536){ 
    obstacles[154].spike(550);
  }
  if(timer > 7550){ 
    obstacles[100].square(525);
  }
  if(timer > 7571){ 
    obstacles[155].spike(500);
  }
  if(timer > 7585){ 
    obstacles[101].square(475);
  }
  if(timer > 7606){ 
    obstacles[156].spike(450);
  }
  if(timer > 7620){ 
    obstacles[102].square(425);
  }
  if(timer > 7641){ 
    obstacles[157].spike(400);
  }
  if(timer > 7655){ 
    obstacles[103].square(375);
  }
  if(timer > 7680){ 
    obstacles[104].square(425);
  }
  if(timer > 7715){ 
    obstacles[105].square(375);
  }
  if(timer > 7750){ 
    obstacles[106].square(325);
  }
  if(timer > 7775){ 
    obstacles[107].square(375);
  }
  //===============(7800 = 130s)===============
  if(timer > 7810){ 
    obstacles[108].square(325);
  }
  if(timer > 7835){ 
    obstacles[109].square(375);
  }
  if(timer > 7860){ 
    obstacles[110].square(425);
    obstacles[158].spike(550);
  }
  if(timer > 7868){ 
    obstacles[159].spike(550);
  }
  if(timer > 7885){ 
    obstacles[111].square(475);
  }
  if(timer > 7910){ 
    obstacles[112].square(525);
  }
  if(timer > 7945){ 
    obstacles[113].square(475);
  }
  if(timer > 7970){ 
    obstacles[114].square(525);
  }
  if(timer > 8005){ 
    obstacles[115].square(475);
  }
  if(timer > 8040){ 
    obstacles[116].square(425);
  }
  if(timer > 8065){ 
    obstacles[117].square(475);
  }
  if(timer > 8100){ 
    obstacles[118].square(425);
  }
  if(timer > 8135){ 
    obstacles[119].square(375);
  }
  if(timer > 8160){ 
    obstacles[120].square(425);
  }
  if(timer > 8195){ 
    obstacles[121].square(375);
  }
  if(timer > 8220){ 
    obstacles[122].square(425);
  }
  if(timer > 8255){ 
    obstacles[123].square(375);
  }
  if(timer > 8290){ 
    obstacles[124].square(325);
  }
  if(timer > 8315){ 
    obstacles[125].square(375);
  }
  if(timer > 8350){ 
    obstacles[126].square(325);
  }
  if(timer > 8375){ 
    obstacles[127].square(375);
  }
  if(timer > 8400){ 
    obstacles[128].square(425);
  }
  //===============(8400 = 140s)===============
  if(timer > 8408){ 
    obstacles[160].spike(550);
  }
  if(timer > 8416){ 
    obstacles[161].spike(550);
  }
  if(timer > 8424){ 
    obstacles[162].spike(550);
  }
  if(timer > 8432){ 
    obstacles[163].spike(550);
  }
  if(timer > 8445){ 
    obstacles[129].square(425);
  }
  if(timer > 8470){ 
    obstacles[130].square(475);
  }
  if(timer > 8495){ 
    obstacles[131].square(525);
  }
  if(timer > 8600){ 
    obstacles[132].square(525);
  }
  if(timer > 8640){ 
    obstacles[133].square(475);
  }
  if(timer > 8648){ 
    obstacles[164].spike(450);
  }
  if(timer > 8656){ 
    obstacles[165].spike(450);
  }
  if(timer > 8664){ 
    obstacles[166].spike(450);
  }
  if(timer > 8750){ 
    obstacles[134].square(525);
  }
  if(timer > 8790){ 
    obstacles[135].square(475);
  }
  if(timer > 8798){ 
    obstacles[167].spike(550);
  }
  if(timer > 8806){ 
    obstacles[168].spike(550);
  }
  if(timer > 8814){ 
    obstacles[169].spike(550);
  }
  if(timer > 8900){ 
    obstacles[136].square(525);
  }
  if(timer > 8940){ 
    obstacles[137].square(475);
  }
  if(timer > 8948){ 
    obstacles[170].spike(550);
  }
  if(timer > 8956){ 
    obstacles[171].spike(550);
  }
  if(timer > 8964){ 
    obstacles[172].spike(550);
  }
  //===============(9000 = 150s)===============
  if(timer > 9050){ 
    obstacles[138].square(525);
  }
  if(timer > 9058){ 
    obstacles[173].spike(550);
  }
  if(timer > 9066){ 
    obstacles[174].spike(550);
  }
  if(timer > 9074){ 
    obstacles[175].spike(550);
  }
  if(timer > 9090){ 
    obstacles[139].square(525);
  }
  if(timer > 9130){ 
    obstacles[140].square(475);
  }
  if(timer > 9165){ 
    obstacles[141].square(425);
  }
  if(timer > 9205){ 
    obstacles[142].square(425);
  }
  if(timer > 9230){ 
    obstacles[143].square(475);
  }
  if(timer > 9275){ 
    obstacles[144].square(475);
  }
  if(timer > 9305){ 
    obstacles[145].square(425);
  }
  if(timer > 9340){ 
    obstacles[146].square(375);
  }
  if(timer > 9385){ 
    obstacles[147].square(375);
  }
  if(timer > 9410){ 
    obstacles[148].square(425);
  }
  if(timer > 9455){ 
    obstacles[149].square(425);
  }
  if(timer > 9490){ 
    obstacles[150].square(375);
  }
  if(timer > 9535){ 
    obstacles[151].square(375);
  }
  if(timer > 9560){ 
    obstacles[152].square(425);
  }
  if(timer > 9560){ 
    obstacles[176].spike(550);
  }
  if(timer > 9568){ 
    obstacles[177].spike(550);
  }
  if(timer > 9585){ 
    obstacles[153].square(475);
  }
  if(timer > 9610){ 
    obstacles[154].square(525);
  }
  //===============(9600 = 160s)===============
  if(timer > 9655){ 
    obstacles[155].square(525);
  }
  if(timer > 9690){ 
    obstacles[156].square(475);
  }
  if(timer > 9725){ 
    obstacles[157].square(425);
  }
  if(timer > 9760){ 
    obstacles[158].square(375);
  }
  if(timer > 9795){ 
    obstacles[159].square(325);
  }
  if(timer > 9830){ 
    obstacles[160].square(275);
  }
  if(timer > 9865){ 
    obstacles[161].square(225);
  }
  if(timer > 9900){ 
    obstacles[162].square(175);
  }
  if(timer > 9960){ 
    obstacles[163].square(475);
  }
  if(timer > 9985){ 
    obstacles[164].square(525);
  }
  if(timer > 9990){ 
    obstacles[165].square(425);
  }
  if(timer > 9993){ 
    obstacles[178].spike(550);
  }
  if(timer > 10001){ 
    obstacles[179].spike(550);
  }
  if(timer > 10035){ 
    obstacles[166].square(425);
  }
  if(timer > 10070){ 
    obstacles[167].square(375);
  }
  if(timer > 10105){ 
    obstacles[168].square(325);
  }
  if(timer > 10130){ 
    obstacles[169].square(375);
  }
  if(timer > 10165){ 
    obstacles[170].square(325);
  }
  if(timer > 10190){ 
    obstacles[171].square(375);
  }
  //===============(10200 = 170s)===============
  if(timer > 10235){ 
    obstacles[172].square(325);
  }
  if(timer > 10260){ 
    obstacles[173].square(375);
  }
  if(timer > 10305){ 
    obstacles[174].square(325);
  }
  if(timer > 10330){ 
    obstacles[175].square(375);
  }
  if(timer > 10355){ 
    obstacles[176].square(425);
  }
  if(timer > 10363){ 
    obstacles[180].spike(550);
  }
  if(timer > 10371){ 
    obstacles[181].spike(550);
  }
  if(timer > 10380){ 
    obstacles[177].square(475);
  }
  if(timer > 10425){ 
    obstacles[178].square(475);
  }
  if(timer > 10470){ 
    obstacles[179].square(475);
  }
  if(timer > 10495){ 
    obstacles[180].square(525);
  }
  if(timer > 10600){ 
    obstacles[181].square(525);
  }
  if(timer > 10635){ 
    obstacles[182].square(475);
  }
  if(timer > 10670){ 
    obstacles[183].square(425);
  }
  if(timer > 10705){ 
    obstacles[184].square(375);
  }
  if(timer > 10740){ 
    obstacles[185].square(325);
  }
  if(timer > 10775){ 
    obstacles[186].square(275);
  }
  //===============(10800 = 180s)===============
  if(timer > 10810){ 
    obstacles[187].square(225);
  }
  if(timer > 10845){ 
    obstacles[188].square(175);
  }
  if(timer > 10870){ 
    obstacles[189].square(225);
  }
  if(timer > 10895){ 
    obstacles[190].square(275);
  }
  if(timer > 10920){ 
    obstacles[191].square(325);
  }
  if(timer > 10945){ 
    obstacles[192].square(375);
  }
  if(timer > 10970){ 
    obstacles[193].square(425);
  }
  if(timer > 10995){ 
    obstacles[194].square(475);
  }
  if(timer > 11020){ 
    obstacles[195].square(525);
  }
  if(timer > 11100){ 
    obstacles[182].spike(550);
  }
  if(timer > 11116){ 
    obstacles[183].spike(450);
  }
  if(timer > 11132){ 
    obstacles[184].spike(350);
  }
  if(timer > 11150){ 
    obstacles[196].square(525);
    obstacles[185].spike(300);
  }
  if(timer > 11166){ 
    obstacles[186].spike(350);
  }
  if(timer > 11184){ 
    obstacles[187].spike(450);
  }
  if(timer > 11200){ 
    obstacles[188].spike(550);
  }
  if(timer > 11350){ 
    obstacles[197].square(525);
  }
  if(timer > 11385){ 
    obstacles[198].square(475);
  }
  //===============(11400 = 190s)===============
  if(timer > 11420){ 
    obstacles[199].square(425);
  }
  if(timer > 11455){ 
    obstacles[200].square(375);
  }
  if(timer > 11490){ 
    obstacles[201].square(325);
  }
  if(timer > 11525){ 
    obstacles[202].square(275);
  }
  if(timer > 11560){ 
    obstacles[203].square(225);
  }
  if(timer > 11595){ 
    obstacles[204].square(175);
  }
  if(timer > 11620){ 
    obstacles[205].square(225);
  }
  if(timer > 11645){ 
    obstacles[206].square(275);
  }
  if(timer > 11670){ 
    obstacles[207].square(325);
  }
  if(timer > 11695){ 
    obstacles[208].square(375);
  }
  if(timer > 11720){ 
    obstacles[209].square(425);
  }
  if(timer > 11745){ 
    obstacles[210].square(475);
  }
  if(timer > 11770){ 
    obstacles[211].square(525);
  }
  //===============(END)===============
  if(timer > 11800){ //completed the game
    gameComplete();
  }
  //===============(12000 = 200s)===============
}
