#!/usr/bin/python3

from bottle import Bottle, response, run
import serial
import time

# Initialize serial connection
def init_serial(port="/dev/ttyUSB0", baudrate=9600, timeout=1):
    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
        time.sleep(2)  # Allow time for initialization
        return ser
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        return None

# Function to read from serial port
def read_sensor(sensor_id):
    global ser

    if ser is None:
        ser = init_serial()
        print("ERROR: Serial port not available")
        return {"error": "Serial port not available"}
    try:
        ser.write(f"{sensor_id}\n".encode())
        res = ser.readline().decode().strip()
        return res
    except Exception as e:
        print("ERROR: " + str(e))
        return {"error": str(e)}

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


ser = init_serial()
app = Bottle()

@app.route("/boiler_temp/current")
def get_temperature_summary():
    sensor1 = ""
    sensor2 = ""
    while is_float(sensor1) == False or is_float(sensor2) == False:
        sensor1 = read_sensor(1)
        sensor2 = read_sensor(2)
        if is_float(sensor1) == False:
            print("WARN: Sensor1 returned non-float result: " + str(sensor1) + ". Retrying...")
        if is_float(sensor2) == False:
            print("WARN: Sensor2 returned non-float result: " + str(sensor2) + ". Retrying...")


    return {
        "TOP": sensor2,
        "BOTTOM": sensor1
    }

@app.route("/boiler_temp/sensor1")
def get_temperature_sensor1():
    return read_sensor(1)

@app.route("/boiler_temp/sensor2")
def get_temperature_sensor2():
    return read_sensor(2)

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8080, debug=True)

