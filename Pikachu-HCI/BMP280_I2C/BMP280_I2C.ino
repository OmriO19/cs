/******************************************************
  Name: BMP280_I2C
  Description: Use the I2C interface of BMP280 to detect temperature, air pressure and sea-level height
  Connection:
   BMP280       Uno/Mega2560
   VCC            5V
   GND            GND
   SCK        A5 Uno/Pin21 mega2560
   SDI        A4 Uno/Pin20 mega2560
*********************************************************/

#include <Wire.h>
#include <Adafruit_BMP280.h>
float current_val=0;
float compare_val=0;
float epsilon = 30;
unsigned long myTime;
boolean flag=false;
int led_2_pin = 9;
int light =0;
Adafruit_BMP280 bmp280; //Define a variable bmp280 of Adafruit_BMP280 type. Subsequently bmp280 represents Adafruit_BMP280

void setup() {
  Serial.begin(9600);  //Set the baud rate of serial monitor as 9600bps
  Serial.println(F("BMP280_I2C"));//print BMP280_I2C on serial monitor
  pinMode(led_2_pin,OUTPUT);
  if (!bmp280.begin()) //if bmp280.begin()==0, it means bmp280 initialization fails.
  {
    Serial.println(F("Could not find a valid BMP280 sensor, check wiring!"));
    while (1);//Infinite loop, no stop until the initialization succeeds.
  }
  
}

void loop() {


  myTime = millis();

  if(myTime > 100 && flag==false){
      flag=true;
      compare_val = bmp280.readPressure();
      
  }
  if(flag==true){
      current_val = bmp280.readPressure();
 
      if(current_val<compare_val + epsilon){
        current_val=0;
      }
      else{ 
        current_val=current_val-compare_val;
      }
      //light = Serial.parseInt();
      light=255;
      if(light==255){
   
        digitalWrite(led_2_pin,HIGH);
      }
      else{
        digitalWrite(led_2_pin,LOW);
      }
      Serial.println (current_val);     // Sending the output to Processing IDE
      delay(10);

  }
   
  
}
