import processing.serial.*;
import cc.arduino.*;

Arduino arduino;

color off = color(4, 79, 111);
color on = color(84, 145, 158);

Serial myPort;   // The Serial Port

// Ratio: 10 pix = (0.01 m)

int h = 700;          // Height of window
int w = 700;          // Width of windows
int radius = 300;    // Radius of circle
float angle = PI/2;
float startX = w/2;            // X-coordinate of the center of the circle
float startY = h/2;            // Y-coordinate of the center of the circle
float endX1 =  w/2;            // X-coordinate of the endpoint of the arrow
float endY1 = h/2 - radius;    // Y-coordinate of the endpoint of the arrow
float angVel = 0;          // Angular velocity
float cenAcc = 0;          // Centripetal acceleration
float radMotion = 0.3;    // Radius of motion
float endX2 = 900;
float endY2 = 400;

float xVel = 0;
float yVel = 0;
float xPos = 350;
float yPos = 350;

// Colors defined here
color white = color(255);
color black = color(65);
color cyan = color(150, 255, 255);
color red = color(255, 0, 0);
color green = color(140, 255, 140);

void setup() {
  size(1090, 700);

  // Prints out the available serial ports.
  println(Arduino.list());
  
  //arduino = new Arduino(this, Arduino.list()[0], 57600);
  // Open the port you are using at the rate you want:
  myPort = new Serial(this, Serial.list()[0], 9600);
  myPort.bufferUntil('\n');
  
}

void draw() {
  background(white);
  
  noStroke();
  fill(black);
  ellipse(startX, startY, radius*2, radius*2);
  arrow(startX, startY, endX1, endY1, cyan, 7); 
  
  stroke(black);
  line(700, 700, 700, 0);
  fill(black);
  textSize(22);
  text("Centripetal Acceleration", 730, 50);
  line(730, 60, 985, 60);
  textSize(18);
  text("Angular velocity = " + nf(angVel,2,3) + " rad/s", 730, 100);
  text("Radius of motion = " + radMotion + " m", 750, 150);
  text("Centripetal acceleration = " + nf(cenAcc, 2, 3) + " m/s^2", 720, 200);
  
  noStroke();
  fill(green);
  ellipse(900, 400, 50, 50);
  arrow(900, 400, endX2, endY2, red, 3);
  redraw();
  
}

void serialEvent(Serial port) {
  // Read the serial buffer:
  String myString = port.readStringUntil('\n');
  if (myString != null) {
    
    float sensors[] = float(split(myString, ' '));
    float change[] = calcDPos(10*sensors[0], 10*sensors[1]);
    println(change);
    
    // Updating angle of the arrow
    angVel = (-sensors[5])/180 * PI;
    angle = angle + angVel * 0.05;
    // Updating centripetal acceleration
    cenAcc = radMotion * angVel * angVel;
    
    startX = startX + change[0];
    startY = startY - change [1];
    endX1 = w/2 - radius * cos(angle) + change[0];
    endY1 = h/2 - radius * sin(angle) - change[1];
    println(endX1);
    println(endY1);
    endX2 = 900 - 10 * cenAcc * cos(angle + PI);
    endY2 = 400 - 10 * cenAcc * sin(angle + PI);
  }

}

void arrow(float x1, float y1, float x2, float y2, color c, int weight) {
  stroke(c);
  strokeWeight(weight);
  line(x1, y1, x2, y2);
  pushMatrix();
  translate(x2, y2);
  float a = atan2(x1-x2, y2-y1);
  rotate(a);
  line(0, 0, -10, -10);
  line(0, 0, 10, -10);
  popMatrix();
}

float[] calcDPos(float accX, float accY) {
  float[] change = {xVel * 0.05 + 0.5 * accX * 0.05*0.05, yVel * 0.05 + 0.5 * accY * 0.05*0.05};
  xVel = xVel + accX * 0.05;
  yVel = yVel + accY * 0.05;
  return change;
}