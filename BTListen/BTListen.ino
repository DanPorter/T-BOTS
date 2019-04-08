#include <SoftwareSerial.h>

SoftwareSerial BTSerial(17,16);  // RX, TX
String Data = "";
#define    STX          0x02
#define    ETX          0x03
String Wait = "Waiting\n";
void setup()  
{
    Serial.begin(38400);
    BTSerial.begin(38400);
    
}

void loop() // run over and over
{

  Serial.print(Wait);
  delay(1000);
  
    while (BTSerial.available())
    {
        char character = BTSerial.read(); // Receive a single character from the software serial port
        
        if (character == ETX) {
          Data.concat(character);
          Data.concat((char)0x0A);
          Serial.print(Data);
          Data = "";
        }
        
        Data.concat(character); // Add the received character to the receive buffer
        Serial.print(Data);

            // Add your code to parse the received line here....

            // Clear receive buffer so we're ready to receive the next line
            // Data = "";
        
    }
    
    /*
       BTSerial.print((char)STX);
   BTSerial.print((char)0x1);
   //BTSerial.print(fping);
   BTSerial.print(1);
   BTSerial.print((char)0x4);
   BTSerial.print(1);
   BTSerial.print((char)0x5);
 //  BTSerial.print(KI_last);
   BTSerial.print(1);
   BTSerial.print((char)ETX);
   */
}
