import os, sys, io
import M5
from M5 import *
import network
from hardware import UART
from umqtt import *



data = None
wlan = None
uart1 = None
mqtt_client = None


buffer2 = None


def setup():
  global data, wlan, uart1, mqtt_client, buffer2

  M5.begin()
  Widgets.fillScreen(0x000000)
  data = Widgets.Label("data", 2, 2, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu9)

  wlan = network.WLAN(network.STA_IF)
  wlan.connect(ssid, password)
  print(wlan.ifconfig()[0])
  mqtt_client = MQTTClient(mqttBrokerName, mqttBrokerAddress, port=1883, user='', password='', keepalive=300)
  mqtt_client.connect(clean_session=True)
  mqtt_client.check_msg()
  uart1 = UART(1, baudrate=9600, bits=8, parity=None, stop=1, tx=1, rx=2)
  uart1.flush()


def loop():
  global data, wlan, uart1, mqtt_client, buffer2
  M5.update()
  if (uart1.any()) >= 38:
    buffer2 = uart1.read()
    print(buffer2.decode('utf-8'))
    data.setText(str(buffer2.decode('utf-8')))
    # Assuming buffer2 contains the received data

    # Wind direction
    winddir = buffer2[0:4].decode("utf-8")
    if winddir[0] == 'c' and winddir[1:4] not in ['...', '---']:
        print(f"wind dir: {winddir[1:4]}°")
    else:
        print("wind direction: sensor error or not available")

    # Wind speed (1 minute average)
    windspeed = buffer2[4:8].decode("utf-8")
    if windspeed[0] == 's' and windspeed[1:4] not in ['...', '---']:
        print(f"wind speed: {windspeed[1:4]} mph")
    else:
        print("wind speed: sensor error or not available")

    # Gust speed (5 minute maximum)
    gustspeed = buffer2[8:12].decode("utf-8")
    if gustspeed[0] == 'g' and gustspeed[1:4] not in ['...', '---']:
        print(f"gust speed: {gustspeed[1:4]} mph")
    else:
        print("gust speed: sensor error or not available")

    # Temperature
    temperature = buffer2[12:16].decode("utf-8")
    if temperature[0] == 't' and temperature[1:4] not in ['...', '---']:
        try:
            temp_f = int(temperature[1:4])
            print(f"temperature: {temp_f}°F")
        except ValueError:
            print("temperature: invalid sensor reading")
    else:
        print("temperature: sensor error or not available")

    # Rainfall (1 hour)
    rain1h = buffer2[16:20].decode("utf-8")
    if rain1h[0] == 'r' and rain1h[1:4] not in ['...', '---']:
        try:
            rain = int(rain1h[1:4])
            print(f"rainfall 1h: {rain * 0.01} inches")  # Convert to inches
        except ValueError:
            print("rainfall 1h: invalid sensor reading")
    else:
        print("rainfall 1h: sensor error or not available")

    # Rainfall (24 hours)
    rain24h = buffer2[20:24].decode("utf-8")
    if rain24h[0] == 'p' and rain24h[1:4] not in ['...', '---']:
        try:
            rain = int(rain24h[1:4])
            print(f"rainfall 24h: {rain * 0.01} inches")  # Convert to inches
        except ValueError:
            print("rainfall 24h: invalid sensor reading")
    else:
        print("rainfall 24h: sensor error or not available")

    # Humidity
    humidity = buffer2[24:27].decode("utf-8")
    if humidity[0] == 'h' and humidity[1:3] not in ['..', '--']:
        try:
            hum = int(humidity[1:3])
            print(f"humidity: {hum}%")
        except ValueError:
            print("humidity: invalid sensor reading")
    else:
        print("humidity: sensor error or not available")

    # Barometric pressure
    pressure = buffer2[27:33].decode("utf-8")
    if pressure[0] == 'b' and pressure[1:5] not in ['....', '----']:
        try:
            press = int(pressure[1:5]) / 10  # Convert to hPa
            print(f"pressure: {press}hPa")
        except ValueError:
            print("pressure: invalid sensor reading")
    else:
        print("pressure: sensor error or not available")

    # Checksum verification (optional)
    if len(buffer2) > 33:
        checksum = buffer2[33:].decode("utf-8").strip()
        if checksum.startswith('*'):
            print(f"checksum: {checksum} (verification not implemented)")
    if mqtt_client.isconnected():
      mqtt_client.publish('weather/data', buffer2, qos=1)
    else:
      mqtt_client.reconnect()


if __name__ == '__main__':
  try:
    setup()
    while True:
      loop()
  except (Exception, KeyboardInterrupt) as e:
    try:
      from utility import print_error_msg
      print_error_msg(e)
    except ImportError:
      print("please update to latest firmware")
