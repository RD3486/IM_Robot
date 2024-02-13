int mr1 = 6; 
int mr2 = 9;
int ml1 = 5;
int ml2 = 4; 
int trig = 10;
int echo = 11;
int distance = 0;
long duration;

int rightWheelSpeed = 247;
int leftWheelSpeed = 255;

// time for going 50 cm.
int straightTime = 2600;

void setup()
{
  //Serial.begin(9600);
  pinMode(mr1,OUTPUT);
  pinMode(ml1,OUTPUT);
  pinMode(mr2,OUTPUT);
  pinMode(ml2,OUTPUT);
  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);
  analogWrite(ml1,OUTPUT);
  analogWrite(ml2,OUTPUT);
  analogWrite(mr1,OUTPUT);
  analogWrite(mr2,OUTPUT);
  Serial.begin(9600);
}
void forward()
{
  analogWrite(mr1,rightWheelSpeed);
  analogWrite(mr2,LOW);
  analogWrite(ml1,leftWheelSpeed);
  analogWrite(ml2,LOW);
}

void right()
{
  analogWrite(mr1,rightWheelSpeed);
  analogWrite(mr2,LOW);
  analogWrite(ml1,LOW);
  analogWrite(ml2,leftWheelSpeed);
}

void left()
{
  analogWrite(mr1,LOW);
  analogWrite(mr2,rightWheelSpeed);
  analogWrite(ml1,leftWheelSpeed);
  analogWrite(ml2,LOW);
}

void backward()
{
  right();
  delay(1000);
  right();
  delay(1000);
  forward();
  delay(straightTime);
}

void stop()
{
  analogWrite(mr1,LOW);
  analogWrite(mr2,LOW);
  analogWrite(ml1,LOW);
  analogWrite(ml2,LOW);
}

void get_dist()
{
  distance = 0;
  for (int i = 0; i < 20;i++)
    {
      digitalWrite(trig, LOW);
      delayMicroseconds(2);
      digitalWrite(trig, HIGH);
      delayMicroseconds(10);
      digitalWrite(trig, LOW);
      duration = pulseIn(echo, HIGH);
      distance += (duration * 0.034) / 2;
    }
    Serial.println(distance/20);
}

void executeCommand(char cmd)
{
  switch(cmd)
  {
    case 'F':
      forward();
      delay(straightTime);
      stop();
      break;
    case 'B':
      backward();
      stop();
      break;
    case 'R':
      right();
      // original thousand
      delay(1300);
      stop();
      break;
    case 'L':
      left();
      // original 1000
      delay(700);
      stop();
      break;
    case 'W':
      forward();
      delay(100);
      stop();
      break;
    case 'A':
      left();
      delay(100);
      stop();
      break;
    case 'D':
      right();
      delay(100);
      stop();
      break;
    case 'O':
      get_dist();
      break;
    case 'S':
      stop();
      break;
  }
}

void loop()
{
  if(Serial.available() > 0)
  {
    char cmd = Serial.read();
    executeCommand(cmd);
    
  }
    Serial.flush();
}