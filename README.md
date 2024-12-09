# DFRobot IOT weather station with M5Stack AtomS3 + PoESP32

I recently got an iot weather station kit from DFRobot, and wrote this very simple MicroPython firmware and Python test client.
Unfortunately, the PoE unit does not seem very well supported so I had to communicate with it using ESP-AT commands manually.
The PoESP32 acts as a TCP server. You can configure this in firmware.py, which must be uploaded to the AtomS3. You may also have to
configure the TX and RX pins for each interface if you are using different hardware / ports. The AtomS3 gets the weather bytes
from the controller board, and then forwards it to the PoESP32 which then will forward it on to TCP clients.

I uploaded this to github as the hardware seemed poorly supported and I had a lot of trouble coding this at first. However this was
built in the UiFlow2 web IDE and uploaded to the AtomS3 through there.