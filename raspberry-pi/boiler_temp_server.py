#!/usr/bin/python3

import serial
import time


def trimmed_average(temps):
    if len(temps) < 7:
        return min(temps) if temps else None  # Return lowest value or None if the list is empty

    sorted_temps = sorted(temps)  # Sort the list
    trimmed_temps = sorted_temps[3:-3]  # Remove the top and bottom 3
    average = sum(trimmed_temps) / len(trimmed_temps)  # Calculate the average

    return average


dev_id = "/dev/ttyUSB0"
s = serial.Serial(dev_id, 9600, timeout=1)
time.sleep(2)

try:
  s.write("1\n".encode())
  res = s.readline()
  print(res.decode(), end="")
finally:
  try:
    s.close()
  except:
    pass

