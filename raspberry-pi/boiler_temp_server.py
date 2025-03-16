#!/usr/bin/python3

from bottle import Bottle, route, response, run
import serial
import time
import json
import logging
import threading

latest_temperatures = []
CACHE_SIZE = 150 # 150 samples at the rate of one sample every two seconds is the number of samples we'll have in 5 minutes

# Function to continuously read data from Arduino
def read_serial_data(port="/dev/ttyUSB0", baudrate=9600, timeout=2):
    global latest_temperatures
    while True:
        try:
            ser = serial.Serial(port, baudrate, timeout=timeout)
            try:
                raw_data = ser.readline().decode('utf-8').strip()
                logging.debug("Raw Arduino data: " + raw_data)
                if raw_data:
                    temp_data = json.loads(raw_data)
                    if is_float(temp_data.get("TOP", "")) and \
                            is_float(temp_data.get("BOTTOM", "")) and \
                            float(temp_data.get("TOP", "")) > -127 and \
                            float(temp_data.get("BOTTOM", "")) > -127:  # The sensor sometimes returns -127 for some reason
                        latest_temperatures.append(
                            {
                                "TOP": float(temp_data.get("TOP", None)),
                                "BOTTOM": float(temp_data.get("BOTTOM", None)),
                                "ts": time.time()
                            }
                        )
                        if len(latest_temperatures) > CACHE_SIZE:
                            latest_temperatures.pop(0)
            except json.JSONDecodeError:
                logging.warning("Warning: Received malformed JSON from Arduino.")
            except serial.SerialException as e:
                logging.warning(f"Serial Error: {e}")
                break  # Stop reading if there's a serial error
            time.sleep(2)
        except serial.SerialException as e:
            logging.warning(f"Error: Could not open serial port {port} - {e}")
            time.sleep(30)

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
    if len(latest_temperatures) > 0:
        res = {
            "TOP": sum(d["TOP"] for d in latest_temperatures) / len(latest_temperatures),
            "BOTTOM": sum(d["BOTTOM"] for d in latest_temperatures) / len(latest_temperatures),
            "minTS": min(d["ts"] for d in latest_temperatures),
            "maxTS": max(d["ts"] for d in latest_temperatures)
        }
        return res
    else:
        return -9999

@route("/boiler_temp/sensor1")
def get_temperature_sensor1():
    if len(latest_temperatures) > 0:
        return sum(d["TOP"] for d in latest_temperatures) / len(latest_temperatures)
    else:
        return -9999

@route("/boiler_temp/sensor2")
def get_temperature_sensor2():
    if len(latest_temperatures) > 0:
        return sum(d["TOP"] for d in latest_temperatures) / len(latest_temperatures)
    else:
        return -9999

@route("/boiler_temp/dump_cache")
def dump_cache():
    return json.dumps(latest_temperatures)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logger = logging.getLogger("bottle.app")

    # Start the background thread for serial reading
    serial_thread = threading.Thread(target=read_serial_data, daemon=True)
    serial_thread.start()

    run(host="0.0.0.0", port=8080, debug=True)

