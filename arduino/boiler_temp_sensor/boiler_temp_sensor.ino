#include <OneWire.h>
#include <DallasTemperature.h>

#define SENSOR_1_PIN 2  // Pin for first DS18B20 sensor
#define SENSOR_2_PIN 3  // Pin for second DS18B20 sensor

OneWire oneWire1(SENSOR_1_PIN);
OneWire oneWire2(SENSOR_2_PIN);
DallasTemperature sensor1(&oneWire1);
DallasTemperature sensor2(&oneWire2);


void setup() {
    Serial.begin(9600);
    sensor1.begin();
    sensor2.begin();
}

void loop() {
    // Process serial commands
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');
        command.trim();

        if (command == "1") {
            sensor1.requestTemperatures();
            float temp1 = sensor1.getTempCByIndex(0);
            if (temp1 != DEVICE_DISCONNECTED_C) {
              Serial.println(temp1);
            } else {
              Serial.println("-");
            }
        } else if (command == "2") {
            sensor2.requestTemperatures();
            float temp2 = sensor2.getTempCByIndex(0);
            if (temp2 != DEVICE_DISCONNECTED_C) {
              Serial.println(temp2);
            } else {
              Serial.println("-");
            }
        }
    }
    
    delay(1000);
}
