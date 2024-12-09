import os, sys, io
import M5
from M5 import *
from hardware import *
import time

eth_buffer = None
weather_buffer = None

eth_uart = None
weather_uart = None

def get_buffer(interface, databuffer):
  if interface.any(): databuffer.append(interface.read(1).decode("utf-8"))

def stringify_buffer(databuffer):
  return "".join(str(x) for x in databuffer)

def write_interface(interface, message):
  interface.write(message+'\r\n')

def write_interface_with_delay(interface, message, delay):
  interface.write(message+'\r\n')
  time.sleep(delay)

def read_interface(interface):
  if interface.any(): return interface.read().decode()

def read_interface_with_delay(interface, delay):
  if interface.any(): return interface.read().decode()
  time.sleep(delay)

# datalen is length of data in bytes. idk why esp-at is like this it sucks
def write_buffer_to_interface(interface, databuffer, datalen):
  write_interface(interface, "AT+CIPSEND=0,"+str(datalen))
  write_interface(interface, stringify_buffer(databuffer).encode())

def write_buffer_to_interface_with_delay(interface, databuffer, datalen, delay):
  write_interface(interface, "AT+CIPSEND=0,"+str(datalen))
  time.sleep(delay)
  write_interface(interface, stringify_buffer(databuffer).encode())

def setup():
  
  M5.begin()

  global eth_buffer, weather_buffer, eth_uart, weather_uart
  
  # init serial interfaces
  eth_uart = UART(1, baudrate=9600, bits=8, parity=None, stop=1, tx=2, rx=1, txbuf=256, rxbuf=256, timeout=0, timeout_char=0, invert=0, flow=0)
  weather_uart = UART(2, baudrate=9600, bits=8, parity=None, stop=1, tx=39, rx=38, txbuf=256, rxbuf=256, timeout=0, timeout_char=0, invert=0, flow=0)

  # init eth and begin server
  write_interface_with_delay(eth_uart, "AT+RESTORE", 5) # restore default settings just in case
  write_interface_with_delay(eth_uart, "AT+CIPMODE=2", 1) # set esp32 to station mode
  write_interface_with_delay(eth_uart, "AT+CIPMUX=1", 1) # set esp32 to allow multiple connections
  write_interface_with_delay(eth_uart, "AT+CIPSERVER=1,12345", 3) # begin tcp server on port 12345

  # read setup info from eth uart
  read_interface_with_delay(eth_uart, 1)

  # init buffers
  eth_buffer = []
  weather_buffer = []

def loop():
  
  M5.update()
  
  global eth_buffer, weather_buffer, eth_uart, weather_uart
  
  while len(weather_buffer) < 38: get_buffer(weather_uart, weather_buffer)
  write_buffer_to_interface_with_delay(eth_uart, weather_buffer, 37, 0.2)

  weather_buffer = []

if __name__ == '__main__':
  setup()
  while True:
    loop()
