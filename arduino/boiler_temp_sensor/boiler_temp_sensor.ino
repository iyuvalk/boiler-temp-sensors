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

float getFilteredTemperature(DallasTemperature &sensor) {
    float readings[10];
    int count = 0;
    
    // Making one "dummy" request to prevent duplication of old values
    sensor.requestTemperatures();
    sensor.getTempCByIndex(0);
    while (count < 10) {
        sensor.requestTemperatures();
        float temp = sensor.getTempCByIndex(0);
        
        if (temp != DEVICE_DISCONNECTED_C) {
            readings[count] = temp;
            count++;
            delay(5);  // 5ms delay between reads
        } else {
            delay(50);  // Wait 50ms and try again if read fails
        }
    }
    
    // Sort readings
    for (int i = 0; i < 9; i++) {
        for (int j = i + 1; j < 10; j++) {
            if (readings[i] > readings[j]) {
                float temp = readings[i];
                readings[i] = readings[j];
                readings[j] = temp;
            }
        }
    }
    
    // Compute average excluding top 3 and bottom 3 values
    float sum = 0;
    for (int i = 3; i < 7; i++) {
        sum += readings[i];
    }
    return sum / 4.0;
}

void loop() {
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');
        command.trim();
        
        if (command == "1") {
            float avgTemp = getFilteredTemperature(sensor1);
            Serial.println(avgTemp);
        } else if (command == "2") {
            float avgTemp = getFilteredTemperature(sensor2);
            Serial.println(avgTemp);
        }
    }
}
