/* Arduino Tutorial: How to use a magnetic contact switch 
   Dev: Michalis Vasilakis // www.ardumotive.com // Date: 4/8/2016 */
#include  <LiquidCrystal.h>

LiquidCrystal lcd(12, 11, 10, 5, 4, 3, 2);

const int buzzer = 6; 
const int magSensor = 9;
const int pirPin = 7;
const int backLight = 13;

int state; // 0 close - 1 open wwitch
int pirState;

void setup()
{
  pinMode(magSensor, INPUT_PULLUP);
  pinMode(pirPin, INPUT);
  pinMode(backLight, OUTPUT);
  analogWrite(backLight, 150); 
  Serial.begin(9600);       
  lcd.begin(16,2);                
  lcd.clear();
}

void loop()
{
  state = digitalRead(magSensor);
  pirState = digitalRead(pirPin);
  
  if (state == HIGH && pirState == HIGH){
    lcd.clear();
    lcd.setCursor(0,0);                 // set cursor to column 0, row 0 (first row)
    lcd.print("Both high");       // input your text here
    lcd.setCursor(0,1);                 // move cursor down one
    lcd.print("Both high");      //input your text here
    tone(buzzer, 500); 
    Serial.println("Send Email");     //send email
  }
  else if(state == HIGH && pirState == LOW){
    lcd.clear();
    lcd.setCursor(0,0);                 // set cursor to column 0, row 0 (first row)
    lcd.print("Magnetic high");       // input your text here
    lcd.setCursor(0,1);                 // move cursor down one
    lcd.print("Magnetic high");      //input your text here
    tone(buzzer, 500); 
    
  }else{
    lcd.clear();
    lcd.setCursor(0,0);                 // set cursor to column 0, row 0 (first row)
    lcd.print("All low");       // input your text here
    lcd.setCursor(0,1);                 // move cursor down one
    lcd.print("All low");
    noTone(buzzer);
  }
  delay(3000);
}

