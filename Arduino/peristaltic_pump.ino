 
int takeSample,
    continuousFlow,
    last_sample;
#define sample 13
#define continuous 8 
#define pump 3
#define dir 2
#define MS1 6
#define MS2 5
#define MS3 4

void setup() {

  //pinMode(LED_BUILTIN, OUTPUT);
  //digitalWrite(LED_BUILTIN, LOW);
  pinMode(sample, INPUT);
  pinMode(continuous, INPUT);
  pinMode(dir, OUTPUT);
  pinMode(pump, OUTPUT);
  pinMode(MS1, OUTPUT);
  pinMode(MS2, OUTPUT);
  pinMode(MS3, OUTPUT);

  digitalWrite(dir, LOW);
  digitalWrite(MS1, HIGH);
  digitalWrite(MS2, LOW);
  digitalWrite(MS3, LOW);
  last_sample = 0;
}

void loop() {

  digitalWrite(pump,HIGH);
  digitalWrite(pump,LOW);
  delay(4);
//  takeSample = digitalRead(sample);
//  continuousFlow = digitalRead(continuous);
//
//  if(takeSample != last_sample && takeSample == 1){
//    Serial.println("Start");
//    for(int i = 0; i < 3887; i++){
//      digitalWrite(pump,HIGH);
//      digitalWrite(pump,LOW);
//      delay(10);
//    }
//    last_sample = 1;
//  }
//  if(last_sample == 1){
//    last_sample = digitalRead(sample);
//  }



  
}
