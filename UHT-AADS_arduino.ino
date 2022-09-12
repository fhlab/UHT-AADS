//Enter Values Here
const float sortThresh = 6; // in volts
const float dropletThresh = 2; // in volts
const float minVoltage = 4; // in voltz
const int minResidence = 2; // in microseconds
const int maxResidence=5000; // in microseconds
const int outputSource = 13; //connect this pin to function generator
const int inputSource = A0; //connect photodetector input to this pin

//Other Global Variables
float absRead;
long dropletWidth;
long dropletTimerEnd;
long dropletTimerStart;

// Absorbance read
float reading(){
absRead = analogRead(inputSource);
absRead = absRead/4096*10; //change 4096 depending on analogReadResolution
return absRead;
}

void setup() {
  Serial.begin(9600);
  pinMode(outputSource, OUTPUT);
  analogReadResolution(12);
 REG_ADC_MR = (REG_ADC_MR & 0xFFF0FFFF) | 0x00020000; //faster analog read
}

// Pulses according to parameters
void pulse(){
delayMicroseconds(50);
digitalWrite(outputSource, HIGH);
delayMicroseconds(50);
digitalWrite(outputSource, LOW);
}

// Advanced sorting algorithm
void sortAdv(){
  absRead = reading();
  if (absRead < dropletThresh){
    if (absRead < sortThresh){
      while (absRead < dropletThresh && absRead > minVoltage){
        absRead = reading();
      }
      dropletTimerEnd = micros();
      dropletWidth = dropletTimerEnd-dropletTimerStart;
      if (dropletWidth > minResidence && dropletWidth < maxResidence){
          pulse();
      }
    }   
  } 
  else {
    dropletTimerStart = micros();
  }
}

// Main loop
void loop(){
  sortAdv();
}
