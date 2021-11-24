int led_pin = 14;

#define MAX_PARSE_ELEMENTS 10

void setup() {
  // Set up the built-in LED pin as an output:
  pinMode(led_pin, OUTPUT);

  Serial.begin(115200);
  Serial1.begin(115200);
  Serial1.println("<Arduino is ready>");
  Serial.println("<Arduino is ready>");
}

void loop() {
  //data from pi 1
  if (Serial1.available() > 0) {
    //DEBUG Serial.println("incoming");
    dataParser(Serial1.readStringUntil('\n'));
  }
}

void dataParser(String input){
  input += '\n';                // readStringUntil('\n') removes char '\n' -> needed to calc length
  int msgLenght = input.indexOf('\n');
  //DEBUG Serial.println('--msgLenght--');Serial.println(msgLenght);Serial.println('---');
  
  String msgType;
  int servoId,servoPos,servoSpd;
  
  int delimiters[MAX_PARSE_ELEMENTS]={0};
  int index=0, counter=0;

  //Get index of all ';' in input
  while(index < msgLenght-1){
    delimiters[counter] = input.indexOf(';',index+1);
    //DEBUG Serial.println(delimiters[counter]);
    index = delimiters[counter];
    counter++;
    }
  
  //DEBUG
  //  for (int i=0;i<MAX_PARSE_ELEMENTS;i++ ){
  //    Serial.println(delimiters[i]);
  //  }

  // Parse msgType to correct var
  msgType = input.substring(0,delimiters[0]);

  if (msgType == "move"){
      // Parse data to correct vars
      servoId = input.substring(delimiters[0]+1,delimiters[1]).toInt();
      servoPos = input.substring(delimiters[1]+1,delimiters[2]).toInt();
      servoSpd = input.substring(delimiters[2]+1,delimiters[3]).toInt();
    
      //DEBUG
      Serial.print("#");
      Serial.print("msgType: ");        Serial.print(msgType);
      Serial.print("=> Data: ");
      Serial.print("-> Servo ID: ");       Serial.print(servoId);
      Serial.print("-> Servo Position: "); Serial.print(servoPos);
      Serial.print("-> Servo Speed: ");    Serial.print(servoSpd);
      Serial.println("#"); 
  }
  else if (msgType == "read"){
    Serial.println("nothing yet, sending back nothing");
    Serial1.println("nothing yet...");
  }
  else
      Serial.println("ERROR: WRONG MSGTYPE");  
  
}

//---data to Pi---
//  int i;
//  digitalWrite(led_pin, HIGH);  // set to as HIGH LED is turn-off
//  Serial.println("led_off");
//  Serial1.println("led_off");
//  delay(1000);                   // Wait for 0.1 second
//  digitalWrite(led_pin, LOW);   // set to as LOW LED is turn-on
//  Serial.println("led_on");
//  Serial1.println("led_on");
//  delay(1000);                   // Wait for 0.1 second
