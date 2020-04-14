//======Serial Recive from MATLAB======//
int command;
float value;
char Buffer[64];
unsigned long commandmillis;
static byte n = 0;
boolean newCommand = false;
int c = 0;


//====== Medición de RPM =======//

#define hallSensor 2
unsigned long pulse;

//====== Mediciones =======//
int const SamplePeriod = 200;
unsigned long StartMillis,
              CurrentMillis,
              sampleTime;
    
//====== Medición de Temperatura =======//

#define TempAmbient A2 //Termistor 103ETB
#define Temp1 A0      //Termistor 103JT-025
#define Temp2 A1      //Termistor 103JT-025
float const inputVoltage = 3.3;
float const refVoltage = 3.3;
int const resistorReference = 10000;
float resistorAmbient,
      resistor1,
      resistor2;

//=====Medicioó de OD ====//
#define DOS 12
#define DOF A3
unsigned long pulseDOF;
unsigned long pulseDOS;

//====== Calentador =======//

#define Heater 9
int Heat,
    heaterValue;

//====== Agitador =======//

#define Stirrer  6
int Speed,
    rpmValue;

//====== Alimentacion de Gas =======//

#define Gas  11
int flowValue;

//====================================================================================================//

void setup() {
  Serial.begin(57600);
  //analogReference(EXTERNAL);
  pinMode(Stirrer, OUTPUT);
  pinMode(Heater, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(Gas, OUTPUT);
  pinMode(TempAmbient, INPUT);
  pinMode(Temp1, INPUT);
  pinMode(Temp2, INPUT);
  pinMode(DOF, INPUT);
  pinMode(DOS, INPUT);
  pinMode(hallSensor, INPUT);
  analogWrite(Stirrer, 100);
}

void loop() {
    parseSerial();
    parseCommand();
}

//====================================================================================================//


void parseSerial(void){
  //Recive el comando a modificar de matlab
  char rc;
  while(Serial.available() && newCommand == false){
    rc = Serial.read();
    if(rc == '\n'){
      n = 0;
      newCommand = true;
    }
    else{
      Buffer[n] = rc;
      n = n +1;
    }
  }

  if(newCommand){
    String read_ = String(Buffer);
    memset(Buffer,0,sizeof(Buffer));
    //Serial.println(read_);
  
    String cmd = read_.substring(0,read_.indexOf(' '));
    command = cmd.toInt();

    String val = read_.substring(read_.indexOf(' '));
    val.trim();
    value = val.toInt();
  }
}

void parseCommand(void){
  if(newCommand){
    if(command == 1){
      digitalWrite(LED_BUILTIN, value);
      Serial.println("1");
    }
    else if(command == 2){
      heaterValue = value; 
      analogWrite(Heater, heaterValue);
      Serial.println("1");
    }
    else if(command == 3){
      rpmValue = value;
      analogWrite(Stirrer, rpmValue);
      Serial.println("1");
    }
    else if(command == 4){
      sendData();
    }
    else if(command == 5){
      flowValue = value;
      analogWrite(Gas, flowValue);
      Serial.println("1");
    }
    newCommand = false;
  }
}

void sendData(void){
  // Inicializa cumuladores de las variables a medir
  pulse = 0;
  pulseDOF = 0;
  pulseDOS = 0;
  resistorAmbient = 0;
  resistor1 = 0;
  resistor2 = 0;
  int sampleNumber = 0;

  // Inicializa conteo de tiempo
  StartMillis = millis();
  CurrentMillis = millis();
  
  // Realiza Media Movil de la mediciones
  while(CurrentMillis - StartMillis <= SamplePeriod){
    sampleNumber += 1;
    CurrentMillis = millis();
    
    pulse += pulseIn(hallSensor,LOW,150000);
    pulseDOF += pulseIn(DOF,HIGH,90000);
    pulseDOS += pulseIn(DOS, HIGH, 90000);
    resistorAmbient += resistorReference/((1023*inputVoltage/(analogRead(TempAmbient)*refVoltage))-1);
    resistor1 += resistorReference/((1023*inputVoltage/(analogRead(Temp1)*refVoltage))-1);
    resistor2 += resistorReference/((1023*inputVoltage/(analogRead(Temp2)*refVoltage))-1);
  }
  pulse = pulse/sampleNumber;
  pulseDOF = pulseDOF/sampleNumber;
  pulseDOS = pulseDOS/sampleNumber;
  resistorAmbient = resistorAmbient/sampleNumber;
  resistor1 = resistor1/sampleNumber;
  resistor2 = resistor2/sampleNumber;
 
  //Escribe los Datos en el Serial
  
  Serial.print(resistorAmbient);
  Serial.print("\t");
  Serial.print(resistor1);
  Serial.print("\t");
  Serial.print(resistor2);
  Serial.print("\t");
  Serial.print(pulse);
  Serial.print("\t");
  Serial.print(pulseDOF);
  Serial.print("\t");
  Serial.println(pulseDOS);
}
