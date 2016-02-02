
#include <Wire.h>
#include <Adafruit_MMA8451.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_L3GD20.h>

Adafruit_MMA8451 acc = Adafruit_MMA8451();

// Comment this next line to use SPI
//#define USE_I2C

#ifdef USE_I2C
  // The default constructor uses I2C
  Adafruit_L3GD20 gyro();
#else
  // To use SPI, you have to define the pins
  #define GYRO_CS 4 // labeled CS
  #define GYRO_DO 5 // labeled SA0
  #define GYRO_DI 6  // labeled SDA
  #define GYRO_CLK 7 // labeled SCL
  Adafruit_L3GD20 gyro(GYRO_CS, GYRO_DO, GYRO_DI, GYRO_CLK);
#endif

int t;

void setup(void) {
  Serial.begin(9600);

  /*Accelerometer initialization*/
  if (! acc.begin()) {
    /*Serial.println("Couldnt start");*/
    while (1);
  }
 /* Serial.println("MMA8451 found!");*/
  
  acc.setRange(MMA8451_RANGE_2_G);
  /*
  Serial.print("Range = "); Serial.print(2 << acc.getRange());  
  Serial.println("G");
  */

  /*Gyro Sensor initialization*/
  // Try to initialise and warn if we couldn't detect the chip
   if (!gyro.begin(gyro.L3DS20_RANGE_250DPS))
  //if (!gyro.begin(gyro.L3DS20_RANGE_500DPS))
  //if (!gyro.begin(gyro.L3DS20_RANGE_2000DPS))
  {
    Serial.println("Oops ... unable to initialize the L3GD20. Check your wiring!");
    while (1);
  }
  
}

void loop() {
  // Read the 'raw' data in 14-bit counts
  acc.read();
  gyro.read();
  
  /* Get a new sensor event */ 
  sensors_event_t event; 
  acc.getEvent(&event);
  
  //Serial.println(t*0.05);
  
  /* Display Accelerometer data*/
  Serial.print(event.acceleration.x);
  Serial.print(" "); 
  Serial.print(event.acceleration.y);
  Serial.print(" ");
  Serial.print(event.acceleration.z); 
  Serial.print(" ");
  
  /* Display Gyro Sensor data*/
  Serial.print((int)gyro.data.x);   
  Serial.print(" ");
  Serial.print((int)gyro.data.y);   
  Serial.print(" ");
  Serial.println((int)gyro.data.z); 

  t++;
  delay(50);
  
}
