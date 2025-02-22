#!/usr/bin/python3

from bottle import Bottle, route, response, run
import serial
import time
import json
import logging

# Initialize serial connection
def init_serial(port="/dev/ttyUSB0", baudrate=9600, timeout=1):
    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
        time.sleep(5)  # Allow time for initialization
        return ser
    except serial.SerialException as e:
        logger.warning(f"WARN: Error opening serial port: {e}. Will try to initialize it next time.")
        return None

# Function to read from serial port
def read_sensor(sensor_id):
    global ser

    if ser is None:
        ser = init_serial()
        logger.warning("WARN: Serial port not available. Retrying to init it.")
    try:
        ser.write(f"{sensor_id}\n".encode())
        res = ser.readline().decode().strip()
        return res
    except Exception as e:
        logger.warning("WARN: Failed to communicate with the Arduino. Returning None to force caller to read again." + str(e))
        return None

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
    except TypeError:
        logger.warning("WARN: Received the following non-string value: " + json.dumps(string))
        return False

@route("/boiler_temp/current")
def get_temperature_summary():
    sensor1 = ""
    sensor2 = ""
    retries = 10
    while is_float(sensor1) == False or is_float(sensor2) == False or sensor1 == -999 or sensor2 == -999:
        sensor1 = read_sensor(1)
        sensor2 = read_sensor(2)
        if is_float(sensor1) == False:
            logger.warning("WARN: Sensor1 returned non-float result: '" + str(sensor1) + "'. Retrying...")
            sensor1 = -999
        if is_float(sensor2) == False:
            logger.warning("WARN: Sensor2 returned non-float result: '" + str(sensor2) + "'. Retrying...")
            sensor2 = -999
        retries = retries - 1
        if retries <= 0:
            logger.error("ERROR: Retries exhausted. Giving up.")
            response.status = 500
            break
    res = {
        "TOP": sensor2,
        "BOTTOM": sensor1
    }
    logger.info("Result: " + json.dumps(res))
    return res

@route("/boiler_temp/sensor1")
def get_temperature_sensor1():
    return read_sensor(1)

@route("/boiler_temp/sensor2")
def get_temperature_sensor2():
    return read_sensor(2)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logger = logging.getLogger("bottle.app")
    ser = init_serial()
    run(host="0.0.0.0", port=8080, debug=True)

