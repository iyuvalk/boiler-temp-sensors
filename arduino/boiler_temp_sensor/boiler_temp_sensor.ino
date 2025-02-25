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
    sensor1.requestTemperatures();
    sensor2.requestTemperatures();

    float temp1 = sensor1.getTempCByIndex(0);
    float temp2 = sensor2.getTempCByIndex(0);

    // JSON formatted output
    Serial.print("{\"BOTTOM\":");
    Serial.print(temp1);
    Serial.print(",\"TOP\":");
    Serial.print(temp2);
    Serial.println("}");

    delay(2000);  // Send data every 2 seconds
}
