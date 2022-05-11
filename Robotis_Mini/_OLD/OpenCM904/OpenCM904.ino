#include <DynamixelSDK.h>

//#############DYNAMIXEL#############
#define PROTOCOL_VERSION                2.0                 // See which protocol version is used in the Dynamixel
#define BAUDRATE                        1000000             // default for xl320: 1 mil
#define DEVICENAME                      "1"                 // "1" -> Serial1 | "2" -> //Serial2 | "3" -> //Serial2(OpenCM 485 EXP)

// Control table address (XL320)
#define ADDR_PRO_TORQUE_ENABLE          24                 // Control table address is different in Dynamixel model
#define ADDR_PRO_GOAL_POSITION          30
#define ADDR_PRO_PRESENT_POSITION       37

#define TORQUE_ENABLE                   1                   // Value for enabling the torque
#define TORQUE_DISABLE                  0                   // Value for disabling the torque
#define DXL_MINIMUM_POSITION_VALUE      500                 // Dynamixel will rotate between this value
#define DXL_MAXIMUM_POSITION_VALUE      550                 // and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
#define DXL_MOVING_STATUS_THRESHOLD     20                  // Dynamixel moving status threshold

#define ESC_ASCII_VALUE                 0x1b
//###################################

//#############CODE VARS#############
#define MAX_PARSE_ELEMENTS 10

String msgType;
int servoId,servoPos,servoSpd;

int led_pin = 14;
//###################################


void setup() {
  // Set up the built-in LED pin as an output:
  pinMode(led_pin, OUTPUT);
  
  //Start serial interfaces: Serial= debugging | //Serial2 =  communication with Pi
  Serial.begin(115200);
  while(!Serial);
  Serial2.begin(115200);
  while(!Serial2);
  
  delay(500);

  // Initialize PortHandler instance + Set the port path
  dynamixel::PortHandler *portHandler = dynamixel::PortHandler::getPortHandler(DEVICENAME); 
  // Initialize PacketHandler instance + Set the protocol version
  dynamixel::PacketHandler *packetHandler = dynamixel::PacketHandler::getPacketHandler(PROTOCOL_VERSION);

  int dxl_comm_result = COMM_TX_FAIL;             // Communication result
  uint8_t dxl_error = 0;                          // Dynamixel error
  uint16_t dxl_model_number;                      // Dynamixel model number
  std::vector<uint8_t> vec;                       // Dynamixel data storages


  
  // communicate state with Pi and debug
  Serial.println("<Arduino is ready>");
  delay(250);
  Serial2.println("<Arduino is ready>");
  delay(250);

  int output;
  
  SetPortAndBaud(portHandler);

  PingAll(packetHandler, portHandler, &vec);
  
  //Serial.println("test: disable torque");
  //SetTorque(false, 1, packetHandler, portHandler);
  //SetTorque(true, 1, packetHandler, portHandler);

  //main loop
  Serial.println("Main Loop");
  while(1){
    //  //data from pi 1
    if (Serial2.available() > 0){
      //DEBUG Serial.println("incoming");
      DataParser(Serial2.readStringUntil('\n'));
    }
  }

  //ReadPos(1, packetHandler, portHandler);
  //WritePos(1,500,packetHandler, portHandler);
  //delay(1000);
  //WritePos(1,550,packetHandler, portHandler);
  //delay(1000);
}

//-----------
void loop(){}
//-----------

void SetPortAndBaud(dynamixel::PortHandler *portHandler){
  
  // Open port
  if (!portHandler->openPort()){
    Serial.println("error with opening port.");
    return;
  }

  // Set port baudrate
  if (!portHandler->setBaudRate(BAUDRATE)){
    Serial.println("error with setting baudrate.");
    return;
  }
  
  Serial.println("Opened port and set baudrate succesfully");
  return;
}


void PingAll(dynamixel::PacketHandler *packetHandler, dynamixel::PortHandler *portHandler, std::vector<uint8_t> *vec){
  // Try to broadcast ping the Dynamixel
  int dxl_comm_result = COMM_TX_FAIL;
  
  dxl_comm_result = packetHandler->broadcastPing(portHandler, *vec);
  if (dxl_comm_result != COMM_SUCCESS) packetHandler->getTxRxResult(dxl_comm_result);

  Serial.print("Detected Dynamixel : \n");
  for (int i = 0; i < (int)(*vec).size(); i++)
  {
    Serial.print("ID : ");
    Serial.println((*vec).at(i));
  }
}

