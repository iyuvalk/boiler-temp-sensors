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

ser = init_serial()

app = Bottle()

# Function to read from serial port
def read_sensor(sensor_id):
    global ser

    if ser is None:
        ser = init_serial()
        return {"error": "Serial port not available"}
    try:
        ser.write(f"{sensor_id}\n".encode())
        res = ser.readline().decode().strip()
        return {"sensor": sensor_id, "temperature": res}
    except Exception as e:
        return {"error": str(e)}

@app.route("/boiler_temp/sensor1")
def get_temperature_sensor1():
    return read_sensor(1)

@app.route("/boiler_temp/sensor2")
def get_temperature_sensor2():
    return read_sensor(2)

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8080, debug=True)

