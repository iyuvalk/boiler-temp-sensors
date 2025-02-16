#!/usr/bin/python3

import serial
import time

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