void ReadPos(int dxl_id, dynamixel::PacketHandler *packetHandler, dynamixel::PortHandler *portHandler){
  // Read present position
  int16_t dxl_present_position = 0;               // Present position
  int16_t dxl_comm_result = COMM_TX_FAIL;
  uint8_t dxl_error=0;
      
  dxl_comm_result = packetHandler->read2ByteTxRx(portHandler, dxl_id, ADDR_PRO_PRESENT_POSITION, (uint16_t*)&dxl_present_position, &dxl_error);
  if (dxl_comm_result != COMM_SUCCESS)
  {
    packetHandler->getTxRxResult(dxl_comm_result);
  }
  else if (dxl_error != 0)
  {
    packetHandler->getRxPacketError(dxl_error);
  }
  
  Serial.print("[ID:");      Serial.print(dxl_id);
  Serial.print(" PresPos:");  Serial.print(dxl_present_position);
  Serial.println(" ");
}

void WritePos(int dxl_id, int dxl_goal, dynamixel::PacketHandler *packetHandler, dynamixel::PortHandler *portHandler){
  // Write goal position
  int16_t dxl_comm_result = COMM_TX_FAIL;
  uint8_t dxl_error=0;
  dxl_comm_result = packetHandler->write2ByteTxRx(portHandler, dxl_id, ADDR_PRO_GOAL_POSITION, dxl_goal, &dxl_error);
  if (dxl_comm_result != COMM_SUCCESS)
  {
    packetHandler->getTxRxResult(dxl_comm_result);
  }
  else if (dxl_error != 0)
  {
    packetHandler->getRxPacketError(dxl_error);
  }
}

void SetTorque(bool input, int dxl_id, dynamixel::PacketHandler *packetHandler, dynamixel::PortHandler *portHandler){

  int dxl_comm_result = COMM_TX_FAIL;
  uint8_t dxl_error = 0;                          // Dynamixel error
  
  if(input){
    dxl_comm_result = packetHandler->write1ByteTxRx(portHandler, dxl_id, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE, &dxl_error);
    if (dxl_comm_result != COMM_SUCCESS)
    {
      packetHandler->getTxRxResult(dxl_comm_result);
    }
    else if (dxl_error != 0)
    {
      packetHandler->getRxPacketError(dxl_error);
    }
    else
    {
      Serial.print("Dynamixel has been successfully connected \n");
    }
  }
  else{
    // Disable Dynamixel Torque
    dxl_comm_result = packetHandler->write1ByteTxRx(portHandler, dxl_id, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE, &dxl_error);
    if (dxl_comm_result != COMM_SUCCESS)
    {
      packetHandler->getTxRxResult(dxl_comm_result);
    }
    else if (dxl_error != 0)
    {
      packetHandler->getRxPacketError(dxl_error);
    }
  }
}

void DataParser(String input){
  input += '\n';                // readStringUntil('\n') removes char '\n' -> needed to calc length
  int msgLenght = input.indexOf('\n');
  //DEBUG Serial.println('--msgLenght--');Serial.println(msgLenght);Serial.println('---');
  
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
    Serial2.println("nothing yet...");
  }
  else if (msgType == "ping"){
    Serial.println("Ping: nothing yet...");
    //
  }
  else if (msgType == "torque"){
    Serial.println("Torque: nothing yet...");
  }
  else
    Serial.println("ERROR: WRONG MSGTYPE");  
  
}

//---data to Pi---
//  int i;
//  digitalWrite(led_pin, HIGH);  // set to as HIGH LED is turn-off
//  Serial.println("led_off");
//  //Serial2.println("led_off");
//  delay(1000);                   // Wait for 0.1 second
//  digitalWrite(led_pin, LOW);   // set to as LOW LED is turn-on
//  Serial.println("led_on");
//  //Serial2.println("led_on");
//  delay(1000);                   // Wait for 0.1 second